import os
from PIL import Image, ImageDraw, ImageFilter

SHIRT_COLORS = {
    "green": {
        "primary": "#10b981",
        "shadow": "#047857",
        "highlight": "#6ee7b7",
        "collar": "#065f46",
        "symbol": "star",
        "symbol_color": "#fef08a"
    },
    "orange": {
        "primary": "#f97316",
        "shadow": "#c2410c",
        "highlight": "#fdba74",
        "collar": "#9a3412",
        "symbol": "bear",
        "symbol_color": "#ffffff"
    },
    "gold": {
        "primary": "#eab308",
        "shadow": "#a16207",
        "highlight": "#fef08a",
        "collar": "#854d0e",
        "symbol": "star",
        "symbol_color": "#ffffff"
    },
    "yellow": {
        "primary": "#facc15",
        "shadow": "#ca8a04",
        "highlight": "#fef9c3",
        "collar": "#a16207",
        "symbol": "sparkle",
        "symbol_color": "#ffffff"
    },
    "blue": {
        "primary": "#38bdf8",
        "shadow": "#0284c7",
        "highlight": "#bae6fd",
        "collar": "#0369a1",
        "symbol": "bear",
        "symbol_color": "#ffffff"
    },
    "navy": {
        "primary": "#3b82f6",
        "shadow": "#1d4ed8",
        "highlight": "#93c5fd",
        "collar": "#1e40af",
        "symbol": "star",
        "symbol_color": "#fde047"
    },
    "pink": {
        "primary": "#ec4899",
        "shadow": "#be185d",
        "highlight": "#fbcfe8",
        "collar": "#9d174d",
        "symbol": "heart",
        "symbol_color": "#ffffff"
    },
    "purple": {
        "primary": "#a855f7",
        "shadow": "#7e22ce",
        "highlight": "#e9d5ff",
        "collar": "#6b21a8",
        "symbol": "star",
        "symbol_color": "#fde047"
    },
    "red": {
        "primary": "#ef4444",
        "shadow": "#b91c1c",
        "highlight": "#fca5a5",
        "collar": "#991b1b",
        "symbol": "sparkle",
        "symbol_color": "#fef08a"
    },
    "white": {
        "primary": "#f8fafc",
        "shadow": "#cbd5e1",
        "highlight": "#ffffff",
        "collar": "#94a3b8",
        "symbol": "bear",
        "symbol_color": "#3b82f6"
    },
    "black": {
        "primary": "#27272a",
        "shadow": "#09090b",
        "highlight": "#52525b",
        "collar": "#18181b",
        "symbol": "star",
        "symbol_color": "#fde047"
    },
    "avoid": {
        "primary": "#7f1d1d",
        "shadow": "#450a0a",
        "highlight": "#f87171",
        "collar": "#450a0a",
        "symbol": "cross",
        "symbol_color": "#ef4444"
    }
}

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_tshirt(color_data, size=256):
    S = 1024
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    p_rgb = hex_to_rgb(color_data["primary"])
    s_rgb = hex_to_rgb(color_data["shadow"])
    h_rgb = hex_to_rgb(color_data["highlight"])
    c_rgb = hex_to_rgb(color_data["collar"])
    sym_rgb = hex_to_rgb(color_data["symbol_color"])

    shirt_pts = [
        (380, 190), (170, 290), (100, 480), (260, 530), (310, 450),
        (290, 860), (512, 885), (734, 860),
        (714, 450), (764, 530), (924, 480), (854, 290), (644, 190)
    ]

    shadow_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    shadow_offset_pts = [(x + 8, y + 25) for (x, y) in shirt_pts]
    s_draw.polygon(shadow_offset_pts, fill=(0, 0, 0, 110))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(28))
    img.alpha_composite(shadow_img)

    draw.polygon(shirt_pts, fill=p_rgb + (255,))

    flank_shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    fs_draw = ImageDraw.Draw(flank_shadow)
    fs_draw.polygon([(290, 450), (360, 450), (340, 860), (290, 860)], fill=s_rgb + (140,))
    fs_draw.polygon([(714, 450), (664, 450), (684, 860), (734, 860)], fill=s_rgb + (140,))
    fs_draw.polygon([(290, 830), (734, 830), (734, 860), (512, 885), (290, 860)], fill=s_rgb + (160,))
    fs_draw.polygon([(100, 450), (260, 500), (260, 530), (100, 480)], fill=s_rgb + (180,))
    fs_draw.polygon([(924, 450), (764, 500), (764, 530), (924, 480)], fill=s_rgb + (180,))
    flank_shadow = flank_shadow.filter(ImageFilter.GaussianBlur(20))
    img.alpha_composite(flank_shadow)

    hl_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(hl_img)
    hl_draw.ellipse([340, 240, 680, 560], fill=h_rgb + (90,))
    hl_draw.polygon([(360, 200), (460, 200), (280, 340), (200, 310)], fill=h_rgb + (120,))
    hl_img = hl_img.filter(ImageFilter.GaussianBlur(32))
    img.alpha_composite(hl_img)

    draw.chord([370, 120, 654, 270], start=0, end=180, fill=c_rgb + (255,))
    draw.chord([395, 115, 629, 235], start=0, end=180, fill=(15, 23, 42, 255))
    draw.arc([385, 130, 639, 260], start=10, end=170, fill=h_rgb + (180,), width=6)
    draw.line(shirt_pts + [shirt_pts[0]], fill=s_rgb + (220,), width=10)

    sym = color_data["symbol"]
    cx, cy = 512, 460
    if sym == "bear":
        draw.ellipse([cx - 75, cy - 65, cx + 75, cy + 65], fill=sym_rgb + (255,))
        draw.ellipse([cx - 85, cy - 85, cx - 45, cy - 45], fill=sym_rgb + (255,))
        draw.ellipse([cx + 45, cy - 85, cx + 85, cy - 45], fill=sym_rgb + (255,))
        draw.ellipse([cx - 75, cy - 75, cx - 55, cy - 55], fill=c_rgb + (200,))
        draw.ellipse([cx + 55, cy - 75, cx + 75, cy - 55], fill=c_rgb + (200,))
        draw.ellipse([cx - 35, cy - 15, cx - 20, cy], fill=(15, 23, 42, 255))
        draw.ellipse([cx + 20, cy - 15, cx + 35, cy], fill=(15, 23, 42, 255))
        draw.ellipse([cx - 28, cy + 2, cx + 28, cy + 42], fill=(241, 245, 249, 255))
        draw.ellipse([cx - 14, cy + 8, cx + 14, cy + 24], fill=(15, 23, 42, 255))
        draw.arc([cx - 16, cy + 18, cx, cy + 34], start=0, end=180, fill=(15, 23, 42, 255), width=4)
        draw.arc([cx, cy + 18, cx + 16, cy + 34], start=0, end=180, fill=(15, 23, 42, 255), width=4)
        draw.ellipse([cx - 60, cy + 8, cx - 40, cy + 24], fill=(244, 114, 182, 180))
        draw.ellipse([cx + 40, cy + 8, cx + 60, cy + 24], fill=(244, 114, 182, 180))
    elif sym == "star":
        import math
        star_pts = []
        r_out, r_in = 75, 34
        for i in range(10):
            r = r_out if i % 2 == 0 else r_in
            ang = math.radians(-90 + i * 36)
            star_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(star_pts, fill=sym_rgb + (255,))
        draw.ellipse([cx - 10, cy - 18, cx - 2, cy - 10], fill=(255, 255, 255, 230))
    elif sym == "heart":
        draw.ellipse([cx - 60, cy - 45, cx + 5, cy + 20], fill=sym_rgb + (255,))
        draw.ellipse([cx - 5, cy - 45, cx + 60, cy + 20], fill=sym_rgb + (255,))
        draw.polygon([(cx - 55, cy - 2), (cx + 55, cy - 2), (cx, cy + 65)], fill=sym_rgb + (255,))
        draw.ellipse([cx - 35, cy - 30, cx - 20, cy - 15], fill=(255, 255, 255, 220))
    elif sym == "sparkle":
        draw.polygon([(cx, cy - 75), (cx + 25, cy), (cx, cy + 75), (cx - 25, cy)], fill=sym_rgb + (255,))
        draw.polygon([(cx - 75, cy), (cx, cy + 25), (cx + 75, cy), (cx - 25, cy)], fill=sym_rgb + (255,))
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 255, 255, 255))
    elif sym == "cross":
        draw.ellipse([cx - 65, cy - 65, cx + 65, cy + 65], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=8)
        draw.line([(cx - 45, cy - 45), (cx + 45, cy + 45)], fill=(255, 255, 255, 255), width=12)

    return img.resize((size, size), Image.Resampling.LANCZOS)

dest_dirs = ["public/shirts", "shirts"]
for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

for key, c_data in SHIRT_COLORS.items():
    s_img = draw_tshirt(c_data, size=256)
    for dest in dest_dirs:
        out_path = os.path.join(dest, f"shirt_{key}.png")
        s_img.save(out_path, format="PNG", optimize=True)
        print(f"Saved {out_path}")
print("ALL DONE")
