#!/usr/bin/env python3
"""Generate the Precalc Prep iOS app icon (1024x1024 PNG).

Design:
- Deep indigo → vibrant blue → soft purple gradient
- Soft sine curves in the background
- Large math-italic "f(x)" centered, using STIX Two Math
- Letter-spaced "PREP" label below
"""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1024

# Font paths on macOS
MATH_FONT = "/System/Library/Fonts/Supplemental/STIXTwoMath.otf"
TEXT_FONT = "/System/Library/Fonts/Supplemental/STIXTwoText.ttf"
FALLBACK = "/System/Library/Fonts/Supplemental/Georgia.ttf"


def make_gradient(size: int, top_color, bottom_color) -> Image.Image:
    base = Image.new("RGB", (1, size), top_color)
    top = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / (size - 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        top.putpixel((0, y), (r, g, b))
    return top.resize((size, size), Image.BILINEAR)


def add_curves(img: Image.Image, color, width: int = 22, opacity: int = 70) -> Image.Image:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for phase, amp, freq, op in [
        (0.0, 0.18, 1.5, opacity),
        (math.pi / 2, 0.10, 1.2, max(40, opacity - 40)),
    ]:
        prev = None
        for x in range(0, w, 4):
            t = x / w
            y = h * 0.62 + math.sin(t * 2 * math.pi * freq + phase) * (h * amp)
            if prev is not None:
                draw.line([prev, (x, y)], fill=(*color, op), width=width)
            prev = (x, y)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=2))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.truetype(FALLBACK, size)


def make_icon() -> Image.Image:
    # Background gradient
    base = make_gradient(
        SIZE,
        top_color=(28, 34, 92),
        bottom_color=(96, 70, 200),
    ).convert("RGBA")

    # Soft curves in the background
    base = add_curves(base, color=(255, 255, 255), width=24, opacity=65)

    # Horizontal highlight band
    band = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for y in range(SIZE // 2 - 120, SIZE // 2 + 120):
        t = abs(y - SIZE // 2) / 120
        alpha = int(40 * (1 - t))
        bd.line([(0, y), (SIZE, y)], fill=(255, 255, 255, alpha), width=1)
    base = Image.alpha_composite(base, band)

    # The main "f(x)" — large, math-italic, centered
    text_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)

    # Big math-italic "f(x)" — fill most of the canvas
    main_font = load_font(MATH_FONT, 540)
    main_text = "f(x)"

    # Measure
    main_bbox = td.textbbox((0, 0), main_text, font=main_font)
    main_w = main_bbox[2] - main_bbox[0]
    main_h = main_bbox[3] - main_bbox[1]

    # Center the math glyph in the upper-mid area of the canvas
    main_x = (SIZE - main_w) // 2 - main_bbox[0]
    main_y = int(SIZE * 0.10) - main_bbox[1]  # ~10% from top

    # "PREP" — letter-spaced, near the bottom
    sub_font = load_font(TEXT_FONT, 110)
    sub_text = "PREP"
    sub_bbox = td.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_h = sub_bbox[3] - sub_bbox[1]
    sub_y = SIZE - 180 - sub_bbox[1]

    # Drop shadow (subtle, since the math glyph is the focus)
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((main_x + 6, main_y + 14), main_text, fill=(0, 0, 0, 110), font=main_font)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    base = Image.alpha_composite(base, shadow)

    # Render the math glyph
    td.text((main_x, main_y), main_text, fill=(255, 255, 255, 255), font=main_font)

    # Render "PREP" with letter spacing, semi-transparent
    letters = list(sub_text)
    spacing = 22
    total_w = sum(
        (td.textbbox((0, 0), L, font=sub_font)[2] - td.textbbox((0, 0), L, font=sub_font)[0]) + spacing
        for L in letters
    ) - spacing
    cur_x = (SIZE - total_w) // 2
    for L in letters:
        lbbox = td.textbbox((0, 0), L, font=sub_font)
        lw = lbbox[2] - lbbox[0]
        td.text((cur_x - lbbox[0], sub_y - lbbox[1]), L, fill=(255, 255, 255, 220), font=sub_font)
        cur_x += lw + spacing

    return Image.alpha_composite(base, text_layer).convert("RGB")


def main():
    icon = make_icon()
    out = "App/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png"
    icon.save(out, "PNG", optimize=True)
    print(f"Saved {out} ({icon.size[0]}x{icon.size[1]})")
    preview = icon.resize((512, 512), Image.LANCZOS)
    preview.save("App/Resources/Assets.xcassets/AppIcon.appiconset/preview-512.png", "PNG", optimize=True)
    print("Saved preview-512.png")


if __name__ == "__main__":
    main()
