#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Resolution Promotional Poster Generator (1080x1920) for PLB Astrology LINE OA.
Combines 3D Pixar polar bear hero visual, Google Font 'Prompt', feature pills, and LINE OA QR code.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

WIDTH = 1080
HEIGHT = 1920
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD_PATH = os.path.join(BASE_DIR, "Prompt-Bold.ttf")
FONT_MED_PATH = os.path.join(BASE_DIR, "Prompt-Medium.ttf")

HERO_IMG_PATH = os.path.join(BASE_DIR, "bear_poster_hero.jpg")
QR_IMG_PATH = os.path.join(BASE_DIR, "qrcode_line.png")

OUTPUT_PATH_1 = os.path.join(BASE_DIR, "public", "share_poster.jpg")
OUTPUT_PATH_2 = os.path.join(BASE_DIR, "share_poster.jpg")

def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5.0 - math.pi / 2.0
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def create_gradient_bg():
    base = Image.new("RGBA", (WIDTH, HEIGHT), (8, 11, 22, 255))
    draw = ImageDraw.Draw(base)
    
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        if ratio < 0.4:
            r = int(8 + (22 - 8) * (ratio / 0.4))
            g = int(11 + (26 - 11) * (ratio / 0.4))
            b = int(24 + (52 - 24) * (ratio / 0.4))
        elif ratio < 0.8:
            r = int(22 + (15 - 22) * ((ratio - 0.4) / 0.4))
            g = int(26 + (20 - 26) * ((ratio - 0.4) / 0.4))
            b = int(52 + (40 - 52) * ((ratio - 0.4) / 0.4))
        else:
            r = int(15 + (8 - 15) * ((ratio - 0.8) / 0.2))
            g = int(20 + (11 - 20) * ((ratio - 0.8) / 0.2))
            b = int(40 + (22 - 40) * ((ratio - 0.8) / 0.2))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
    
    aurora = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(aurora)
    a_draw.ellipse([600, -100, 1200, 500], fill=(138, 43, 226, 35))
    a_draw.ellipse([-200, 450, 450, 1100], fill=(14, 165, 233, 30))
    a_draw.ellipse([500, 1300, 1200, 1950], fill=(245, 158, 11, 25))
    
    aurora = aurora.filter(ImageFilter.GaussianBlur(80))
    base = Image.alpha_composite(base, aurora)
    
    dust_draw = ImageDraw.Draw(base)
    random.seed(999)
    for _ in range(160):
        sx = random.randint(0, WIDTH)
        sy = random.randint(0, HEIGHT)
        sr = random.choice([1, 1, 2, 2, 3])
        alpha = random.randint(60, 220)
        dust_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, alpha))
        if random.random() < 0.15:
            draw_star(dust_draw, sx, sy, sr * 3.5, sr * 1.5, fill=(251, 191, 36, alpha))
            
    return base

