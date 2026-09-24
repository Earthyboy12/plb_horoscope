#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cute Modern Polar Bear Rich Menu Generator (2500x1686) for PLB Astrology LINE OA.
Uses Google Font 'Prompt' (Ultra-Modern Thai Sans-Serif), Vector Icons,
and embeds the Earth PLB Buff Polar Bear Logo in the center.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os

WIDTH = 2500
HEIGHT = 1686
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "public", "logo.jpg")
FONT_BOLD_PATH = os.path.join(BASE_DIR, "Prompt-Bold.ttf")
FONT_MED_PATH = os.path.join(BASE_DIR, "Prompt-Medium.ttf")

def draw_star(draw, cx, cy, r_outer, r_inner, fill, outline=None, width=1):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5.0 - math.pi / 2.0
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline)

def draw_paw_print(draw, cx, cy, size=24, fill=(255, 255, 255)):
    """Draw a cute bear paw print."""
    # Main pad
    pad_r = int(size * 0.6)
    draw.ellipse([cx - pad_r, cy - int(pad_r * 0.5), cx + pad_r, cy + int(pad_r * 0.8)], fill=fill)
    # 4 Toes
    toe_r = int(size * 0.28)
    toe_offsets = [(-int(size * 0.65), -int(size * 0.6)), 
                   (-int(size * 0.22), -int(size * 0.85)), 
                   (int(size * 0.22), -int(size * 0.85)), 
                   (int(size * 0.65), -int(size * 0.6))]
    for ox, oy in toe_offsets:
        draw.ellipse([cx + ox - toe_r, cy + oy - toe_r, cx + ox + toe_r, cy + oy + toe_r], fill=fill)

