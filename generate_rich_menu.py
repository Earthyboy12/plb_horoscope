#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cute Polar Bear Rich Menu Generator (2500x1686) for PLB Astrology LINE OA.
Theme: หมีขั้วโลกน่ารัก & ดวงดาวอาร์กติก (Cute Arctic Polar Bear Theme)
"""

from PIL import Image, ImageDraw, ImageFont
import math

WIDTH = 2500
HEIGHT = 1686

def draw_star(draw, cx, cy, r_outer, r_inner, fill, outline=None):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5.0 - math.pi / 2.0
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline)

def draw_polar_bear_face(draw, cx, cy, size=180, accessory="star"):
    """
    Draw a cute fluffy polar bear with blush cheeks and specific accessory.
    """
    # Ears
    ear_r = int(size * 0.32)
    ear_offset_x = int(size * 0.65)
    ear_offset_y = int(size * 0.60)
    
    # Left Ear
    draw.ellipse([cx - ear_offset_x - ear_r, cy - ear_offset_y - ear_r, 
                  cx - ear_offset_x + ear_r, cy - ear_offset_y + ear_r], fill=(255, 255, 255), outline=(203, 213, 225), width=4)
    draw.ellipse([cx - ear_offset_x - int(ear_r*0.6), cy - ear_offset_y - int(ear_r*0.6), 
                  cx - ear_offset_x + int(ear_r*0.6), cy - ear_offset_y + int(ear_r*0.6)], fill=(253, 205, 211))
    
    # Right Ear
    draw.ellipse([cx + ear_offset_x - ear_r, cy - ear_offset_y - ear_r, 
                  cx + ear_offset_x + ear_r, cy - ear_offset_y + ear_r], fill=(255, 255, 255), outline=(203, 213, 225), width=4)
    draw.ellipse([cx + ear_offset_x - int(ear_r*0.6), cy - ear_offset_y - int(ear_r*0.6), 
                  cx + ear_offset_x + int(ear_r*0.6), cy - ear_offset_y + int(ear_r*0.6)], fill=(253, 205, 211))

    # Head
    head_rx = int(size * 0.88)
    head_ry = int(size * 0.82)
    draw.ellipse([cx - head_rx, cy - head_ry, cx + head_rx, cy + head_ry], fill=(255, 255, 255), outline=(203, 213, 225), width=5)

    # Cute Blush Cheeks
    blush_rx = int(size * 0.22)
    blush_ry = int(size * 0.14)
    draw.ellipse([cx - int(size*0.58) - blush_rx, cy + int(size*0.12) - blush_ry,
                  cx - int(size*0.58) + blush_rx, cy + int(size*0.12) + blush_ry], fill=(254, 205, 211))
    draw.ellipse([cx + int(size*0.58) - blush_rx, cy + int(size*0.12) - blush_ry,
                  cx + int(size*0.58) + blush_rx, cy + int(size*0.12) + blush_ry], fill=(254, 205, 211))

    # Eyes (big sparkling button eyes)
    eye_r = int(size * 0.11)
    eye_x = int(size * 0.38)
    eye_y = int(size * 0.05)
    
    # Left eye
    draw.ellipse([cx - eye_x - eye_r, cy - eye_y - eye_r, cx - eye_x + eye_r, cy - eye_y + eye_r], fill=(30, 41, 59))
    draw.ellipse([cx - eye_x - int(eye_r*0.6), cy - eye_y - int(eye_r*0.6), 
                  cx - eye_x - int(eye_r*0.1), cy - eye_y - int(eye_r*0.1)], fill=(255, 255, 255))
    
    # Right eye
    draw.ellipse([cx + eye_x - eye_r, cy - eye_y - eye_r, cx + eye_x + eye_r, cy - eye_y + eye_r], fill=(30, 41, 59))
    draw.ellipse([cx + eye_x - int(eye_r*0.6), cy - eye_y - int(eye_r*0.6), 
                  cx + eye_x - int(eye_r*0.1), cy - eye_y - int(eye_r*0.1)], fill=(255, 255, 255))

    # Snout
    snout_rx = int(size * 0.38)
    snout_ry = int(size * 0.28)
    snout_y = cy + int(size * 0.24)
    draw.ellipse([cx - snout_rx, snout_y - snout_ry, cx + snout_rx, snout_y + snout_ry], fill=(241, 245, 249), outline=(226, 232, 240), width=3)

    # Cute nose
    nose_rx = int(size * 0.15)
    nose_ry = int(size * 0.10)
    nose_y = snout_y - int(size * 0.08)
    draw.ellipse([cx - nose_rx, nose_y - nose_ry, cx + nose_rx, nose_y + nose_ry], fill=(15, 23, 42))

    # Mouth (smile)
    mouth_y = nose_y + int(size * 0.12)
    draw.arc([cx - int(size*0.14), mouth_y - int(size*0.06), cx, mouth_y + int(size*0.12)], start=20, end=160, fill=(30, 41, 59), width=4)
    draw.arc([cx, mouth_y - int(size*0.06), cx + int(size*0.14), mouth_y + int(size*0.12)], start=20, end=160, fill=(30, 41, 59), width=4)

    # Accessory by quadrant
    if accessory == "star":
        # Wizard star hat
        draw.polygon([(cx, cy - int(size*1.35)), (cx - int(size*0.55), cy - int(size*0.65)), (cx + int(size*0.55), cy - int(size*0.65))], fill=(124, 58, 237))
        draw_star(draw, cx, cy - int(size*0.95), int(size*0.18), int(size*0.09), fill=(251, 191, 36))
        draw.ellipse([cx - int(size*0.65), cy - int(size*0.72), cx + int(size*0.65), cy - int(size*0.58)], fill=(167, 139, 250))
    elif accessory == "crystal":
        # Crystal ball in front
        ball_r = int(size * 0.35)
        ball_y = cy + int(size * 0.65)
        draw.ellipse([cx - ball_r, ball_y - ball_r, cx + ball_r, ball_y + ball_r], fill=(99, 102, 241), outline=(199, 210, 254), width=5)
        draw.ellipse([cx - int(ball_r*0.6), ball_y - int(ball_r*0.6), cx - int(ball_r*0.2), ball_y - int(ball_r*0.2)], fill=(255, 255, 255))
    elif accessory == "rating":
        # Big golden 5-star badge
        star_y = cy + int(size * 0.65)
        draw_star(draw, cx, star_y, int(size*0.42), int(size*0.20), fill=(251, 191, 36), outline=(245, 158, 11))
    elif accessory == "coffee":
        # Hot coffee cup with steam
        cup_y = cy + int(size * 0.65)
        cup_w = int(size * 0.32)
        cup_h = int(size * 0.28)
        draw.rounded_rectangle([cx - cup_w, cup_y - cup_h//2, cx + cup_w, cup_y + cup_h//2], radius=16, fill=(244, 63, 94))
        # Handle
        draw.arc([cx + cup_w - 6, cup_y - cup_h//3, cx + cup_w + 26, cup_y + cup_h//3], start=270, end=90, fill=(244, 63, 94), width=6)
        # Steam heart
        draw_star(draw, cx, cup_y - int(size*0.30), int(size*0.12), int(size*0.06), fill=(254, 205, 211))

def generate_cute_polar_rich_menu(output_path="rich_menu.png"):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 15, 30, 255))
    draw = ImageDraw.Draw(img)

    # Fonts - Tahoma Bold for crisp, large, clear Thai rendering
    font_bold = "C:/Windows/Fonts/tahomabd.ttf"
    font_reg = "C:/Windows/Fonts/tahoma.ttf"

    font_super_title = ImageFont.truetype(font_bold, 110)
    font_sub = ImageFont.truetype(font_bold, 50)
    font_pill = ImageFont.truetype(font_bold, 40)
    font_center_title = ImageFont.truetype(font_bold, 44)
    font_center_sub = ImageFont.truetype(font_bold, 30)

    # 4 Quadrants configuration with cute polar bear theme
    cards = [
        {
            "rect": (35, 35, 1230, 823),
            "bg": (17, 24, 48, 255),
            "border": (251, 191, 36, 230),
            "tag": "⭐ ส่องดวงชะตา",
            "tag_color": (251, 191, 36),
            "title": "สรุปดวงวันนี้",
            "sub": "ลัคนา • 4 มิติชีวิต • เลขมงคล",
            "btn_text": "แตะดูดวงทันที 🐾",
            "bear_type": "star"
        },
        {
            "rect": (1270, 35, 2465, 823),
            "bg": (20, 28, 58, 255),
            "border": (96, 165, 250, 230),
            "tag": "🔮 ลูกแก้ววิเศษ",
            "tag_color": (96, 165, 250),
            "title": "เลือกหมวดดูดวง",
            "sub": "งาน • เงิน • ความรัก • สุขภาพ",
            "btn_text": "แตะเลือกหมวด 🐾",
            "bear_type": "crystal"
        },
        {
            "rect": (35, 863, 1230, 1651),
            "bg": (32, 20, 68, 255),
            "border": (216, 180, 254, 230),
            "tag": "💖 แม่นแค่ไหน",
            "tag_color": (216, 180, 254),
            "title": "ให้ Feedback 5 ดาว",
            "sub": "ประเมินความแม่น • ติชมแม่หมอ",
            "btn_text": "แตะให้คะแนน 🐾",
            "bear_type": "rating"
        },
        {
            "rect": (1270, 863, 2465, 1651),
            "bg": (38, 24, 45, 255),
            "border": (251, 146, 60, 230),
            "tag": "☕ สมทบทุนเซิร์ฟเวอร์",
            "tag_color": (251, 146, 60),
            "title": "สนับสนุนแม่หมอ",
            "sub": "เลี้ยงกาแฟน้องหมี • PromptPay",
            "btn_text": "แตะร่วมสนับสนุน 🐾",
            "bear_type": "coffee"
        }
    ]

    for c in cards:
        x1, y1, x2, y2 = c["rect"]
        # Card Body
        draw.rounded_rectangle([x1, y1, x2, y2], radius=44, fill=c["bg"], outline=c["border"], width=6)

        # Draw decorative stars in card corners
        draw_star(draw, x2 - 70, y1 + 70, 18, 8, fill=(255, 255, 255, 180))
        draw_star(draw, x2 - 130, y1 + 100, 12, 5, fill=(255, 255, 255, 130))

        # Tag Badge (Pill)
        tag_text = c["tag"]
        tag_bbox = draw.textbbox((0, 0), tag_text, font=font_pill)
        tag_w = tag_bbox[2] - tag_bbox[0] + 48
        tag_h = 64
        draw.rounded_rectangle([x1 + 60, y1 + 60, x1 + 60 + tag_w, y1 + 60 + tag_h], radius=32, fill=(15, 23, 42, 220), outline=c["tag_color"], width=3)
        draw.text((x1 + 84, y1 + 70), tag_text, font=font_pill, fill=c["tag_color"])

        # Main Title (BIG & BOLD)
        draw.text((x1 + 60, y1 + 155), c["title"], font=font_super_title, fill=(255, 255, 255))

        # Subtitle (Readable & Clear)
        draw.text((x1 + 65, y1 + 290), c["sub"], font=font_sub, fill=(203, 213, 225))

        # Bottom Button Pill
        btn_y = y2 - 120
        draw.rounded_rectangle([x1 + 60, btn_y, x1 + 480, btn_y + 76], radius=24, fill=(15, 23, 42, 230), outline=c["border"], width=3)
        draw.text((x1 + 88, btn_y + 14), c["btn_text"], font=font_pill, fill=(255, 255, 255))

        # Polar Bear Character Illustration (Right side of each card)
        bear_cx = x2 - 250
        bear_cy = y1 + 420
        draw_polar_bear_face(draw, bear_cx, bear_cy, size=175, accessory=c["bear_type"])

    # Center Badge: Cute Polar Bear Logo
    cx, cy = WIDTH // 2, HEIGHT // 2
    cw, ch = 440, 130
    draw.rounded_rectangle([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], radius=48, fill=(10, 15, 30, 255), outline=(251, 191, 36, 255), width=6)
    
    draw.text((cx - 195, cy - 46), "🐻‍❄️ PLB หมีดูดวง ✨", font=font_center_title, fill=(254, 240, 138))
    draw.text((cx - 150, cy + 12), "โหราศาสตร์ไทยชั้นสูง", font=font_center_sub, fill=(148, 163, 184))

    img.save(output_path, "PNG")
    print(f"Cute Polar Bear Rich Menu generated: {output_path}")

if __name__ == "__main__":
    generate_cute_polar_rich_menu("rich_menu.png")
    generate_cute_polar_rich_menu("public/rich_menu.png")
