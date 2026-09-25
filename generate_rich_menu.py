#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
World-Class 3D Pixar-Style Polar Bear Rich Menu Generator (2500x1686) for PLB Astrology LINE OA.
Uses Google Font 'Prompt' (Ultra-Modern Thai Sans-Serif), 3D rendered character avatars,
glowing ambient glassmorphism cards, and Apple/Pixar aesthetics.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

WIDTH = 2500
HEIGHT = 1686
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD_PATH = os.path.join(BASE_DIR, "Prompt-Bold.ttf")
FONT_MED_PATH = os.path.join(BASE_DIR, "Prompt-Medium.ttf")
ASSETS_DIR = os.path.join(BASE_DIR, "public", "rich_menu_assets")

def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5.0 - math.pi / 2.0
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def generate_cute_polar_rich_menu(output_path="rich_menu.png"):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (6, 9, 20, 255))
    draw = ImageDraw.Draw(img)

    # Use Modern Google Font 'Prompt'
    if os.path.exists(FONT_BOLD_PATH):
        font_title = ImageFont.truetype(FONT_BOLD_PATH, 68)
        font_sub = ImageFont.truetype(FONT_MED_PATH, 32)
        font_pill = ImageFont.truetype(FONT_BOLD_PATH, 30)
        font_btn = ImageFont.truetype(FONT_BOLD_PATH, 32)
    else:
        font_title = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 66)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 30)
        font_pill = font_title
        font_btn = font_title

    # Background subtle cosmic stardust
    random.seed(42)
    for _ in range(200):
        sx = random.randint(0, WIDTH)
        sy = random.randint(0, HEIGHT)
        sr = random.randint(1, 3)
        alpha = random.randint(50, 180)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, alpha))

    # 6 Grid Cards (3 columns x 2 rows)
    cards = [
        # ROW 1
        {
            "rect": (30, 30, 826, 828),
            "bg": (16, 22, 44, 250),
            "border": (251, 191, 36, 230),
            "tag_text": "ส่องดวงชะตา",
            "tag_color": (251, 191, 36),
            "tag_icon": "⭐",
            "title": "สรุปดวงวันนี้",
            "sub": "ลัคนา • 4 มิติชีวิต • เลขมงคล",
            "btn_text": "แตะเปิดดวงวันนี้ ›",
            "asset": "card_1_summary.jpg"
        },
        {
            "rect": (848, 30, 1652, 828),
            "bg": (14, 26, 50, 250),
            "border": (56, 189, 248, 230),
            "tag_text": "4 มิติชีวิต",
            "tag_color": (56, 189, 248),
            "tag_icon": "🔮",
            "title": "เลือกหมวดดวง",
            "sub": "งาน • เงิน • ความรัก • สุขภาพ",
            "btn_text": "แตะเลือกหมวดดวง ›",
            "asset": "card_2_category.jpg"
        },
        {
            "rect": (1674, 30, 2470, 828),
            "bg": (14, 32, 40, 250),
            "border": (52, 211, 153, 230),
            "tag_text": "สถิติวาสนา",
            "tag_color": (52, 211, 153),
            "tag_icon": "👑",
            "title": "เรียกดูสถิติ",
            "sub": "คลื่นดวง 7 วัน • ยศ 7 ระดับ",
            "btn_text": "แตะตรวจเช็กสถิติ ›",
            "asset": "card_3_stats.jpg"
        },
        # ROW 2
        {
            "rect": (30, 856, 826, 1656),
            "bg": (34, 18, 42, 250),
            "border": (244, 114, 182, 230),
            "tag_text": "ชวนเพื่อนมู",
            "tag_color": (244, 114, 182),
            "tag_icon": "💖",
            "title": "แชร์ให้เพื่อน",
            "sub": "ส่งต่อดวงดี • สะสมแต้มบุญ",
            "btn_text": "แตะชวนเพื่อนแอด ›",
            "asset": "card_4_share.jpg"
        },
        {
            "rect": (848, 856, 1652, 1656),
            "bg": (42, 16, 26, 250),
            "border": (248, 113, 113, 230),
            "tag_text": "28 ใบมงคล",
            "tag_color": (248, 113, 113),
            "tag_icon": "🥠",
            "title": "เสี่ยงเซียมซี",
            "sub": "เขย่าลุ้นดวง • เซียมซีโบราณ",
            "btn_text": "แตะเขย่าเซียมซี ›",
            "asset": "card_5_siamsee.jpg"
        },
        {
            "rect": (1674, 856, 2470, 1656),
            "bg": (36, 24, 18, 250),
            "border": (251, 146, 60, 230),
            "tag_text": "บำรุงเซิร์ฟเวอร์",
            "tag_color": (251, 146, 60),
            "tag_icon": "☕",
            "title": "สนับสนุนแม่หมอ",
            "sub": "เลี้ยงกาแฟน้องหมี • PromptPay",
            "btn_text": "แตะสแกน QR โอนเงิน ›",
            "asset": "card_6_support.jpg"
        }
    ]

    for c in cards:
        x1, y1, x2, y2 = c["rect"]
        # Outer glow and rounded glassmorphism card
        draw.rounded_rectangle([x1, y1, x2, y2], radius=40, fill=c["bg"], outline=c["border"], width=5)
        
        # Corner star sparkle
        draw_star(draw, x2 - 45, y1 + 45, 12, 5, fill=(255, 255, 255, 180))

        # Pill Tag
        tag_str = f"{c['tag_icon']} {c['tag_text']}"
        tb = draw.textbbox((0, 0), tag_str, font=font_pill)
        pw = (tb[2] - tb[0]) + 40
        ph = 52
        px = x1 + 42
        py = y1 + 42
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=26, fill=(10, 15, 30, 220), outline=c["tag_color"], width=3)
        draw.text((px + 20, py + 8), tag_str, font=font_pill, fill=c["tag_color"])

        # Main Title (BIG, MODERN, BOLD)
        draw.text((x1 + 42, y1 + 130), c["title"], font=font_title, fill=(255, 255, 255))

        # Subtitle (Readable & Clear)
        draw.text((x1 + 44, y1 + 242), c["sub"], font=font_sub, fill=(203, 213, 225))

        # Bottom Button Pill
        by = y2 - 105
        bw = 430
        bh = 66
        draw.rounded_rectangle([x1 + 42, by, x1 + 42 + bw, by + bh], radius=22, fill=(10, 15, 30, 240), outline=c["border"], width=3)
        draw.text((x1 + 65, by + 12), c["btn_text"], font=font_btn, fill=(255, 255, 255))

        # 3D Bear Asset Medallion on the right side
        asset_path = os.path.join(ASSETS_DIR, c["asset"])
        if os.path.exists(asset_path):
            raw = Image.open(asset_path).convert("RGBA")
            med_size = 350
            raw = raw.resize((med_size, med_size), Image.Resampling.LANCZOS)
            
            # High quality circular anti-aliased mask (2x supersampled)
            m_hi = Image.new("L", (med_size * 2, med_size * 2), 0)
            m_draw = ImageDraw.Draw(m_hi)
            m_draw.ellipse([0, 0, med_size * 2, med_size * 2], fill=255)
            mask = m_hi.resize((med_size, med_size), Image.Resampling.LANCZOS)
            
            mx = x2 - med_size - 28
            my = y1 + (y2 - y1 - med_size) // 2 - 5
            
            # Outer luminous halo ring
            draw.ellipse([mx - 6, my - 6, mx + med_size + 6, my + med_size + 6], outline=c["border"], width=6)
            
            img.paste(raw, (mx, my), mask)

    img.save(output_path, "PNG")
    # Also save optimized JPEG under 1MB for LINE API upload
    jpg_path = os.path.splitext(output_path)[0] + ".jpg"
    rgb_img = img.convert("RGB")
    rgb_img.save(jpg_path, "JPEG", quality=94, optimize=True)
    print(f"Modern Cute 3D Polar Bear Rich Menu generated: {output_path} and {jpg_path}")

if __name__ == "__main__":
    generate_cute_polar_rich_menu("rich_menu.png")
    generate_cute_polar_rich_menu("public/rich_menu.png")
