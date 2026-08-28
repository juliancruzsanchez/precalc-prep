#!/usr/bin/env python3
"""Find replacement videos on YouTube for any IDs that failed to download.

For each missing video in _inventory.json:
  1. Search YouTube for the title (preferring the same channel)
  2. Pick the best-matching result
  3. Download it to the new video ID
  4. Patch course.json so the new ID replaces the old one (keeping the
     original title/curriculum placement intact)

Usage:
    python3 replace_missing_videos.py            # replace all missing
    python3 replace_missing_videos.py --limit 3  # try the first 3
    python3 replace_missing_videos.py --dry-run  # search only, don't download

This is best-effort: search results aren't always a perfect topic match.
Review the diff to course.json before committing.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INV = ROOT / "App" / "Resources" / "Content" / "Videos" / "_inventory.json"
COURSE = ROOT / "App" / "Resources" / "Content" / "course.json"
OUT = ROOT / "App" / "Resources" / "Content" / "Videos"


def have(vid: str) -> bool:
    p = OUT / f"{vid}.mp4"
    return p.exists() and p.stat().st_size > 100_000


def search_youtube(query: str, max_results: int = 5) -> list[dict]:
    """Run `yt-dlp ytsearch:` and return [{id, title, channel}, ...]."""
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--no-warnings",
        "--skip-download",
        "--get-id", "--get-title", "--get-channel",
        "-J",  # dump JSON for the last entry
    ]
    # Easier: use --dump-json with --flat-playlist
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--no-warnings",
        "--skip-download",
        "--flat-playlist",
        "-J",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0 or not result.stdout.strip():
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    entries = data.get("entries", []) if isinstance(data, dict) else data
    out = []
    for e in entries:
        if not e:
            continue
        out.append({
            "id": e.get("id", ""),
            "title": e.get("title", ""),
            "channel": e.get("channel") or e.get("uploader") or "",
        })
    return out


def pick_best(results: list[dict], wanted_title: str, wanted_channel: str) -> dict | None:
    """Score results by title overlap and channel match."""
    if not results:
        return None
    wanted_words = set(re.findall(r"\w+", wanted_title.lower())) - {"a", "the", "of", "and", "to", "in", "for", "on"}
    def score(r: dict) -> int:
        s = 0
        title_words = set(re.findall(r"\w+", r["title"].lower()))
        overlap = len(wanted_words & title_words)
        s += overlap * 3
        if wanted_channel and wanted_channel.lower() in r["channel"].lower():
            s += 10
        if r["channel"].lower() == wanted_channel.lower():
            s += 5
        return s
    return max(results, key=score, default=None)


def download(vid: str) -> bool:
    cmd = [
        "yt-dlp",
        "-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[height<=720]+ba/b[height<=720]/b",
        "--merge-output-format", "mp4",
        "--remux-video", "mp4",
        "-o", str(OUT / f"{vid}.%(ext)s"),
        "--no-playlist",
        "--no-warnings",
        "--no-progress",
        f"https://www.youtube.com/watch?v={vid}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0 and (OUT / f"{vid}.mp4").exists() and (OUT / f"{vid}.mp4").stat().st_size > 100_000


def patch_course_json(replacements: dict[str, str]) -> int:
    """Replace old_id with new_id in course.json. Returns count of substitutions."""
    text = COURSE.read_text()
    count = 0
    for old, new in replacements.items():
        # The youtubeId appears inside video objects as `"youtubeId": "OLD"`.
        # Use a quoted match to avoid hitting substrings.
        before = text
        text = text.replace(f'"youtubeId": "{old}"', f'"youtubeId": "{new}"')
        if text != before:
            count += 1
    if count:
        COURSE.write_text(text)
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true", help="search only, don't download or patch")
    args = parser.parse_args()

    inv = json.loads(INV.read_text())
    missing = [v for v in inv if not have(v["id"])]
    if args.limit:
        missing = missing[: args.limit]
    print(f"Attempting to replace {len(missing)} missing videos")

    replacements: dict[str, str] = {}
    for v in missing:
        query = f"{v['title']} {v['channel']}"
        print(f"\n[{v['id']}] {v['title']}  ({v['channel']})")
        results = search_youtube(query, max_results=5)
        if not results:
            print("  no search results")
            continue
        best = pick_best(results, v["title"], v["channel"])
        if not best:
            continue
        print(f"  -> {best['id']}  {best['title']}  [{best['channel']}]")
        if best["id"] == v["id"]:
            print("  (same ID, skipping — must be a different problem)")
            continue
        if args.dry_run:
            continue
        if not download(best["id"]):
            print(f"  download failed for {best['id']}")
            continue
        size = (OUT / f"{best['id']}.mp4").stat().st_size // 1024
        print(f"  ok ({size} KB)")
        replacements[v["id"]] = best["id"]

    if args.dry_run:
        print(f"\n(dry run — would replace {len(replacements)} IDs in course.json)")
        return 0

    if not replacements:
        print("\nNo replacements to make.")
        return 0

    n = patch_course_json(replacements)
    # Also update the inventory so the new IDs are the ones tracked.
    new_inv = []
    for entry in inv:
        if entry["id"] in replacements:
            old_id = entry["id"]
            new_id = replacements[old_id]
            new_inv.append({**entry, "id": new_id, "replaces": old_id})
        else:
            new_inv.append(entry)
    INV.write_text(json.dumps(new_inv, indent=2))
    print(f"\nPatched course.json ({n} substitutions) and inventory ({len(replacements)} entries).")
    print("Next: run `xcodegen generate` so the new MP4 filenames get added to the Xcode project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
