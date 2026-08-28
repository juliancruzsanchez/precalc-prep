#!/usr/bin/env python3
"""Generate the Precalc Prep iOS app icon (1024x1024 PNG).

Design:
- Deep indigo → vibrant blue → soft purple gradient
- Soft sine curves in the background
- Centered composition: math-italic f(x) above letter-spaced PREP
- The whole composition is centered as one block in the middle of the canvas
- f(x) uses true math Unicode glyphs (U+1D453, U+1D465) from STIX Two Math
"""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1024

# True math italic characters (U+1D453, U+1D465) from STIX Two Math
MATH_ITALIC_F = "\U0001D453"   # 𝑓
MATH_ITALIC_X = "\U0001D465"   # 𝑥

MATH_FONT = "/System/Library/Fonts/Supplemental/STIXTwoMath.otf"
TEXT_FONT = "/System/Library/Fonts/Supplemental/STIXTwoText.ttf"
FALLBACK = "/System/Library/Fonts/Supplemental/Georgia.ttf"


def make_gradient(size, top_color, bottom_color):
    base = Image.new("RGB", (1, size), top_color)
    top = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / (size - 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        top.putpixel((0, y), (r, g, b))
    return top.resize((size, size), Image.BILINEAR)


def add_curves(img, color, width=22, opacity=55):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for phase, amp, freq, op in [
        (0.0, 0.20, 1.5, opacity),
        (math.pi / 2, 0.11, 1.2, max(35, opacity - 35)),
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


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.truetype(FALLBACK, size)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]


def make_icon():
    base = make_gradient(
        SIZE,
        top_color=(28, 34, 92),
        bottom_color=(96, 70, 200),
    ).convert("RGBA")

    # Subtle background curves
    base = add_curves(base, color=(255, 255, 255), width=22, opacity=55)

    # Subtle highlight band
    band = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for y in range(SIZE // 2 - 140, SIZE // 2 + 140):
        t = abs(y - SIZE // 2) / 140
        alpha = int(35 * (1 - t))
        bd.line([(0, y), (SIZE, y)], fill=(255, 255, 255, alpha), width=1)
    base = Image.alpha_composite(base, band)

    text_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)

    # ─── Render f(x) with math italic glyphs, tight spacing ───
    main_font = load_font(MATH_FONT, 460)

    f_char = MATH_ITALIC_F
    x_char = MATH_ITALIC_X

    fx_off, fy_off, fw, fh = measure(td, f_char, main_font)
    lpar_off, lpar_y, lpar_w, lpar_h = measure(td, "(", main_font)
    xx_off, xy_off, xw, xh = measure(td, x_char, main_font)
    rpar_off, rpar_y, rpar_w, rpar_h = measure(td, ")", main_font)

    # Tight inner gaps: f( x ) — minimal whitespace, no excess
    gap = 10             # between f and (
    inner_gap = 30       # between ( and x, x and )
    f_x_w = fw + gap
    parens_w = lpar_w + inner_gap + xw + inner_gap + rpar_w
    f_x_w_total = f_x_w + parens_w
    start_x = (SIZE - f_x_w_total) // 2

    f_x = start_x
    lpar_x = f_x + fw + gap
    x_x = lpar_x + lpar_w + inner_gap
    rpar_x = x_x + xw + inner_gap

    # Vertical: put f(x) in the middle-upper area
    glyph_h = max(fh, lpar_h, xh, rpar_h)
    f_x_y_top = int(SIZE * 0.18)

    # ─── Render PREP, letter-spaced, below f(x) ───
    sub_font = load_font(TEXT_FONT, 120)
    sub_text = "PREP"
    sub_bbox = td.textbbox((0, 0), sub_text, font=sub_font)
    sub_h = sub_bbox[3] - sub_bbox[1]

    # Gap between f(x) and PREP
    gap_between = 90
    f_x_bottom = f_x_y_top + glyph_h
    prep_y_top = f_x_bottom + gap_between

    # Letter-spaced PREP width
    letters = list(sub_text)
    spacing = 22
    prep_total_w = sum(
        (td.textbbox((0, 0), L, font=sub_font)[2] - td.textbbox((0, 0), L, font=sub_font)[0]) + spacing
        for L in letters
    ) - spacing
    prep_start_x = (SIZE - prep_total_w) // 2

    # ─── Drop shadow for the whole composition ───
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((f_x - fx_off + 6, f_x_y_top - fy_off + 12), f_char, fill=(0, 0, 0, 110), font=main_font)
    sd.text((lpar_x - lpar_off + 6, f_x_y_top - lpar_y + 12), "(", fill=(0, 0, 0, 110), font=main_font)
    sd.text((x_x - xx_off + 6, f_x_y_top - xy_off + 12), x_char, fill=(0, 0, 0, 110), font=main_font)
    sd.text((rpar_x - rpar_off + 6, f_x_y_top - rpar_y + 12), ")", fill=(0, 0, 0, 110), font=main_font)
    cur_x = prep_start_x
    for L in letters:
        lbbox = sd.textbbox((0, 0), L, font=sub_font)
        lw = lbbox[2] - lbbox[0]
        sd.text((cur_x - lbbox[0] + 3, prep_y_top - lbbox[1] + 4), L, fill=(0, 0, 0, 90), font=sub_font)
        cur_x += lw + spacing
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=11))
    base = Image.alpha_composite(base, shadow)

    # ─── Render the math glyph (f ( x ) in proper math italic) ───
    td.text((f_x - fx_off, f_x_y_top - fy_off), f_char, fill=(255, 255, 255, 255), font=main_font)
    td.text((lpar_x - lpar_off, f_x_y_top - lpar_y), "(", fill=(255, 255, 255, 255), font=main_font)
    td.text((x_x - xx_off, f_x_y_top - xy_off), x_char, fill=(255, 255, 255, 255), font=main_font)
    td.text((rpar_x - rpar_off, f_x_y_top - rpar_y), ")", fill=(255, 255, 255, 255), font=main_font)

    # ─── Render PREP ───
    cur_x = prep_start_x
    for L in letters:
        lbbox = td.textbbox((0, 0), L, font=sub_font)
        lw = lbbox[2] - lbbox[0]
        td.text((cur_x - lbbox[0], prep_y_top - lbbox[1]), L, fill=(255, 255, 255, 230), font=sub_font)
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