def round_corners(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
    result = image.copy().convert("RGBA")
    result.putalpha(mask)
    return result

def generate_poster():
    img = create_gradient_bg()
    draw = ImageDraw.Draw(img)

    if os.path.exists(FONT_BOLD_PATH) and os.path.exists(FONT_MED_PATH):
        font_pill = ImageFont.truetype(FONT_BOLD_PATH, 28)
        font_title = ImageFont.truetype(FONT_BOLD_PATH, 66)
        font_subtitle = ImageFont.truetype(FONT_MED_PATH, 34)
        font_hero_badge = ImageFont.truetype(FONT_BOLD_PATH, 30)
        font_feat_title = ImageFont.truetype(FONT_BOLD_PATH, 32)
        font_feat_desc = ImageFont.truetype(FONT_MED_PATH, 23)
        font_cta_heading = ImageFont.truetype(FONT_BOLD_PATH, 42)
        font_cta_sub = ImageFont.truetype(FONT_BOLD_PATH, 30)
        font_cta_bullet = ImageFont.truetype(FONT_MED_PATH, 25)
        font_footer = ImageFont.truetype(FONT_MED_PATH, 22)
    else:
        fallback = "C:/Windows/Fonts/tahomabd.ttf"
        font_pill = ImageFont.truetype(fallback, 26)
        font_title = ImageFont.truetype(fallback, 60)
        font_subtitle = ImageFont.truetype(fallback, 32)
        font_hero_badge = ImageFont.truetype(fallback, 28)
        font_feat_title = ImageFont.truetype(fallback, 30)
        font_feat_desc = ImageFont.truetype(fallback, 22)
        font_cta_heading = ImageFont.truetype(fallback, 38)
        font_cta_sub = ImageFont.truetype(fallback, 28)
        font_cta_bullet = ImageFont.truetype(fallback, 24)
        font_footer = ImageFont.truetype(fallback, 20)

    # 1. Top Brand Pill Badge with stars
    pill_text = "น้องหมีแม่หมอพยากรณ์  •  THAI DAILY HOROSCOPE"
    pill_bbox = font_pill.getbbox(pill_text)
    pill_w = pill_bbox[2] - pill_bbox[0]
    pill_h = pill_bbox[3] - pill_bbox[1]
    pill_cx = WIDTH // 2
    pill_y = 65
    pill_pad_x = 55
    pill_pad_y = 12
    draw.rounded_rectangle(
        [(pill_cx - pill_w // 2 - pill_pad_x, pill_y - pill_pad_y),
         (pill_cx + pill_w // 2 + pill_pad_x, pill_y + pill_h + pill_pad_y)],
        radius=25,
        fill=(255, 255, 255, 18),
        outline=(251, 191, 36, 180),
        width=2
    )
    draw_star(draw, pill_cx - pill_w // 2 - 28, pill_y + pill_h // 2 + 1, 11, 5, fill=(251, 191, 36, 255))
    draw_star(draw, pill_cx + pill_w // 2 + 28, pill_y + pill_h // 2 + 1, 11, 5, fill=(251, 191, 36, 255))
    draw.text((pill_cx - pill_w // 2, pill_y - 2), pill_text, fill=(251, 191, 36, 255), font=font_pill)

    # 2. Main Title & Subtitle
    title_text = "เช็กดวงรายวัน & สีเสื้อมงคล"
    title_bbox = font_title.getbbox(title_text)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((WIDTH - title_w) // 2 + 2, 138), title_text, fill=(0, 0, 0, 160), font=font_title)
    draw.text(((WIDTH - title_w) // 2, 136), title_text, fill=(255, 255, 255, 255), font=font_title)

    sub_text = "ดวงแม่นระดับ AI x กิมมิกเสริมดวงจัดเต็มทุกวัน"
    sub_bbox = font_subtitle.getbbox(sub_text)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((WIDTH - sub_w) // 2, 222), sub_text, fill=(203, 213, 225, 240), font=font_subtitle)

    # 3. Hero Visual
    hero_card_x1 = 70
    hero_card_y1 = 290
    hero_card_x2 = WIDTH - 70
    hero_card_y2 = 1040
    hero_w = hero_card_x2 - hero_card_x1
    hero_h = hero_card_y2 - hero_card_y1

    glow_box = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_box)
    glow_draw.rounded_rectangle(
        [(hero_card_x1 - 6, hero_card_y1 - 6), (hero_card_x2 + 6, hero_card_y2 + 6)],
        radius=36,
        fill=(251, 191, 36, 60)
    )
    glow_box = glow_box.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img, glow_box)
    draw = ImageDraw.Draw(img)

    if os.path.exists(HERO_IMG_PATH):
        hero_raw = Image.open(HERO_IMG_PATH).convert("RGBA")
        raw_w, raw_h = hero_raw.size
        target_ratio = hero_w / hero_h
        current_ratio = raw_w / raw_h

        if current_ratio > target_ratio:
            new_w = int(raw_h * target_ratio)
            left = (raw_w - new_w) // 2
            hero_cropped = hero_raw.crop((left, 0, left + new_w, raw_h))
        else:
            new_h = int(raw_w / target_ratio)
            top = max(0, int((raw_h - new_h) * 0.2))
            hero_cropped = hero_raw.crop((0, top, raw_w, top + new_h))

        hero_resized = hero_cropped.resize((hero_w, hero_h), Image.Resampling.LANCZOS)
        hero_rounded = round_corners(hero_resized, 32)
        img.paste(hero_rounded, (hero_card_x1, hero_card_y1), hero_rounded)

    draw.rounded_rectangle(
        [(hero_card_x1, hero_card_y1), (hero_card_x2, hero_card_y2)],
        radius=32,
        outline=(251, 191, 36, 210),
        width=4
    )

    hero_badge_text = "น้องหมีแม่หมอ • ผู้พิทักษ์ดวงชะตาประจำวันของคุณ"
    h_b_bbox = font_hero_badge.getbbox(hero_badge_text)
    h_b_w = h_b_bbox[2] - h_b_bbox[0]
    h_b_h = h_b_bbox[3] - h_b_bbox[1]
    h_b_cx = WIDTH // 2
    h_b_y = hero_card_y2 - 58
    draw.rounded_rectangle(
        [(h_b_cx - h_b_w // 2 - 36, h_b_y - 8), (h_b_cx + h_b_w // 2 + 36, h_b_y + h_b_h + 10)],
        radius=20,
        fill=(15, 23, 42, 230),
        outline=(251, 191, 36, 180),
        width=2
    )
    draw_star(draw, h_b_cx - h_b_w // 2 - 18, h_b_y + h_b_h // 2 + 1, 9, 4, fill=(251, 191, 36, 255))
    draw_star(draw, h_b_cx + h_b_w // 2 + 18, h_b_y + h_b_h // 2 + 1, 9, 4, fill=(251, 191, 36, 255))
    draw.text((h_b_cx - h_b_w // 2, h_b_y - 2), hero_badge_text, fill=(255, 255, 255, 255), font=font_hero_badge)

    # 4. Feature Highlight Grid (2 Columns x 2 Rows)
    features = [
        {
            "tag": "ดวง",
            "tag_bg": (251, 191, 36),
            "tag_fg": (20, 20, 20),
            "title": "สรุปดวง 4 มิติชีวิต",
            "desc": "งาน เงิน รัก สุขภาพ ละเอียด",
            "border": (251, 191, 36, 160)
        },
        {
            "tag": "เสื้อ",
            "tag_bg": (56, 189, 248),
            "tag_fg": (20, 20, 20),
            "title": "สีเสื้อมงคลประจำวัน",
            "desc": "อัปเดตสีนำโชค & กาลกิณี",
            "border": (56, 189, 248, 160)
        },
        {
            "tag": "เซียมซี",
            "tag_bg": (244, 114, 182),
            "tag_fg": (20, 20, 20),
            "title": "เสี่ยงเซียมซี 28 ใบ",
            "desc": "คำทำนายมงคล ลุ้นได้ 24 ชม.",
            "border": (244, 114, 182, 160)
        },
        {
            "tag": "สถิติ",
            "tag_bg": (52, 211, 153),
            "tag_fg": (20, 20, 20),
            "title": "สถิติวาสนา & ยศ",
            "desc": "กราฟคลื่นดวง 7 วัน & เลขเด็ด",
            "border": (52, 211, 153, 160)
        }
    ]

    grid_y_start = 1070
    grid_col_w = 458
    grid_gap_x = 24
    grid_row_h = 105
    grid_gap_y = 16

    font_tag = ImageFont.truetype(FONT_BOLD_PATH, 20) if os.path.exists(FONT_BOLD_PATH) else font_feat_desc

    for i, feat in enumerate(features):
        row = i // 2
        col = i % 2
        gx1 = 70 + col * (grid_col_w + grid_gap_x)
        gy1 = grid_y_start + row * (grid_row_h + grid_gap_y)
        gx2 = gx1 + grid_col_w
        gy2 = gy1 + grid_row_h

        draw.rounded_rectangle(
            [(gx1, gy1), (gx2, gy2)],
            radius=20,
            fill=(18, 25, 48, 220),
            outline=feat["border"],
            width=2
        )

        # Tag pill
        tag_w = 64 if len(feat["tag"]) <= 3 else 76
        draw.rounded_rectangle(
            [(gx1 + 16, gy1 + 22), (gx1 + 16 + tag_w, gy1 + 54)],
            radius=10,
            fill=feat["tag_bg"]
        )
        tag_bbox = font_tag.getbbox(feat["tag"])
        tw = tag_bbox[2] - tag_bbox[0]
        draw.text((gx1 + 16 + (tag_w - tw)//2, gy1 + 24), feat["tag"], fill=feat["tag_fg"], font=font_tag)

        # Title
        draw.text((gx1 + 28 + tag_w, gy1 + 14), feat["title"], fill=(255, 255, 255), font=font_feat_title)
        # Desc
        draw.text((gx1 + 28 + tag_w, gy1 + 54), feat["desc"], fill=(148, 163, 184), font=font_feat_desc)

    # 5. Call To Action (CTA) Card
    cta_x1 = 70
    cta_y1 = 1330
    cta_x2 = WIDTH - 70
    cta_y2 = 1750

    cta_glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cg_draw = ImageDraw.Draw(cta_glow)
    cg_draw.rounded_rectangle(
        [(cta_x1 - 8, cta_y1 - 8), (cta_x2 + 8, cta_y2 + 8)],
        radius=36,
        fill=(251, 191, 36, 45)
    )
    cta_glow = cta_glow.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img, cta_glow)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(cta_x1, cta_y1), (cta_x2, cta_y2)],
        radius=32,
        fill=(13, 20, 40, 245),
        outline=(251, 191, 36, 230),
        width=3
    )

    qr_size = 340
    qr_x = cta_x1 + 40
    qr_y = cta_y1 + (cta_y2 - cta_y1 - qr_size) // 2

    draw.rounded_rectangle(
        [(qr_x - 12, qr_y - 12), (qr_x + qr_size + 12, qr_y + qr_size + 12)],
        radius=24,
        fill=(255, 255, 255, 255),
        outline=(251, 191, 36, 255),
        width=3
    )

    if os.path.exists(QR_IMG_PATH):
        qr_img = Image.open(QR_IMG_PATH).convert("RGBA")
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        img.paste(qr_img, (qr_x, qr_y), qr_img)

    text_x = qr_x + qr_size + 42
    cur_y = cta_y1 + 45

    draw.rounded_rectangle(
        [(text_x, cur_y), (text_x + 220, cur_y + 40)],
        radius=14,
        fill=(6, 199, 85, 230)
    )
    draw.text((text_x + 18, cur_y + 4), "LINE OFFICIAL", fill=(255, 255, 255), font=font_feat_desc)
    
    cur_y += 56
    draw.text((text_x, cur_y), "สแกนเพิ่มเพื่อนทันที", fill=(255, 255, 255), font=font_cta_heading)
    
    cur_y += 62
    id_pill_w = 340
    draw.rounded_rectangle(
        [(text_x, cur_y), (text_x + id_pill_w, cur_y + 54)],
        radius=16,
        fill=(30, 41, 59, 240),
        outline=(251, 191, 36, 200),
        width=2
    )
    draw.text((text_x + 20, cur_y + 8), "LINE ID: @374xcoto", fill=(251, 191, 36), font=font_cta_sub)

    cur_y += 75
    bullets = [
        "ดูดวงรายวัน & เช็กสีเสื้อมงคลฟรี!",
        "เสี่ยงเซียมซี 28 ใบ ได้ตลอด 24 ชม.",
        "ส่งต่อให้เพื่อน เพื่อรับพลังบวกไปด้วยกัน"
    ]
    for b in bullets:
        draw.ellipse([text_x, cur_y + 12, text_x + 8, cur_y + 20], fill=(251, 191, 36))
        draw.text((text_x + 22, cur_y), b, fill=(226, 232, 240), font=font_cta_bullet)
        cur_y += 40

    # 6. Footer Note
    footer_text = "น้องหมีแม่หมอพยากรณ์ • Thai Daily Horoscope • LINE OA: @374xcoto"
    f_bbox = font_footer.getbbox(footer_text)
    f_w = f_bbox[2] - f_bbox[0]
    draw.text(((WIDTH - f_w) // 2, HEIGHT - 85), footer_text, fill=(148, 163, 184, 180), font=font_footer)

    img_rgb = img.convert("RGB")
    os.makedirs(os.path.dirname(OUTPUT_PATH_1), exist_ok=True)
    img_rgb.save(OUTPUT_PATH_1, format="JPEG", quality=95)
    img_rgb.save(OUTPUT_PATH_2, format="JPEG", quality=95)
    print(f"Successfully generated poster at:\n  -> {OUTPUT_PATH_1}\n  -> {OUTPUT_PATH_2}")

if __name__ == "__main__":
    generate_poster()
