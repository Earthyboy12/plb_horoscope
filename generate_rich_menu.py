#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate high-resolution (2500x1686) LINE OA Rich Menu Image
Dark Cosmic & Luxury Gold Theme matching PLB Astrology web app.
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 2500
HEIGHT = 1686

def create_rich_menu_image(output_path="rich_menu.png"):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (7, 10, 19, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = "C:/Windows/Fonts/tahomabd.ttf"
    font_path_regular = "C:/Windows/Fonts/tahoma.ttf"
    
    try:
        font_title = ImageFont.truetype(font_path_bold, 84)
        font_sub = ImageFont.truetype(font_path_regular, 44)
        font_badge = ImageFont.truetype(font_path_bold, 36)
        font_center = ImageFont.truetype(font_path_bold, 38)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
        font_center = font_title

    # 4 Quadrants bounds
    # Top-Left: (0, 0, 1250, 843)
    # Top-Right: (1250, 0, 2500, 843)
    # Bottom-Left: (0, 843, 1250, 1686)
    # Bottom-Right: (1250, 843, 2500, 1686)
    
    quadrants = [
        {
            "rect": (30, 30, 1235, 828),
            "bg_color": (15, 23, 42, 255),
            "border_color": (245, 158, 11, 180),
            "accent_color": (245, 158, 11),
            "tag": "เมนูยอดนิยม",
            "title": "สรุปดวงประจำวัน",
            "subtitle": "วิเคราะห์ลัคนาราศี • คะแนน 4 ด้าน • สี/เลขมงคล",
            "action_hint": "แตะเพื่อดูดวงวันนี้ ⚡"
        },
        {
            "rect": (1265, 30, 2470, 828),
            "bg_color": (15, 23, 42, 255),
            "border_color": (59, 130, 246, 180),
            "accent_color": (96, 165, 250),
            "tag": "เจาะลึก 5 หมวด",
            "title": "เลือกหมวดดูดวง",
            "subtitle": "การงาน • การเงิน • ความรัก • สุขภาพ • ผัง 12 ช่อง",
            "action_hint": "แตะเลือกหมวดที่สนใจ 🔮"
        },
        {
            "rect": (30, 858, 1235, 1656),
            "bg_color": (26, 15, 60, 255),
            "border_color": (168, 85, 247, 180),
            "accent_color": (192, 132, 252),
            "tag": "คะแนนความแม่น",
            "title": "ให้ Feedback 5 ดาว",
            "subtitle": "ให้คะแนนแม่หมอ • เขียนคอมเมนต์ติชมแนะนำ",
            "action_hint": "แตะเพื่อร่วมประเมิน ⭐"
        },
        {
            "rect": (1265, 858, 2470, 1656),
            "bg_color": (15, 23, 42, 255),
            "border_color": (234, 179, 8, 180),
            "accent_color": (251, 191, 36),
            "tag": "สมทบทุนเซิร์ฟเวอร์",
            "title": "สนับสนุนแม่หมอ ☕",
            "subtitle": "PromptPay พร้อมเพย์ • สนับสนุนให้เปิดดูดวงฟรี",
            "action_hint": "แตะเพื่อร่วมสนับสนุน 🙏"
        }
    ]

    for q in quadrants:
        x1, y1, x2, y2 = q["rect"]
        # Draw rounded card
        draw.rounded_rectangle([x1, y1, x2, y2], radius=36, fill=q["bg_color"], outline=q["border_color"], width=4)
        
        # Tag Badge
        tag_text = q["tag"]
        tag_bbox = draw.textbbox((0, 0), tag_text, font=font_badge)
        tag_w = tag_bbox[2] - tag_bbox[0] + 36
        tag_h = 56
        tag_x = x1 + 60
        tag_y = y1 + 60
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=28, fill=(30, 41, 59, 255), outline=q["accent_color"], width=2)
        draw.text((tag_x + 18, tag_y + 8), tag_text, font=font_badge, fill=q["accent_color"])

        # Main Title
        title_y = tag_y + 110
        draw.text((x1 + 60, title_y), q["title"], font=font_title, fill=(255, 255, 255))

        # Subtitle
        sub_y = title_y + 120
        draw.text((x1 + 60, sub_y), q["subtitle"], font=font_sub, fill=(148, 163, 184))

        # Bottom Action Bar
        action_y = y2 - 120
        draw.rounded_rectangle([x1 + 60, action_y, x2 - 60, action_y + 68], radius=20, fill=(15, 23, 42, 200), outline=(51, 65, 85, 255), width=2)
        draw.text((x1 + 80, action_y + 12), q["action_hint"], font=font_badge, fill=q["accent_color"])

    # Center Logo Divider Badge
    cx, cy = WIDTH // 2, HEIGHT // 2
    cw, ch = 380, 110
    draw.rounded_rectangle([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], radius=40, fill=(7, 10, 19, 255), outline=(245, 158, 11, 255), width=4)
    logo_text = "PLB โหราศาสตร์"
    draw.text((cx - 150, cy - 24), logo_text, font=font_center, fill=(251, 191, 36))

    # Save image
    img.save(output_path, "PNG")
    print(f"Rich Menu image generated successfully at {output_path}")

if __name__ == "__main__":
    create_rich_menu_image("rich_menu.png")
    create_rich_menu_image("public/rich_menu.png")
