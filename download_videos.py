#!/usr/bin/env python3
"""Download every YouTube video referenced in the curriculum at 720p.

Uses `yt-dlp`, the actively-maintained community fork of youtube-dl.
youtube-dl's last release (2021.12.17) is too old for YouTube's current
API and fails on basically everything with "The page needs to be
reloaded" or "No video formats found". yt-dlp keeps the same CLI and
fixes the extractor.

Install:
    brew install yt-dlp ffmpeg

Resumable: skips IDs that already have a file in the Videos/ directory.
Filenames are the YouTube video ID, so they line up 1:1 with the
youtubeId field in course.json.

Usage:
    python3 download_videos.py            # download everything missing
    python3 download_videos.py --limit 3  # smoke-test the first 3
    python3 download_videos.py --id Xyz   # download one specific ID
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INV = ROOT / "App" / "Resources" / "Content" / "Videos" / "_inventory.json"
OUT = ROOT / "App" / "Resources" / "Content" / "Videos"
BINARY = "yt-dlp"


def already_have(vid: str) -> Path | None:
    for ext in (".mp4", ".mkv", ".webm"):
        p = OUT / f"{vid}{ext}"
        if p.exists() and p.stat().st_size > 100_000:  # >100KB, not a stub
            return p
    return None


def download_one(vid: str) -> bool:
    if existing := already_have(vid):
        print(f"  [skip] {vid}  (already at {existing.name}, {existing.stat().st_size // 1024} KB)")
        return True

    print(f"  [get ] {vid}")
    # 720p ceiling, mp4 container, h264 video, m4a audio when available.
    # Falls back gracefully if a specific format isn't offered.
    cmd = [
        BINARY,
        "-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[height<=720]+ba/b[height<=720]/b",
        "--merge-output-format", "mp4",
        "--remux-video", "mp4",
        "-o", str(OUT / f"{vid}.%(ext)s"),
        "--no-playlist",
        "--no-warnings",
        "--no-progress",
        f"https://www.youtube.com/watch?v={vid}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"  [FAIL] {vid} — timeout after 300s")
        return False

    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip().splitlines()[-1] if (result.stderr or result.stdout) else "unknown error"
        print(f"  [FAIL] {vid} — {err[:120]}")
        return False

    final = OUT / f"{vid}.mp4"
    if not final.exists():
        for ext in (".mkv", ".webm"):
            alt = OUT / f"{vid}{ext}"
            if alt.exists():
                alt.rename(final)
                break
    if final.exists() and final.stat().st_size > 100_000:
        print(f"  [ok  ] {vid}  ({final.stat().st_size // 1024} KB)")
        return True
    print(f"  [FAIL] {vid} — file missing or too small after download")
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="only download the first N")
    parser.add_argument("--id", help="only download a specific video ID")
    args = parser.parse_args()

    if not shutil.which(BINARY):
        print(f"{BINARY} not found. Install with: brew install yt-dlp", file=sys.stderr)
        return 1

    if not INV.exists():
        print(f"Inventory not found: {INV}", file=sys.stderr)
        return 1

    inventory = json.loads(INV.read_text())
    targets = inventory
    if args.id:
        targets = [v for v in inventory if v["id"] == args.id]
        if not targets:
            print(f"{args.id} not in inventory", file=sys.stderr)
            return 1
    if args.limit:
        targets = targets[: args.limit]

    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(targets)} videos to {OUT.relative_to(ROOT)} using {BINARY}")

    ok = fail = skip = 0
    for v in targets:
        if already_have(v["id"]):
            skip += 1
            continue
        if download_one(v["id"]):
            ok += 1
        else:
            fail += 1

    print(f"\nDone. ok={ok}  skip={skip}  fail={fail}  total={len(targets)}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
