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

    # Cute Themed Accessories
    if accessory == "star":
        # Wizard star hat
        draw.polygon([(cx, cy - int(size*1.35)), (cx - int(size*0.55), cy - int(size*0.65)), (cx + int(size*0.55), cy - int(size*0.65))], fill=(124, 58, 237))
        draw_star(draw, cx, cy - int(size*0.95), int(size*0.18), int(size*0.09), fill=(251, 191, 36))
        draw.ellipse([cx - int(size*0.65), cy - int(size*0.72), cx + int(size*0.65), cy - int(size*0.58)], fill=(167, 139, 250))
    elif accessory == "crystal":
        # Glowing Crystal Ball
        ball_r = int(size * 0.36)
        ball_y = cy + int(size * 0.65)
        draw.ellipse([cx - ball_r, ball_y - ball_r, cx + ball_r, ball_y + ball_r], fill=(99, 102, 241), outline=(199, 210, 254), width=5)
        draw.ellipse([cx - int(ball_r*0.6), ball_y - int(ball_r*0.6), cx - int(ball_r*0.2), ball_y - int(ball_r*0.2)], fill=(255, 255, 255))
    elif accessory == "crown":
        # Royal Astrological Crown (Rank 7)
        crown_y = cy - int(size * 0.95)
        crown_w = int(size * 0.55)
        crown_h = int(size * 0.35)
        points = [
            (cx - crown_w, cy - int(size * 0.65)),
            (cx - crown_w, crown_y),
            (cx - crown_w // 2, crown_y + crown_h // 2),
            (cx, crown_y - int(size * 0.15)),
            (cx + crown_w // 2, crown_y + crown_h // 2),
            (cx + crown_w, crown_y),
            (cx + crown_w, cy - int(size * 0.65))
        ]
        draw.polygon(points, fill=(251, 191, 36), outline=(245, 158, 11))
        draw_star(draw, cx, crown_y - int(size * 0.15), 12, 6, fill=(239, 68, 68))
        draw_star(draw, cx - crown_w, crown_y, 8, 4, fill=(59, 130, 246))
        draw_star(draw, cx + crown_w, crown_y, 8, 4, fill=(59, 130, 246))
    elif accessory == "share":
        # Holding glowing heart
        heart_y = cy + int(size * 0.65)
        hr = int(size * 0.20)
        draw.ellipse([cx - hr*2, heart_y - hr, cx, heart_y + hr], fill=(244, 114, 182))
        draw.ellipse([cx, heart_y - hr, cx + hr*2, heart_y + hr], fill=(244, 114, 182))
        draw.polygon([(cx - hr*2, heart_y), (cx + hr*2, heart_y), (cx, heart_y + int(hr*2.0))], fill=(244, 114, 182))
        draw_star(draw, cx, heart_y, 8, 4, fill=(255, 255, 255))
    elif accessory == "rating":
        # 5-Star Golden Badge
        star_y = cy + int(size * 0.65)
        draw_star(draw, cx, star_y, int(size*0.44), int(size*0.22), fill=(251, 191, 36), outline=(245, 158, 11), width=3)
    elif accessory == "siamsee":
        # Bamboo fortune cylinder & sticks
        cyl_y = cy + int(size * 0.62)
        cyl_w = int(size * 0.30)
        cyl_h = int(size * 0.36)
        # Red & gold lucky sticks
        draw.line([cx - int(cyl_w*0.5), cyl_y - cyl_h//2, cx - int(cyl_w*0.7), cyl_y - cyl_h//2 - int(size*0.35)], fill=(239, 68, 68), width=7)
        draw.line([cx, cyl_y - cyl_h//2, cx, cyl_y - cyl_h//2 - int(size*0.42)], fill=(251, 191, 36), width=7)
        draw.line([cx + int(cyl_w*0.5), cyl_y - cyl_h//2, cx + int(cyl_w*0.7), cyl_y - cyl_h//2 - int(size*0.35)], fill=(239, 68, 68), width=7)
        # Bamboo cylinder
        draw.rounded_rectangle([cx - cyl_w, cyl_y - cyl_h//2, cx + cyl_w, cyl_y + cyl_h//2], radius=12, fill=(180, 83, 9), outline=(251, 191, 36), width=4)
        # Gold emblem on cylinder
        draw_star(draw, cx, cyl_y, int(size*0.14), int(size*0.07), fill=(254, 240, 138))
    elif accessory == "coffee":
        # Hot coffee cup with steam
        cup_y = cy + int(size * 0.65)
        cup_w = int(size * 0.32)
        cup_h = int(size * 0.28)
        draw.rounded_rectangle([cx - cup_w, cup_y - cup_h//2, cx + cup_w, cup_y + cup_h//2], radius=14, fill=(244, 63, 94))
        draw.arc([cx + cup_w - 6, cup_y - cup_h//3, cx + cup_w + 24, cup_y + cup_h//3], start=270, end=90, fill=(244, 63, 94), width=6)
        draw_star(draw, cx, cup_y - int(size*0.30), int(size*0.14), int(size*0.07), fill=(254, 205, 211))

def generate_cute_polar_rich_menu(output_path="rich_menu.png"):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 15, 30, 255))
    draw = ImageDraw.Draw(img)

    # Use Modern Google Font 'Prompt'
    if os.path.exists(FONT_BOLD_PATH):
        font_title = ImageFont.truetype(FONT_BOLD_PATH, 74)
        font_sub = ImageFont.truetype(FONT_MED_PATH, 36)
        font_pill = ImageFont.truetype(FONT_BOLD_PATH, 34)
        font_btn = ImageFont.truetype(FONT_BOLD_PATH, 34)
    else:
        font_title = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 70)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 34)
        font_pill = font_title
        font_btn = font_title

    # 6 Grid Cards (3 columns x 2 rows)
    cards = [
        # ROW 1
        {
            "rect": (32, 32, 828, 831),
            "bg": (17, 24, 48, 255),
            "border": (251, 191, 36, 230),
            "tag_text": "ส่องดวงชะตา",
            "tag_color": (251, 191, 36),
            "tag_icon": "star",
            "title": "สรุปดวงวันนี้",
            "sub": "ลัคนา • 4 มิติชีวิต • เลขมงคล",
            "btn_text": "แตะเปิดดวงวันนี้",
            "bear_type": "star",
            "use_logo": True
        },
        {
            "rect": (852, 32, 1648, 831),
            "bg": (20, 28, 58, 255),
            "border": (96, 165, 250, 230),
            "tag_text": "ลูกแก้ววิเศษ",
            "tag_color": (96, 165, 250),
            "tag_icon": "crystal",
            "title": "เลือกหมวดดวง",
            "sub": "งาน • เงิน • ความรัก • สุขภาพ",
            "btn_text": "แตะเลือกหมวดดวง",
            "bear_type": "crystal",
            "use_logo": False
        },
        {
            "rect": (1672, 32, 2468, 831),
            "bg": (26, 20, 54, 255),
            "border": (52, 211, 153, 230),
            "tag_text": "ยศ 7 ระดับ",
            "tag_color": (52, 211, 153),
            "tag_icon": "crown",
            "title": "เรียกดูสถิติ",
            "sub": "คลื่นดวง 7 วัน • สถิติวาสนา",
            "btn_text": "แตะตรวจเช็กสถิติ",
            "bear_type": "crown",
            "use_logo": False
        },
        # ROW 2
        {
            "rect": (32, 855, 828, 1654),
            "bg": (42, 20, 50, 255),
            "border": (244, 114, 182, 230),
            "tag_text": "ชวนเพื่อนมู",
            "tag_color": (244, 114, 182),
            "tag_icon": "heart",
            "title": "แชร์ให้เพื่อน",
            "sub": "ส่งต่อดวงดี • สะสมแต้มบุญ",
            "btn_text": "แตะชวนเพื่อนแอด",
            "bear_type": "share",
            "use_logo": False
        },
        {
            "rect": (852, 855, 1648, 1654),
            "bg": (38, 18, 68, 255),
            "border": (192, 132, 252, 230),
            "tag_text": "28 ใบมงคล",
            "tag_color": (192, 132, 252),
            "tag_icon": "star",
            "title": "เสี่ยงเซียมซี",
            "sub": "เขย่าลุ้นดวง • เซียมซีโบราณ",
            "btn_text": "แตะเขย่าเซียมซี",
            "bear_type": "siamsee",
            "use_logo": False
        },
        {
            "rect": (1672, 855, 2468, 1654),
            "bg": (38, 24, 45, 255),
            "border": (251, 146, 60, 230),
            "tag_text": "บำรุงเซิร์ฟเวอร์",
            "tag_color": (251, 146, 60),
            "tag_icon": "coffee",
            "title": "สนับสนุนแม่หมอ",
            "sub": "เลี้ยงกาแฟน้องหมี • PromptPay",
            "btn_text": "แตะสแกน QR โอนเงิน",
            "bear_type": "coffee",
            "use_logo": False
        }
    ]

    for c in cards:
        x1, y1, x2, y2 = c["rect"]
        # Card Body
        draw.rounded_rectangle([x1, y1, x2, y2], radius=38, fill=c["bg"], outline=c["border"], width=5)

        # Star sparkles in card corners
        draw_star(draw, x2 - 50, y1 + 50, 14, 6, fill=(255, 255, 255, 180))
        draw_star(draw, x2 - 90, y1 + 80, 9, 4, fill=(255, 255, 255, 130))

        # Tag Badge (Pill) with vector icon inside
        tag_text = c["tag_text"]
        tag_bbox = draw.textbbox((0, 0), tag_text, font=font_pill)
        text_w = tag_bbox[2] - tag_bbox[0]
        pill_w = text_w + 75
        pill_h = 56
        pill_x = x1 + 45
        pill_y = y1 + 45
        draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=28, fill=(15, 23, 42, 230), outline=c["tag_color"], width=3)
        
        # Draw vector icon inside pill
        icon_cx = pill_x + 30
        icon_cy = pill_y + pill_h // 2
        if c["tag_icon"] == "star":
            draw_star(draw, icon_cx, icon_cy, 13, 6, fill=c["tag_color"])
        elif c["tag_icon"] == "crystal":
            draw.ellipse([icon_cx - 11, icon_cy - 11, icon_cx + 11, icon_cy + 11], fill=c["tag_color"])
            draw.ellipse([icon_cx - 6, icon_cy - 6, icon_cx - 1, icon_cy - 1], fill=(255, 255, 255))
        elif c["tag_icon"] == "crown":
            draw_star(draw, icon_cx, icon_cy - 2, 13, 6, fill=c["tag_color"])
            draw.ellipse([icon_cx - 10, icon_cy + 6, icon_cx + 10, icon_cy + 10], fill=c["tag_color"])
        elif c["tag_icon"] == "heart":
            draw.ellipse([icon_cx - 8, icon_cy - 9, icon_cx, icon_cy + 1], fill=c["tag_color"])
            draw.ellipse([icon_cx, icon_cy - 9, icon_cx + 8, icon_cy + 1], fill=c["tag_color"])
            draw.polygon([(icon_cx - 8, icon_cy - 2), (icon_cx + 8, icon_cy - 2), (icon_cx, icon_cy + 9)], fill=c["tag_color"])
        elif c["tag_icon"] == "rating":
            draw_star(draw, icon_cx, icon_cy, 13, 6, fill=c["tag_color"])
        elif c["tag_icon"] == "coffee":
            draw.rounded_rectangle([icon_cx - 10, icon_cy - 8, icon_cx + 6, icon_cy + 8], radius=3, fill=c["tag_color"])
            draw.arc([icon_cx + 3, icon_cy - 5, icon_cx + 13, icon_cy + 5], start=270, end=90, fill=c["tag_color"], width=3)

        # Text inside pill
        draw.text((pill_x + 55, pill_y + 8), tag_text, font=font_pill, fill=c["tag_color"])

        # Main Title (BIG, MODERN, BOLD)
        draw.text((x1 + 45, y1 + 130), c["title"], font=font_title, fill=(255, 255, 255))

        # Subtitle (Readable & Clear)
        draw.text((x1 + 48, y1 + 245), c["sub"], font=font_sub, fill=(203, 213, 225))

        # Bottom Button Pill with paw print icon
        btn_y = y2 - 100
        btn_w = 420
        btn_h = 66
        draw.rounded_rectangle([x1 + 45, btn_y, x1 + 45 + btn_w, btn_y + btn_h], radius=22, fill=(15, 23, 42, 240), outline=c["border"], width=3)
        draw_paw_print(draw, x1 + 80, btn_y + btn_h // 2, size=14, fill=c["tag_color"])
        draw.text((x1 + 110, btn_y + 11), c["btn_text"], font=font_btn, fill=(255, 255, 255))

        # Bear Illustration on the right
        bear_cx = x2 - 175
        bear_cy = y1 + 375
        
        # If use_logo is True and logo exists, embed the Earth PLB Buff Bear with gold ring
        if c.get("use_logo") and os.path.exists(LOGO_PATH):
            try:
                logo_img = Image.open(LOGO_PATH).convert("RGBA")
                asize = 160
                logo_img = logo_img.resize((asize, asize), Image.Resampling.LANCZOS)
                mask = Image.new("L", (asize, asize), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, asize, asize), fill=255)
                ax = bear_cx - asize // 2
                ay = bear_cy - asize // 2
                img.paste(logo_img, (ax, ay), mask)
                draw.ellipse([ax, ay, ax + asize, ay + asize], outline=(251, 191, 36), width=5)
                # Wizard star hat above buff bear
                draw.polygon([(bear_cx, ay - 45), (bear_cx - 45, ay), (bear_cx + 45, ay)], fill=(124, 58, 237))
                draw_star(draw, bear_cx, ay - 25, 12, 6, fill=(251, 191, 36))
            except Exception:
                draw_polar_bear_face(draw, bear_cx, bear_cy, size=135, accessory=c["bear_type"])
        else:
            draw_polar_bear_face(draw, bear_cx, bear_cy, size=135, accessory=c["bear_type"])

    img.save(output_path, "PNG")
    print(f"Modern Cute Polar Bear 6-Button Rich Menu generated: {output_path}")

if __name__ == "__main__":
    generate_cute_polar_rich_menu("rich_menu.png")
    generate_cute_polar_rich_menu("public/rich_menu.png")