def draw_polar_bear_face(draw, cx, cy, size=180, accessory="star"):
    """Draw an adorable fluffy polar bear with rosy cheeks."""
    # Ears
    ear_r = int(size * 0.32)
    ear_offset_x = int(size * 0.65)
    ear_offset_y = int(size * 0.60)
    
    # Left Ear
    draw.ellipse([cx - ear_offset_x - ear_r, cy - ear_offset_y - ear_r, 
                  cx - ear_offset_x + ear_r, cy - ear_offset_y + ear_r], fill=(255, 255, 255), outline=(203, 213, 225), width=5)
    draw.ellipse([cx - ear_offset_x - int(ear_r*0.6), cy - ear_offset_y - int(ear_r*0.6), 
                  cx - ear_offset_x + int(ear_r*0.6), cy - ear_offset_y + int(ear_r*0.6)], fill=(254, 205, 211))
    
    # Right Ear
    draw.ellipse([cx + ear_offset_x - ear_r, cy - ear_offset_y - ear_r, 
                  cx + ear_offset_x + ear_r, cy - ear_offset_y + ear_r], fill=(255, 255, 255), outline=(203, 213, 225), width=5)
    draw.ellipse([cx + ear_offset_x - int(ear_r*0.6), cy - ear_offset_y - int(ear_r*0.6), 
                  cx + ear_offset_x + int(ear_r*0.6), cy - ear_offset_y + int(ear_r*0.6)], fill=(254, 205, 211))

    # Head
    head_rx = int(size * 0.88)
    head_ry = int(size * 0.82)
    draw.ellipse([cx - head_rx, cy - head_ry, cx + head_rx, cy + head_ry], fill=(255, 255, 255), outline=(203, 213, 225), width=5)

    # Rosy Blush Cheeks
    blush_rx = int(size * 0.22)
    blush_ry = int(size * 0.14)
    draw.ellipse([cx - int(size*0.58) - blush_rx, cy + int(size*0.12) - blush_ry,
                  cx - int(size*0.58) + blush_rx, cy + int(size*0.12) + blush_ry], fill=(254, 205, 211))
    draw.ellipse([cx + int(size*0.58) - blush_rx, cy + int(size*0.12) - blush_ry,
                  cx + int(size*0.58) + blush_rx, cy + int(size*0.12) + blush_ry], fill=(254, 205, 211))

    # Big Sparkling Button Eyes
    eye_r = int(size * 0.11)
    eye_x = int(size * 0.38)
    eye_y = int(size * 0.05)
    
    # Left eye
    draw.ellipse([cx - eye_x - eye_r, cy - eye_y - eye_r, cx - eye_x + eye_r, cy - eye_y + eye_r], fill=(15, 23, 42))
    draw.ellipse([cx - eye_x - int(eye_r*0.6), cy - eye_y - int(eye_r*0.6), 
                  cx - eye_x - int(eye_r*0.1), cy - eye_y - int(eye_r*0.1)], fill=(255, 255, 255))
    
    # Right eye
    draw.ellipse([cx + eye_x - eye_r, cy - eye_y - eye_r, cx + eye_x + eye_r, cy - eye_y + eye_r], fill=(15, 23, 42))
    draw.ellipse([cx + eye_x - int(eye_r*0.6), cy - eye_y - int(eye_r*0.6), 
                  cx + eye_x - int(eye_r*0.1), cy - eye_y - int(eye_r*0.1)], fill=(255, 255, 255))

    # Snout
    snout_rx = int(size * 0.38)
    snout_ry = int(size * 0.28)
    snout_y = cy + int(size * 0.24)
    draw.ellipse([cx - snout_rx, snout_y - snout_ry, cx + snout_rx, snout_y + snout_ry], fill=(241, 245, 249), outline=(226, 232, 240), width=3)

    # Black Nose
    nose_rx = int(size * 0.15)
    nose_ry = int(size * 0.10)
    nose_y = snout_y - int(size * 0.08)
    draw.ellipse([cx - nose_rx, nose_y - nose_ry, cx + nose_rx, nose_y + nose_ry], fill=(15, 23, 42))

    # Happy Smile
    mouth_y = nose_y + int(size * 0.12)
    draw.arc([cx - int(size*0.14), mouth_y - int(size*0.06), cx, mouth_y + int(size*0.12)], start=20, end=160, fill=(30, 41, 59), width=5)
    draw.arc([cx, mouth_y - int(size*0.06), cx + int(size*0.14), mouth_y + int(size*0.12)], start=20, end=160, fill=(30, 41, 59), width=5)

    # Accessories
    if accessory == "star":
        # Wizard star hat
        draw.polygon([(cx, cy - int(size*1.35)), (cx - int(size*0.55), cy - int(size*0.65)), (cx + int(size*0.55), cy - int(size*0.65))], fill=(124, 58, 237))
        draw_star(draw, cx, cy - int(size*0.95), int(size*0.18), int(size*0.09), fill=(251, 191, 36))
        draw.ellipse([cx - int(size*0.65), cy - int(size*0.72), cx + int(size*0.65), cy - int(size*0.58)], fill=(167, 139, 250))
    elif accessory == "crystal":
        # Glowing Crystal Ball
        ball_r = int(size * 0.36)
        ball_y = cy + int(size * 0.65)
        draw.ellipse([cx - ball_r, ball_y - ball_r, cx + ball_r, ball_y + ball_r], fill=(99, 102, 241), outline=(199, 210, 254), width=6)
        draw.ellipse([cx - int(ball_r*0.6), ball_y - int(ball_r*0.6), cx - int(ball_r*0.2), ball_y - int(ball_r*0.2)], fill=(255, 255, 255))
    elif accessory == "rating":
        # 5-Star Golden Badge
        star_y = cy + int(size * 0.65)
        draw_star(draw, cx, star_y, int(size*0.44), int(size*0.22), fill=(251, 191, 36), outline=(245, 158, 11), width=3)
    elif accessory == "coffee":
        # Hot coffee cup with steam
        cup_y = cy + int(size * 0.65)
        cup_w = int(size * 0.32)
        cup_h = int(size * 0.28)
        draw.rounded_rectangle([cx - cup_w, cup_y - cup_h//2, cx + cup_w, cup_y + cup_h//2], radius=16, fill=(244, 63, 94))
        # Handle
        draw.arc([cx + cup_w - 6, cup_y - cup_h//3, cx + cup_w + 28, cup_y + cup_h//3], start=270, end=90, fill=(244, 63, 94), width=7)
        # Steam Heart / Star
        draw_star(draw, cx, cup_y - int(size*0.30), int(size*0.14), int(size*0.07), fill=(254, 205, 211))

def generate_cute_polar_rich_menu(output_path="rich_menu.png"):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 15, 30, 255))
    draw = ImageDraw.Draw(img)

    # Use Modern Google Font 'Prompt'
    if os.path.exists(FONT_BOLD_PATH):
        font_super_title = ImageFont.truetype(FONT_BOLD_PATH, 115)
        font_sub = ImageFont.truetype(FONT_MED_PATH, 48)
        font_pill = ImageFont.truetype(FONT_BOLD_PATH, 42)
        font_btn = ImageFont.truetype(FONT_BOLD_PATH, 42)
        font_center_title = ImageFont.truetype(FONT_BOLD_PATH, 42)
        font_center_sub = ImageFont.truetype(FONT_MED_PATH, 28)
    else:
        # Fallback
        font_super_title = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 110)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 46)
        font_pill = font_super_title
        font_btn = font_super_title
        font_center_title = font_super_title
        font_center_sub = font_sub

    # 4 Quadrants configuration with NO raw unicode emojis in text strings!
    cards = [
        {
            "rect": (35, 35, 1230, 823),
            "bg": (17, 24, 48, 255),
            "border": (251, 191, 36, 230),
            "tag_text": "ส่องดวงชะตา",
            "tag_color": (251, 191, 36),
            "tag_icon": "star",
            "title": "สรุปดวงวันนี้",
            "sub": "ลัคนา • 4 มิติชีวิต • เลขมงคล",
            "btn_text": "แตะเปิดดวงวันนี้",
            "bear_type": "star"
        },
        {
            "rect": (1270, 35, 2465, 823),
            "bg": (20, 28, 58, 255),
            "border": (96, 165, 250, 230),
            "tag_text": "ลูกแก้ววิเศษ",
            "tag_color": (96, 165, 250),
            "tag_icon": "crystal",
            "title": "เลือกหมวดดูดวง",
            "sub": "งาน • เงิน • ความรัก • สุขภาพ",
            "btn_text": "แตะเลือกหมวดดวง",
            "bear_type": "crystal"
        },
        {
            "rect": (35, 863, 1230, 1651),
            "bg": (32, 20, 68, 255),
            "border": (216, 180, 254, 230),
            "tag_text": "แม่นแค่ไหน",
            "tag_color": (216, 180, 254),
            "tag_icon": "heart",
            "title": "ให้ Feedback 5 ดาว",
            "sub": "ประเมินความแม่น • ติชมแม่หมอ",
            "btn_text": "แตะร่วมประเมินผล",
            "bear_type": "rating"
        },
        {
            "rect": (1270, 863, 2465, 1651),
            "bg": (38, 24, 45, 255),
            "border": (251, 146, 60, 230),
            "tag_text": "สมทบทุนเซิร์ฟเวอร์",
            "tag_color": (251, 146, 60),
            "tag_icon": "coffee",
            "title": "สนับสนุนแม่หมอ",
            "sub": "เลี้ยงกาแฟน้องหมี • PromptPay",
            "btn_text": "แตะร่วมสนับสนุน",
            "bear_type": "coffee"
        }
    ]

    for c in cards:
        x1, y1, x2, y2 = c["rect"]
        # Card Body
        draw.rounded_rectangle([x1, y1, x2, y2], radius=44, fill=c["bg"], outline=c["border"], width=6)

        # Star sparkles in card corners
        draw_star(draw, x2 - 70, y1 + 70, 18, 8, fill=(255, 255, 255, 190))
        draw_star(draw, x2 - 130, y1 + 100, 12, 5, fill=(255, 255, 255, 140))

        # Tag Badge (Pill) with vector icon inside
        tag_text = c["tag_text"]
        tag_bbox = draw.textbbox((0, 0), tag_text, font=font_pill)
        text_w = tag_bbox[2] - tag_bbox[0]
        pill_w = text_w + 90
        pill_h = 66
        pill_x = x1 + 60
        pill_y = y1 + 55
        draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=33, fill=(15, 23, 42, 230), outline=c["tag_color"], width=3)
        
        # Draw vector icon inside pill
        icon_cx = pill_x + 36
        icon_cy = pill_y + pill_h // 2
        if c["tag_icon"] == "star":
            draw_star(draw, icon_cx, icon_cy, 16, 8, fill=c["tag_color"])
        elif c["tag_icon"] == "crystal":
            draw.ellipse([icon_cx - 14, icon_cy - 14, icon_cx + 14, icon_cy + 14], fill=c["tag_color"])
            draw.ellipse([icon_cx - 8, icon_cy - 8, icon_cx - 2, icon_cy - 2], fill=(255, 255, 255))
        elif c["tag_icon"] == "heart":
            draw.ellipse([icon_cx - 10, icon_cy - 12, icon_cx, icon_cy], fill=c["tag_color"])
            draw.ellipse([icon_cx, icon_cy - 12, icon_cx + 10, icon_cy], fill=c["tag_color"])
            draw.polygon([(icon_cx - 10, icon_cy - 4), (icon_cx + 10, icon_cy - 4), (icon_cx, icon_cy + 10)], fill=c["tag_color"])
        elif c["tag_icon"] == "coffee":
            draw.rounded_rectangle([icon_cx - 12, icon_cy - 10, icon_cx + 8, icon_cy + 10], radius=4, fill=c["tag_color"])
            draw.arc([icon_cx + 4, icon_cy - 6, icon_cx + 16, icon_cy + 6], start=270, end=90, fill=c["tag_color"], width=3)

        # Text inside pill
        draw.text((pill_x + 65, pill_y + 8), tag_text, font=font_pill, fill=c["tag_color"])

        # Main Title (BIG, MODERN, BOLD)
        draw.text((x1 + 60, y1 + 155), c["title"], font=font_super_title, fill=(255, 255, 255))

        # Subtitle (Readable & Clear)
        draw.text((x1 + 65, y1 + 300), c["sub"], font=font_sub, fill=(203, 213, 225))

        # Bottom Button Pill with paw print icon
        btn_y = y2 - 120
        btn_w = 480
        btn_h = 76
        draw.rounded_rectangle([x1 + 60, btn_y, x1 + 60 + btn_w, btn_y + btn_h], radius=26, fill=(15, 23, 42, 240), outline=c["border"], width=3)
        draw_paw_print(draw, x1 + 100, btn_y + btn_h // 2, size=16, fill=c["tag_color"])
        draw.text((x1 + 130, btn_y + 12), c["btn_text"], font=font_btn, fill=(255, 255, 255))

        # Fluffy Polar Bear Character Illustration on the right
        bear_cx = x2 - 250
        bear_cy = y1 + 420
        draw_polar_bear_face(draw, bear_cx, bear_cy, size=175, accessory=c["bear_type"])

    # Center Badge: Embed the Earth PLB Buff Polar Bear Logo!
    cx, cy = WIDTH // 2, HEIGHT // 2
    cw, ch = 520, 160
    draw.rounded_rectangle([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], radius=50, fill=(10, 15, 30, 255), outline=(251, 191, 36, 255), width=6)

    # Insert Circular Buff Bear Avatar from logo.jpg if available
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
            avatar_size = 120
            logo_img = logo_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
            
            # Mask to circle
            mask = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
            
            avatar_x = cx - cw//2 + 25
            avatar_y = cy - avatar_size // 2
            img.paste(logo_img, (avatar_x, avatar_y), mask)
            draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size], outline=(251, 191, 36), width=4)
            
            text_start_x = avatar_x + avatar_size + 20
        except Exception as le:
            print(f"Logo load warning: {le}")
            text_start_x = cx - 180
    else:
        text_start_x = cx - 180

    draw.text((text_start_x, cy - 44), "PLB หมีดูดวง", font=font_center_title, fill=(254, 240, 138))
    draw.text((text_start_x, cy + 12), "โหราศาสตร์ไทยชั้นสูง", font=font_center_sub, fill=(148, 163, 184))

    img.save(output_path, "PNG")
    print(f"Modern Cute Polar Bear Rich Menu generated: {output_path}")

if __name__ == "__main__":
    generate_cute_polar_rich_menu("rich_menu.png")
    generate_cute_polar_rich_menu("public/rich_menu.png")
