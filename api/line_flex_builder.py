#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Flex Message Builder for PLB Thai Astrology Bot
Produces pixel-perfect, dark cosmic & luxury gold themed Flex Messages.
Compatible with LINE Messaging API specifications.
"""

import datetime
import re

def build_new_friend_welcome_flex(liff_url: str, web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build a world-class, ultra-cute 3D mascot welcome onboarding card for new LINE OA friends."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    return {
        "type": "flex",
        "altText": "🐻‍❄️ ยินดีต้อนรับเพื่อนใหม่สู่น้องหมีแม่หมอพยากรณ์ ✨",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/bear_welcome.jpg",
                "size": "full",
                "aspectRatio": "16:9",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": liff_url
                }
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🐻‍❄️ ยินดีต้อนรับเพื่อนใหม่ ✨", "weight": "bold", "color": "#fbbf24", "size": "md", "flex": 1},
                            {"type": "text", "text": "AI x ดาราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {"type": "text", "text": "น้องหมีแม่หมอ • ผู้พิทักษ์ดวงชะตาประจำวันของคุณ", "color": "#cbd5e1", "size": "xs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "text",
                        "text": "สวัสดีครับ! น้องหมียินดีที่ได้รู้จักนะครับ 💖",
                        "weight": "bold",
                        "size": "md",
                        "color": "#f8fafc"
                    },
                    {
                        "type": "text",
                        "text": "น้องหมีพร้อมพาคุณมาผูกดวงชะตาเฉพาะบุคคล คำนวณลัคนาแม่นยำ พร้อมอัปเดตสีเสื้อมงคลและเสี่ยงเซียมซีได้ฟรีทุกวันครับ 🔮",
                        "size": "xs",
                        "color": "#cbd5e1",
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "12px",
                        "contents": [
                            {"type": "text", "text": "🌟 ฟีเจอร์ที่คุณจะได้รับฟรีทุกวัน:", "weight": "bold", "size": "xs", "color": "#fbbf24"},
                            {"type": "text", "text": "• คำนวณลัคนาราศีและดวง 4 มิติชีวิต (งาน เงิน รัก สุขภาพ)", "size": "xxs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• ตารางสีเสื้อมงคลประจำวัน เสริมโชคลาภ & กาลกิณี", "size": "xxs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• เสี่ยงเซียมซี 28 ใบ พร้อมใบคำทำนายมงคล 24 ชม.", "size": "xxs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• สถิติวาสนาสะสม คลื่นดวง 7 วัน & กิมมิกเลขเด็ด", "size": "xxs", "color": "#94a3b8", "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm",
                        "backgroundColor": "#06281e",
                        "borderColor": "#10b981",
                        "borderWidth": "1px",
                        "cornerRadius": "10px",
                        "paddingAll": "10px",
                        "contents": [
                            {"type": "text", "text": "🛡️ ปลอดภัย 100% เจ้าของแอปไม่มีการเก็บข้อมูลส่วนตัวใด ๆ ทั้งสิ้น", "size": "xxs", "color": "#86efac", "weight": "bold", "wrap": True}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "14px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#f59e0b",
                        "action": {
                            "type": "uri",
                            "label": "🌟 แตะผูกดวง & เริ่มต้นใช้งาน",
                            "uri": liff_url
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "action": {
                            "type": "message",
                            "label": "👥 ชวนเพื่อน & รับรูปโปสเตอร์มู",
                            "text": "โปสเตอร์"
                        }
                    }
                ]
            }
        }
    }

def build_welcome_flex(liff_url: str) -> dict:
    """Build a welcoming onboarding card prompting the user to register birth info."""
    return {
        "type": "flex",
        "altText": "ยินดีต้อนรับสู่ PLB โหราศาสตร์ 🔮",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🔮 PLB โหราศาสตร์", "weight": "bold", "color": "#f59e0b", "size": "md", "flex": 1},
                            {"type": "text", "text": "โหราศาสตร์ไทยชั้นสูง", "color": "#94a3b8", "size": "xs", "align": "end"}
                        ]
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "ยินดีต้อนรับสู่ระบบดูดวงส่วนบุคคล ✨", "weight": "bold", "size": "lg", "color": "#f8fafc", "wrap": True},
                    {"type": "text", "text": "คำนวณลัคนาและตำแหน่งดาวจรตามพิกัดดาราศาสตร์จริง ละเอียดถึงระดับเขต/อำเภอ", "size": "sm", "color": "#cbd5e1", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "14px",
                        "contents": [
                            {"type": "text", "text": "🌟 ฟีเจอร์ที่คุณจะได้รับ:", "weight": "bold", "size": "xs", "color": "#fbbf24"},
                            {"type": "text", "text": "• คำนวณลัคนาราศีแม่นยำด้วยอันโตนาทีสามัญ", "size": "xs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• สรุปดวงรายวัน 4 ด้าน (งาน, เงิน, รัก, สุขภาพ)", "size": "xs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• ปรับเปลี่ยนสถานที่จรได้ทุกวันตามที่คุณเดินทาง", "size": "xs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": "• เลขมงคล, สีมงคล, ทิศมงคล และเคล็ดลับเสริมดวง", "size": "xs", "color": "#94a3b8", "margin": "xs"}
                        ]
                    },
                    # Privacy & Data Security Guarantee Box
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#06281e",
                        "borderColor": "#10b981",
                        "borderWidth": "1px",
                        "cornerRadius": "10px",
                        "paddingAll": "12px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": "🛡️ คำยืนยันความปลอดภัย & ความเป็นส่วนตัว", "weight": "bold", "size": "xs", "color": "#86efac", "flex": 1}
                                ]
                            },
                            {"type": "text", "text": "เจ้าของแอปไม่มีการบันทึกหรือเก็บข้อมูลส่วนตัวใด ๆ ทั้งสิ้น ข้อมูลวันเวลาเกิดใช้เพื่อคำนวณตำแหน่งดวงดาวบนอุปกรณ์ของคุณเท่านั้น ปลอดภัย 100% สบายใจไม่ต้องกังวลครับ 🔒✨", "size": "xxs", "color": "#a7f3d0", "wrap": True, "margin": "xs"}
                        ]
                    },
                    {"type": "text", "text": "กรุณาลงทะเบียนข้อมูลวันเกิดและสถานที่เกิด เพื่อเริ่มคำนวณดวงชะตาเฉพาะตัวของคุณ 👇", "size": "xs", "color": "#38bdf8", "wrap": True, "margin": "md"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#f59e0b",
                        "action": {
                            "type": "uri",
                            "label": "🌟 ลงทะเบียนข้อมูลดวงชะตา",
                            "uri": liff_url
                        }
                    }
                ]
            }
        }
    }

def make_progress_bar(score: int, fill_color: str = "#fbbf24", bg_color: str = "#1e293b", height: str = "8px") -> dict:
    """Create a sleek visual vector progress bar using Flex boxes."""
    fill_flex = max(1, min(100, int(score)))
    empty_flex = max(1, 100 - fill_flex)
    return {
        "type": "box",
        "layout": "horizontal",
        "height": height,
        "backgroundColor": bg_color,
        "cornerRadius": "99px",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": fill_color,
                "flex": fill_flex,
                "height": height,
                "cornerRadius": "99px",
                "contents": [{"type": "filler"}]
            },
            {
                "type": "box",
                "layout": "vertical",
                "flex": empty_flex,
                "contents": [{"type": "filler"}]
            }
        ]
    }

def get_postback_meta(user: dict) -> str:
    """Generate compact postback metadata preserving birth chart and user stats across stateless requests."""
    if not user:
        return ""
    b_date = user.get("birth_date", "1995-08-12")
    b_time = user.get("birth_time", "08:30")
    b_prov = user.get("birth_province", "กรุงเทพมหานคร")
    t_prov = user.get("transit_province", b_prov)
    try:
        cc = int(user.get("check_count", 1))
    except (ValueError, TypeError):
        cc = 1
    try:
        st = int(user.get("streak", 1))
    except (ValueError, TypeError):
        st = 1
    try:
        xp = int(user.get("xp", 0))
    except (ValueError, TypeError):
        xp = 0
    try:
        lvl = int(user.get("level", 1))
    except (ValueError, TypeError):
        lvl = 1
    ld = user.get("last_check_date", "")
    name = user.get("name", "ผู้ใช้")
    return f"&b={b_date}&t={b_time}&p={b_prov}&tp={t_prov}&cc={cc}&st={st}&ld={ld}&n={name}&xp={xp}&lvl={lvl}"


def make_liff_url(base_url: str, user: dict = None, extra_query: str = "") -> str:
    """Build a LIFF URL embedding user id, check_count, streak, xp, and birth chart parameters."""
    if not base_url:
        return ""
    import urllib.parse
    user = user or {}
    uid = user.get("line_user_id", "")
    cc = user.get("check_count", 0)
    st = user.get("streak", 1)
    xp = user.get("xp", 0)
    lvl = user.get("level", 1)
    ld = user.get("last_check_date", "")
    n = urllib.parse.quote(str(user.get("name", "ผู้ใช้")))
    b = user.get("birth_date", "")
    t = user.get("birth_time", "")
    p = urllib.parse.quote(str(user.get("birth_province", "กรุงเทพมหานคร")))
    tp = urllib.parse.quote(str(user.get("transit_province", user.get("birth_province", "กรุงเทพมหานคร"))))
    
    clean_base = base_url.split("?")[0]
    res = f"{clean_base}?userId={uid}&cc={cc}&st={st}&ld={ld}&n={n}&b={b}&t={t}&p={p}&tp={tp}&xp={xp}&lvl={lvl}"
    if extra_query:
        if extra_query.startswith("#"):
            res += extra_query
        else:
            res += f"&{extra_query.lstrip('&')}"
    return res

def build_daily_summary_flex(user: dict, horoscope: dict, liff_url: str = "", web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build an Ultra-Premium Royal Gold & Obsidian themed Daily Summary Flex Card."""
    from user_store import get_rank_title
    
    web_url = web_url or "https://plb-horoscope.vercel.app"
    liff_url = liff_url or f"{web_url}/liff-register.html"
    
    natal = horoscope.get("natalChart", {})
    asc = natal.get("ascendant", {})
    asc_name = asc.get("signName", "เมษ")
    asc_deg = asc.get("signDegree", 0)
    asc_min = asc.get("arcMinutes", 0)
    
    transit = horoscope.get("transitLocation", {})
    transit_prov = transit.get("province", "กรุงเทพมหานคร")
    transit_dist = transit.get("district", "พระนคร")
    sunrise = transit.get("sunriseTime", "06:00")
    
    cats = horoscope.get("categories", {})
    overall = cats.get("overall", {})
    overall_score = overall.get("score", 80)
    career = cats.get("career", {})
    finance = cats.get("finance", {})
    love = cats.get("love", {})
    health = cats.get("health", {})
    
    lucky = horoscope.get("luckyInfo", {})
    lucky_nums = " ".join([str(n) for n in lucky.get("numbers", [1, 5, 9])[:3]])
    lucky_colors = lucky.get("colors", "ทองคำ, เหลืองมงคล")
    lucky_dirs = lucky.get("directions", "ทิศมหาราช (ตะวันออก)")
    gemstones = lucky.get("gemstones", "บุษราคัมจักรพรรดิ์")
    
    date_str = horoscope.get("date", "")
    user_name = user.get("name", "ผู้ใช้")
    check_count = user.get("check_count", 1)
    streak = user.get("streak", 1)
    rank = get_rank_title(check_count, streak)
    
    # Stateless postback metadata preserving stats
    pb_meta = get_postback_meta(user)

    # Visual gauge color based on score
    gauge_color = "#fbbf24" if overall_score >= 85 else ("#38bdf8" if overall_score >= 75 else "#a78bfa")

    return {
        "type": "flex",
        "altText": f"👑 ดวงประจำวัน: ลัคนาราศี{asc_name} (เกณฑ์วาสนา {overall_score}%)",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/bear_wizard.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "👑 PLB โหราศาสตร์ไทยชั้นสูง", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                            {"type": "text", "text": f"📅 {date_str}", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "alignItems": "center",
                        "contents": [
                            {"type": "text", "text": f"ดวงชะตาคุณ {user_name}", "color": "#f8fafc", "size": "md", "weight": "bold", "flex": 1},
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#1e1b4b",
                                "borderColor": "#818cf8",
                                "borderWidth": "1px",
                                "cornerRadius": "99px",
                                "paddingStart": "8px",
                                "paddingEnd": "8px",
                                "paddingTop": "2px",
                                "paddingBottom": "2px",
                                "contents": [
                                    {"type": "text", "text": rank["title"], "color": "#c7d2fe", "size": "xxs", "weight": "bold"}
                                ]
                            }
                        ]
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#070b19",
                "paddingAll": "16px",
                "contents": [
                    # Ascendant & Transit Badge
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#0d1b38",
                        "borderColor": "#1d4ed8",
                        "borderWidth": "1px",
                        "cornerRadius": "12px",
                        "paddingAll": "12px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": f"✨ ลัคนาราศี{asc_name} • วาสนามหาจักร", "size": "sm", "color": "#fef08a", "weight": "bold", "flex": 1},
                                    {"type": "text", "text": f"{asc_deg}° {asc_min}'", "size": "xs", "color": "#93c5fd", "weight": "bold", "align": "end"}
                                ]
                            },
                            {"type": "text", "text": f"📍 สถิตจร: {transit_prov} ({transit_dist}) • รุ่งอรุณ {sunrise} น.", "size": "xxs", "color": "#7dd3fc", "margin": "xs"}
                        ]
                    },
                    # Overall Power Score Gauge
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#0f172a",
                        "borderColor": "#334155",
                        "borderWidth": "1px",
                        "cornerRadius": "12px",
                        "paddingAll": "12px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "alignItems": "center",
                                "contents": [
                                    {"type": "text", "text": "⚜️ ดัชนีพลังดวงชะตาประจำวัน", "size": "xs", "color": "#e2e8f0", "weight": "bold", "flex": 1},
                                    {"type": "text", "text": f"{overall_score}%", "size": "lg", "color": gauge_color, "weight": "bold", "align": "end"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xs",
                                "contents": [
                                    make_progress_bar(overall_score, fill_color=gauge_color, bg_color="#1e293b", height="8px")
                                ]
                            },
                            {"type": "text", "text": overall.get("theme", "จังหวะดวงเปิดกว้าง มีเกณฑ์ก้าวหน้าราบรื่น"), "size": "xs", "color": "#fef08a", "wrap": True, "margin": "xs"},
                            # Gamified Streak Badge
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "sm",
                                "backgroundColor": "#172554",
                                "cornerRadius": "8px",
                                "paddingAll": "6px",
                                "contents": [
                                    {"type": "text", "text": f"🔥 ตรวจดวงสะสม {check_count} ครั้ง • เช็กติดต่อกัน {streak} วัน", "size": "xxs", "color": "#67e8f9", "weight": "bold", "align": "center"}
                                ]
                            }
                        ]
                    },
                    # 4 Pillars of Destiny
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "🏛️ จตุสดมภ์โชคลาภ 4 ด้าน (แตะดูเจาะลึก):", "size": "xxs", "color": "#fbbf24", "weight": "bold"},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "spacing": "xs",
                                "contents": [
                                    # Career
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#0b192c",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "action": {
                                            "type": "postback",
                                            "label": "การงาน",
                                            "data": f"action=category_career{pb_meta}",
                                            "displayText": "การงาน"
                                        },
                                        "contents": [
                                            {"type": "text", "text": f"💼 งาน {career.get('score', 80)}% ›", "size": "xxs", "color": "#93c5fd", "weight": "bold"},
                                            {"type": "text", "text": career.get("summary", "งานก้าวหน้า"), "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                                        ]
                                    },
                                    # Finance
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#1c1917",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "action": {
                                            "type": "postback",
                                            "label": "การเงิน",
                                            "data": f"action=category_finance{pb_meta}",
                                            "displayText": "การเงิน"
                                        },
                                        "contents": [
                                            {"type": "text", "text": f"💰 เงิน {finance.get('score', 80)}% ›", "size": "xxs", "color": "#fef08a", "weight": "bold"},
                                            {"type": "text", "text": finance.get("summary", "เงินคล่องตัว"), "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "spacing": "xs",
                                "contents": [
                                    # Love
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#1f1224",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "action": {
                                            "type": "postback",
                                            "label": "ความรัก",
                                            "data": f"action=category_love{pb_meta}",
                                            "displayText": "ความรัก"
                                        },
                                        "contents": [
                                            {"type": "text", "text": f"❤️ รัก {love.get('score', 80)}% ›", "size": "xxs", "color": "#f472b6", "weight": "bold"},
                                            {"type": "text", "text": love.get("summary", "เสน่ห์เมตตา"), "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                                        ]
                                    },
                                    # Health
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#06231a",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "action": {
                                            "type": "postback",
                                            "label": "สุขภาพ",
                                            "data": f"action=category_health{pb_meta}",
                                            "displayText": "สุขภาพ"
                                        },
                                        "contents": [
                                            {"type": "text", "text": f"🩺 กาย {health.get('score', 80)}% ›", "size": "xxs", "color": "#86efac", "weight": "bold"},
                                            {"type": "text", "text": health.get("summary", "พลังชีวาสดใส"), "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    # Sacred Royal Alignments
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#0f172a",
                        "borderColor": "#ca8a04",
                        "borderWidth": "1px",
                        "cornerRadius": "10px",
                        "paddingAll": "10px",
                        "contents": [
                            {"type": "text", "text": "⚜️ เครื่องหมายมงคลราชสำนัก:", "size": "xxs", "color": "#fbbf24", "weight": "bold"},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {"type": "text", "text": f"🔢 เลขเทวราช: {lucky_nums}", "size": "xxs", "color": "#f8fafc", "flex": 1},
                                    {"type": "text", "text": f"🎨 สีมหาจักร: {lucky_colors}", "size": "xxs", "color": "#f8fafc", "flex": 1}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {"type": "text", "text": f"🧭 ทิศมหาราช: {lucky_dirs}", "size": "xxs", "color": "#94a3b8", "flex": 1},
                                    {"type": "text", "text": f"💎 อัญมณี: {gemstones}", "size": "xxs", "color": "#94a3b8", "flex": 1}
                                ]
                            }
                        ]
                    },
                    # Privacy Reassurance Badge
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "contents": [
                            {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ปลอดภัย 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "12px",
                "spacing": "xs",
                "contents": [
                    # 1. PROMINENT PRIMARY CTA: เลือกหมวดอยากจะดูหมวดไหน
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#d97706",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "🔮 เลือกหมวดอยากจะดูหมวดไหน",
                            "data": f"action=select_category{pb_meta}",
                            "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
                        }
                    },
                    # 2. SECONDARY SPLIT ROW: สถิติดวงย้อนหลัง & เปลี่ยนสถานที่จร
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "📊 สถิติดวงย้อนหลัง",
                                    "data": f"action=stats{pb_meta}",
                                    "displayText": "สถิติดวงย้อนหลัง"
                                },
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "📍 เปลี่ยนสถานที่จร",
                                    "data": f"action=change_transit{pb_meta}",
                                    "displayText": "เปลี่ยนสถานที่จร"
                                },
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "uri",
                                    "label": "⚙️ แก้ไขวันเกิด",
                                    "uri": make_liff_url(liff_url, user)
                                },
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#065f46",
                                "height": "sm",
                                "action": {
                                    "type": "uri",
                                    "label": "👥 ชวนเพื่อนดูดวง",
                                    "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                                },
                                "flex": 1
                            }
                        ]
                    }
                ]
            }
        },
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวดดูดวง", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                {"type": "action", "action": {"type": "message", "label": "🗓️ ดวงรายเดือน", "text": "ดวงรายเดือน"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                {"type": "action", "action": {"type": "uri", "label": "🌐 ดูละเอียดบนเว็บ", "uri": make_liff_url(f"{web_url}/", user) if user else f"{web_url}/"}},
                {"type": "action", "action": {"type": "message", "label": "📍 เปลี่ยนที่จร", "text": "เปลี่ยนสถานที่จร"}}
            ]
        }
    }

def build_stats_flex(user: dict, horoscope: dict, days_history: list = None) -> dict:
    """Build the Gamified Personal Astro Stats & 7-Day Luck Wave Flex Card."""
    try:
        from user_store import get_rank_title
        from thai_astrology import get_horoscope
    except ImportError:
        from api.user_store import get_rank_title
        from api.thai_astrology import get_horoscope
    import datetime

    user_name = user.get("name", "ผู้ใช้")
    check_count = user.get("check_count", 1)
    streak = user.get("streak", 1)
    rank = get_rank_title(check_count, streak)
    
    # Calculate 7-day luck history if not provided
    if not days_history:
        now_th = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        thai_months = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
        days_history = []
        for offset in range(-4, 3):
            d = now_th + datetime.timedelta(days=offset)
            d_str = d.strftime("%Y-%m-%d")
            day_name = thai_days[d.weekday()]
            label = f"{day_name[:2]} {d.day} {thai_months[d.month]}"
            try:
                h_day = get_horoscope(user, d_str)
                sc = h_day.get("categories", {}).get("overall", {}).get("score", 78)
            except Exception:
                sc = 80
            days_history.append({
                "date": d_str,
                "label": label,
                "score": sc,
                "is_today": (offset == 0)
            })

    best_day = max(days_history, key=lambda x: x["score"])
    avg_score = round(sum(d["score"] for d in days_history) / len(days_history))
    
    # Build visual progress bar rows for the 7 days
    day_rows = []
    for d in days_history:
        is_today = d.get("is_today", False)
        is_best = (d["date"] == best_day["date"])
        sc = d["score"]
        bar_color = "#fbbf24" if sc >= 85 else ("#38bdf8" if sc >= 75 else "#a78bfa")
        
        status_tag = " 🏆 (สูงสุด)" if is_best else (" ✨ (วันนี้)" if is_today else "")
        day_rows.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xs",
            "backgroundColor": "#172554" if is_today else "#0a0f24",
            "borderColor": "#3b82f6" if is_today else "#1e293b",
            "borderWidth": "1px",
            "cornerRadius": "8px",
            "paddingAll": "8px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"{d['label']}{status_tag}", "size": "xxs", "color": "#fef08a" if is_today else "#e2e8f0", "weight": "bold" if (is_today or is_best) else "regular", "flex": 3},
                        {"type": "text", "text": f"{sc}%", "size": "xxs", "color": bar_color, "weight": "bold", "align": "end", "flex": 1}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xs",
                    "contents": [
                        make_progress_bar(sc, fill_color=bar_color, bg_color="#1e293b", height="6px")
                    ]
                }
            ]
        })

    # Stateless postback metadata preserving stats
    pb_meta = get_postback_meta(user)

    return {
        "type": "flex",
        "altText": f"📊 แดชบอร์ดสถิติดวงชะตา: คุณ {user_name} ({rank['title']})",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": "https://plb-horoscope.vercel.app/bear_explorer.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "📊 แดชบอร์ดสถิติดวงชะตา", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                            {"type": "text", "text": "PLB โหราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {"type": "text", "text": f"บันทึกประวัติและความเฮงของคุณ {user_name} ✨", "color": "#e2e8f0", "size": "xs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#070b19",
                "paddingAll": "16px",
                "contents": [
                    # Rank & Streak Trophy Card
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#0f172a",
                        "borderColor": "#ca8a04",
                        "borderWidth": "1px",
                        "cornerRadius": "12px",
                        "paddingAll": "14px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "alignItems": "center",
                                "contents": [
                                    {"type": "text", "text": rank["title"], "size": "md", "color": rank["color"], "weight": "bold", "flex": 1},
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#172554",
                                        "cornerRadius": "99px",
                                        "paddingStart": "8px",
                                        "paddingEnd": "8px",
                                        "paddingTop": "2px",
                                        "paddingBottom": "2px",
                                        "contents": [
                                            {"type": "text", "text": rank["badge"], "size": "xxs", "color": "#93c5fd", "weight": "bold"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "sm",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#1e293b",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "contents": [
                                            {"type": "text", "text": "💬 สนทนา & ตรวจดวง", "size": "xxs", "color": "#94a3b8"},
                                            {"type": "text", "text": f"{check_count} ครั้ง", "size": "sm", "color": "#fbbf24", "weight": "bold"}
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#1e293b",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "contents": [
                                            {"type": "text", "text": "🔥 คุยต่อเนื่อง", "size": "xxs", "color": "#94a3b8"},
                                            {"type": "text", "text": f"{streak} วันติด", "size": "sm", "color": "#38bdf8", "weight": "bold"}
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "backgroundColor": "#1e293b",
                                        "cornerRadius": "8px",
                                        "paddingAll": "8px",
                                        "flex": 1,
                                        "contents": [
                                            {"type": "text", "text": "📈 เฉลี่ยสัปดาห์นี้", "size": "xxs", "color": "#94a3b8"},
                                            {"type": "text", "text": f"{avg_score}%", "size": "sm", "color": "#86efac", "weight": "bold"}
                                        ]
                                    }
                                ]
                            },
                            {"type": "text", "text": rank["perk"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "sm"}
                        ]
                    },
                    # 7-Day Planetary Wave Section
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": "📈 กราฟความเฮง 7 วัน (7-Day Luck Wave):", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 1},
                                    {"type": "text", "text": f"🏆 สูงสุด: {best_day['score']}%", "size": "xxs", "color": "#fef08a", "weight": "bold", "align": "end"}
                                ]
                            },
                            *day_rows
                        ]
                    },
                    # Motivational astro tip
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#111827",
                        "borderColor": "#374151",
                        "borderWidth": "1px",
                        "cornerRadius": "10px",
                        "paddingAll": "10px",
                        "contents": [
                            {"type": "text", "text": "💡 เคล็ดลับการรักษาสถิติวาสนา:", "size": "xxs", "color": "#38bdf8", "weight": "bold"},
                            {"type": "text", "text": "การตรวจดวงทุกเช้าช่วยให้คุณตั้งรับและคว้าจังหวะโชคดีได้แม่นยำ เช็กต่อเนื่องทุกวันเพื่อสะสมแต้มวาสนาสู่ระดับมหาจักรพรรดิ์ครับ ✨", "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                        ]
                    },
                    # Privacy Reassurance Badge
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "contents": [
                            {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ข้อมูลอยู่บนเครื่องคุณ 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "12px",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#d97706",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "🌟 ดูสรุปดวงประจำวัน",
                            "data": f"action=daily_summary{pb_meta}",
                            "displayText": "สรุปดวงประจำวัน"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "🔮 เลือกหมวดดูดวง",
                                    "data": f"action=select_category{pb_meta}",
                                    "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
                                },
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#065f46",
                                "height": "sm",
                                "action": {
                                    "type": "uri",
                                    "label": "👥 ชวนเพื่อนดูดวง",
                                    "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                                },
                                "flex": 1
                            }
                        ]
                    }
                ]
            }
        },
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวดดูดวง", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}}
            ]
        }
    }

def build_monthly_forecast_flex(user: dict, forecast_28: dict, liff_url: str = "", web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build a specialized luxury Flex card for 28-day monthly horoscope & auspicious action days."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    liff_url = liff_url or f"{web_url}#monthly"
    user_name = user.get("name", "ผู้ใช้")
    asc_name = forecast_28.get("ascendant", "สิงห์")
    avg_score = forecast_28.get("averageScore", 75)
    date_range = forecast_28.get("dateRangeLabel", "")
    peak_day = forecast_28.get("peakDay", {})
    lowest_day = forecast_28.get("lowestDay", {})
    golden_days = forecast_28.get("goldenDays", [])[:3]
    caution_days = forecast_28.get("cautionDays", [])[:3]
    weeks = forecast_28.get("weeks", [])

    # 4 Weeks progress bar contents
    week_rows = []
    for w in weeks:
        w_sc = w.get("avgScore", 75)
        bar_color = "#fbbf24" if w_sc >= 80 else ("#38bdf8" if w_sc >= 74 else "#a78bfa")
        week_rows.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": w.get("label", ""), "size": "xxs", "color": "#cbd5e1", "flex": 3},
                        {"type": "text", "text": f"{w_sc}%", "size": "xxs", "color": bar_color, "weight": "bold", "align": "end", "flex": 1}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xs",
                    "contents": [
                        make_progress_bar(w_sc, fill_color=bar_color, bg_color="#1e293b", height="5px")
                    ]
                }
            ]
        })

    # Golden days box contents
    golden_items = []
    for g in golden_days:
        golden_items.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xs",
            "backgroundColor": "#0d2818",
            "borderColor": "#10b981",
            "borderWidth": "1px",
            "cornerRadius": "8px",
            "paddingAll": "8px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"🌟 {g.get('shortLabel', '')} ({g.get('weekday', '')})", "size": "xs", "weight": "bold", "color": "#86efac", "flex": 3},
                        {"type": "text", "text": f"{g.get('score', 80)}%", "size": "xs", "weight": "bold", "color": "#fbbf24", "align": "end", "flex": 1}
                    ]
                },
                {"type": "text", "text": f"• {g.get('actionAdvice', 'เหมาะทำการใหญ่')}", "size": "xxs", "color": "#f0fdf4", "wrap": True, "margin": "xs"}
            ]
        })

    # Caution days box contents
    caution_items = []
    for c in caution_days:
        caution_items.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xs",
            "backgroundColor": "#2a0808",
            "borderColor": "#ef4444",
            "borderWidth": "1px",
            "cornerRadius": "8px",
            "paddingAll": "8px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"⚠️ {c.get('shortLabel', '')} ({c.get('weekday', '')})", "size": "xs", "weight": "bold", "color": "#fca5a5", "flex": 3},
                        {"type": "text", "text": f"{c.get('score', 65)}%", "size": "xs", "weight": "bold", "color": "#f87171", "align": "end", "flex": 1}
                    ]
                },
                {"type": "text", "text": f"• {c.get('actionAdvice', 'ควรระวังรอบคอบ')}", "size": "xxs", "color": "#fef2f2", "wrap": True, "margin": "xs"}
            ]
        })

    return {
        "type": "flex",
        "altText": f"🗓️ สรุปดวงรายเดือน 28 วันข้างหน้า: คุณ {user_name} (คะแนนเฉลี่ย {avg_score}%) ✨",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/bear_monthly.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#080b16",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🗓️ สรุปดวง 28 วันข้างหน้า ✨", "weight": "bold", "color": "#fbbf24", "size": "md", "flex": 1},
                            {"type": "text", "text": "วางแผนชีวิตมงคล", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {"type": "text", "text": f"คุณ {user_name} • ลัคนาราศี{asc_name} • {date_range}", "color": "#cbd5e1", "size": "xs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    # KPI Badges Box
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "10px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "คะแนนเฉลี่ย", "size": "xxs", "color": "#94a3b8", "align": "center"},
                                    {"type": "text", "text": f"{avg_score}%", "size": "md", "weight": "bold", "color": "#38bdf8", "align": "center"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "🌟 พีคสุด", "size": "xxs", "color": "#94a3b8", "align": "center"},
                                    {"type": "text", "text": f"{peak_day.get('shortLabel', '')}", "size": "sm", "weight": "bold", "color": "#fbbf24", "align": "center"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "⚠️ ควรระวัง", "size": "xxs", "color": "#94a3b8", "align": "center"},
                                    {"type": "text", "text": f"{lowest_day.get('shortLabel', '')}", "size": "sm", "weight": "bold", "color": "#f87171", "align": "center"}
                                ]
                            }
                        ]
                    },
                    # 4 Weeks Phase
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "📊 แนวโน้มดวงชะตา 4 สัปดาห์:", "weight": "bold", "size": "xs", "color": "#f8fafc"},
                            *week_rows
                        ]
                    },
                    # Golden Days
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "🌟 วันมงคลฤกษ์ดี • เหมาะทำการใหญ่:", "weight": "bold", "size": "xs", "color": "#34d399"},
                            *golden_items
                        ]
                    },
                    # Caution Days
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "⚠️ วันควรระวัง • งดทำการใหญ่และมีสติ:", "weight": "bold", "size": "xs", "color": "#f87171"},
                            *caution_items
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#080b16",
                "paddingAll": "12px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#f59e0b",
                        "action": {
                            "type": "uri",
                            "label": "📊 ดูดวงละเอียดบนเว็บ (กราฟ 28 วัน)",
                            "uri": make_liff_url(f"{web_url}/", user, extra_query="#monthly") if user else f"{web_url}/#monthly"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "action": {
                            "type": "message",
                            "label": "🌟 ดูดวงสรุปวันนี้",
                            "text": "สรุปดวงวันนี้"
                        }
                    }
                ]
            }
        },
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🌟 ดูดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวดดวง", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "uri", "label": "🌐 ดูละเอียดบนเว็บ", "uri": make_liff_url(f"{web_url}/", user, extra_query="#monthly") if user else f"{web_url}/#monthly"}},
                {"type": "action", "action": {"type": "message", "label": "👥 ชวนเพื่อนมู", "text": "ชวนเพื่อน"}}
            ]
        }
    }

def build_category_menu_flex(web_url: str = "https://plb-horoscope.vercel.app", user: dict = None) -> dict:
    """Build an interactive luxury card to choose horoscope categories."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    pb_meta = get_postback_meta(user) if user else ""
    return {
        "type": "flex",
        "altText": "🔮 เลือกหมวดดูดวงเจาะลึก (การงาน, การเงิน, ความรัก, สุขภาพ)",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/bear_wizard.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🔮 เลือกหมวดดูดวงเจาะลึก", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                            {"type": "text", "text": "PLB โหราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {"type": "text", "text": "แตะเลือกหมวดที่คุณต้องการทำนายเฉพาะด้านได้ทันที 👇", "color": "#cbd5e1", "size": "xs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#070b19",
                "paddingAll": "14px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#1d4ed8",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "💼 ดูหมวดการงาน & ธุรกิจ",
                            "data": f"action=category&cat=career{pb_meta}" if pb_meta else "การงาน",
                            "displayText": "การงาน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#047857",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "💰 ดูหมวดการเงิน & โชคลาภ",
                            "data": f"action=category&cat=finance{pb_meta}" if pb_meta else "การเงิน",
                            "displayText": "การเงิน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#be185d",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "❤️ ดูหมวดความรัก & เสน่ห์",
                            "data": f"action=category&cat=love{pb_meta}" if pb_meta else "ความรัก",
                            "displayText": "ความรัก"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#b45309",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "🩺 ดูหมวดสุขภาพ & เตือนภัย",
                            "data": f"action=category&cat=health{pb_meta}" if pb_meta else "สุขภาพ",
                            "displayText": "สุขภาพ"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#7c3aed",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "🥠 เสี่ยงเซียมซีพยากรณ์",
                            "data": f"action=siamsee{pb_meta}" if pb_meta else "เซียมซี",
                            "displayText": "เซียมซี"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#d97706",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "🎰 ขอเลขเด็ด & เลขมงคล",
                            "data": f"action=lucky_numbers{pb_meta}" if pb_meta else "ขอเลขเด็ด",
                            "displayText": "ขอเลขเด็ด"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#4f46e5",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "👕 ตารางสีเสื้อมงคล",
                            "data": f"action=lucky_colors{pb_meta}" if pb_meta else "สีเสื้อมงคล",
                            "displayText": "สีเสื้อมงคล"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "backgroundColor": "#030712",
                "paddingAll": "12px",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "🌟 สรุปดวงรวม",
                            "text": "สรุปดวงประจำวัน"
                        },
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "📍 เปลี่ยนที่จร",
                            "text": "เปลี่ยนสถานที่จร"
                        },
                        "flex": 1
                    }
                ]
            }
        },
        "quickReply": get_category_quick_reply()
    }

def build_category_flex(category_key: str, category_data: dict, asc_name: str, date_str: str, user: dict = None) -> dict:
    pb_meta = get_postback_meta(user) if user else ""
    """Build a detailed single-category horoscope flex message in Royal Obsidian & Gold theme."""
    CAT_NAMES = {
        "career": ("💼 การงาน & ธุรกิจ", "#3b82f6", "#1d4ed8"),
        "finance": ("💰 การเงิน & โชคลาภ", "#10b981", "#047857"),
        "love": ("❤️ ความรัก & เสน่ห์", "#ec4899", "#be185d"),
        "health": ("🩺 สุขภาพ & เตือนภัย", "#eab308", "#b45309"),
        "zodiac": ("☸ ผังจักรราศี 12 ช่อง", "#8b5cf6", "#6d28d9")
    }
    
    info = CAT_NAMES.get(category_key, ("🔮 คำทำนายดวงชะตา", "#f59e0b", "#d97706"))
    title, color, border_color = info[0], info[1], info[2]
    
    score = int(category_data.get("score", 75))
    if score >= 85:
        grade = "A+ (มหาเฮง)"
    elif score >= 75:
        grade = "A (ดวงเปิด)"
    elif score >= 65:
        grade = "B+ (เกณฑ์ดี)"
    elif score >= 55:
        grade = "B (ปานกลาง)"
    else:
        grade = "C+ (ต้องรอบคอบ)"
        
    theme = category_data.get("statusLabel") or category_data.get("theme") or "จังหวะดวงเปิดในทิศทางที่ดี"
    summary = category_data.get("summary") or category_data.get("forecast") or "ดวงชะตาในหมวดนี้มีเกณฑ์เคลื่อนไหวที่ดี มีโอกาสและจังหวะก้าวหน้า ให้ดำเนินชีวิตด้วยความมั่นใจและรอบคอบครับ"
    
    # Subsections (e.g. 🏢 งานประจำ, 📈 ธุรกิจ, 💡 กลยุทธ์)
    subsections = category_data.get("subsections", {})
    sub_boxes = []
    for sub_k, sub_v in subsections.items():
        sub_title = sub_v.get("title", "")
        sub_desc = sub_v.get("desc", "")
        if sub_title and sub_desc:
            sub_boxes.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#111827",
                "borderColor": "#1f2937",
                "borderWidth": "1px",
                "cornerRadius": "8px",
                "paddingAll": "10px",
                "margin": "xs",
                "contents": [
                    {"type": "text", "text": sub_title, "weight": "bold", "size": "xxs", "color": "#fef08a"},
                    {"type": "text", "text": sub_desc, "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                ]
            })
            
    # Highlights / DoList / DontList
    highlights = category_data.get("highlights", [])
    hl_contents = []
    for hl in highlights[:3]:
        if hl:
            hl_contents.append({
                "type": "text",
                "text": f"• {hl}",
                "size": "xxs",
                "color": "#94a3b8",
                "wrap": True,
                "margin": "xs"
            })
            
    do_list = category_data.get("doList", [])
    dont_list = category_data.get("dontList", [])
    action_tips = []
    if do_list and do_list[0]:
        action_tips.append({
            "type": "text",
            "text": f"✅ แนะนำ: {do_list[0]}",
            "size": "xxs",
            "color": "#86efac",
            "wrap": True,
            "margin": "xs"
        })
    if dont_list and dont_list[0]:
        action_tips.append({
            "type": "text",
            "text": f"❌ ระวัง: {dont_list[0]}",
            "size": "xxs",
            "color": "#fca5a5",
            "wrap": True,
            "margin": "xs"
        })

    HERO_URLS = {
        "career": "https://plb-horoscope.vercel.app/bear_explorer.jpg",
        "finance": "https://plb-horoscope.vercel.app/bear_fortune.jpg",
        "love": "https://plb-horoscope.vercel.app/bear_love.jpg",
        "health": "https://plb-horoscope.vercel.app/bear_wizard.jpg",
        "zodiac": "https://plb-horoscope.vercel.app/bear_explorer.jpg"
    }
    cat_hero = HERO_URLS.get(category_key, "https://plb-horoscope.vercel.app/bear_wizard.jpg")

    return {
        "type": "flex",
        "altText": f"{title} (ลัคนาราศี{asc_name}): {score}%",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": cat_hero,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": title, "weight": "bold", "color": color, "size": "md", "flex": 1},
                            {"type": "text", "text": f"{score}% ({grade})", "color": "#f8fafc", "size": "sm", "weight": "bold", "align": "end"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm",
                        "contents": [
                            make_progress_bar(score, fill_color=color, bg_color="#1e293b", height="7px")
                        ]
                    },
                    {"type": "text", "text": f"ลัคนาราศี{asc_name} • วันที่ {date_str}", "size": "xxs", "color": "#94a3b8", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#070b19",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": f"✨ เกณฑ์ดวง: {theme}", "weight": "bold", "size": "xs", "color": "#fbbf24", "wrap": True},
                    {"type": "separator", "color": "#1e293b", "margin": "sm"},
                    {"type": "text", "text": summary, "size": "xs", "color": "#e2e8f0", "wrap": True, "margin": "md"},
                    *( [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": sub_boxes
                        }
                    ] if sub_boxes else [] ),
                    *( [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "backgroundColor": "#0f172a",
                            "borderColor": "#334155",
                            "borderWidth": "1px",
                            "cornerRadius": "8px",
                            "paddingAll": "10px",
                            "contents": [
                                {"type": "text", "text": "💡 เคล็ดลับเสริมดวงประจำวัน:", "weight": "bold", "size": "xxs", "color": "#38bdf8"},
                                *action_tips
                            ]
                        }
                    ] if action_tips else [] ),
                    *( [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {"type": "text", "text": "📌 ไฮไลต์ดาวเด่น:", "weight": "bold", "size": "xxs", "color": "#94a3b8"},
                                *hl_contents
                            ]
                        }
                    ] if hl_contents else [] )
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#030712",
                "paddingAll": "12px",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#d97706",
                        "height": "sm",
                        "action": {
                            "type": "postback" if pb_meta else "message",
                            "label": "🔮 เลือกหมวดอื่น",
                            "data": f"action=select_category{pb_meta}" if pb_meta else "เลือกหมวดอยากจะดูหมวดไหน",
                            "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "postback" if pb_meta else "message",
                                    "label": "🌟 สรุปดวงรวม",
                                    "data": f"action=daily_summary{pb_meta}" if pb_meta else "สรุปดวงประจำวัน",
                                    "displayText": "สรุปดวงประจำวัน"
                                },
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#065f46",
                                "height": "sm",
                                "action": {
                                    "type": "postback" if pb_meta else "message",
                                    "label": "📊 สถิติ & กิมมิก",
                                    "data": f"action=stats{pb_meta}" if pb_meta else "สถิติ",
                                    "displayText": "สถิติดวงย้อนหลัง"
                                },
                                "flex": 1
                            }
                        ]
                    }
                ]
            }
        },
        "quickReply": get_category_quick_reply()
    }

def build_feedback_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build the 5-star accuracy rating and comment card."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    return {
        "type": "flex",
        "altText": "⭐ ประเมินความแม่นยำดวงวันนี้ (Feedback)",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#1a0f3c",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "⭐ ประเมินความแม่นยำดวงวันนี้", "weight": "bold", "color": "#c084fc", "size": "md"},
                    {"type": "text", "text": "PLB Feedback & Suggestion", "color": "#a855f7", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0d0620",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "คำทำนายวันนี้ตรงกับชีวิตของคุณแค่ไหนครับ? แตะเลือกระดับความแม่นยำได้เลย 👇", "size": "xs", "color": "#e9d5ff", "wrap": True},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#2e1065",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "⭐⭐⭐⭐⭐ แม่นมาก ตรงเป๊ะ! 🎯",
                                    "data": "action=feedback_rate&stars=5",
                                    "displayText": "ให้คะแนนความแม่นยำ: 5 ดาว ⭐⭐⭐⭐⭐"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#2e1065",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "⭐⭐⭐⭐ แม่นดี ตรงหลายเรื่อง ✨",
                                    "data": "action=feedback_rate&stars=4",
                                    "displayText": "ให้คะแนนความแม่นยำ: 4 ดาว ⭐⭐⭐⭐"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#2e1065",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "⭐⭐⭐ ปานกลาง ตรงบางเรื่อง 🔮",
                                    "data": "action=feedback_rate&stars=3",
                                    "displayText": "ให้คะแนนความแม่นยำ: 3 ดาว ⭐⭐⭐"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#2e1065",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "⭐⭐ ค่อนข้างเฉยๆ / ยังไม่ค่อยตรง 💭",
                                    "data": "action=feedback_rate&stars=2",
                                    "displayText": "ให้คะแนนความแม่นยำ: 2 ดาว ⭐⭐"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#2e1065",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "⭐ ไม่ค่อยตรงเท่าไหร่ 🌧️",
                                    "data": "action=feedback_rate&stars=1",
                                    "displayText": "ให้คะแนนความแม่นยำ: 1 ดาว ⭐"
                                }
                            }
                        ]
                    },
                    {"type": "text", "text": "💡 หลังกดดาว คุณสามารถพิมพ์ข้อความคอมเมนต์ส่งเข้ามาในแชตนี้ได้ทันที หรือแตะปุ่มด้านล่างเพื่อเขียนบนเว็บครับ", "size": "xxs", "color": "#94a3b8", "wrap": True, "margin": "md"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0d0620",
                "paddingAll": "14px",
                "paddingTop": "0px",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#7c3aed",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "📝 เปิดแบบประเมินละเอียดบนเว็บ",
                            "uri": f"{web_url}#feedback"
                        }
                    }
                ]
            }
        },
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "postback", "label": "⭐⭐⭐⭐⭐ 5 ดาว", "data": "action=feedback_rate&stars=5", "displayText": "ให้คะแนน 5 ดาว ⭐⭐⭐⭐⭐"}},
                {"type": "action", "action": {"type": "postback", "label": "⭐⭐⭐⭐ 4 ดาว", "data": "action=feedback_rate&stars=4", "displayText": "ให้คะแนน 4 ดาว ⭐⭐⭐⭐"}},
                {"type": "action", "action": {"type": "postback", "label": "⭐⭐⭐ 3 ดาว", "data": "action=feedback_rate&stars=3", "displayText": "ให้คะแนน 3 ดาว ⭐⭐⭐"}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงวันนี้"}},
                {"type": "action", "action": {"type": "uri", "label": "📝 เขียนบนเว็บ", "uri": f"{web_url}#feedback"}}
            ]
        }
    }

def build_donation_flex(
    account_name: str = "นาย เสฏฐพงศ์ เลิศสกุลบรรลือ",
    bank_info: str = "พร้อมเพย์ (PromptPay) • ttb touch",
    qr_url: str = "https://plb-horoscope.vercel.app/qr_donate.jpg",
    account_en: str = "MR SETHAPONG LERTSAKULBUNLUE"
) -> dict:
    """Build the donation / support flex card."""
    return {
        "type": "flex",
        "altText": f"☕ ข้อมูลสนับสนุนแม่หมอ PLB ({account_name})",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "☕ ร่วมสนับสนุนแม่หมอ PLB", "weight": "bold", "color": "#f59e0b", "size": "md"},
                    {"type": "text", "text": "สมทบทุนค่าเซิร์ฟเวอร์ & พัฒนาระบบดูดวงฟรี ✨", "color": "#94a3b8", "size": "xxs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "ขอบพระคุณทุกท่านจากใจจริงครับ 🙏", "weight": "bold", "size": "sm", "color": "#f8fafc"},
                    {"type": "text", "text": "เงินสนับสนุนของคุณช่วยเป็นค่าน้ำชา กาแฟ และค่าเซิร์ฟเวอร์พัฒนาระบบคำนวณโหราศาสตร์ไทยชั้นสูง เพื่อเปิดบริการฟรีแก่ทุกคนอย่างต่อเนื่องครับ ✨", "size": "xs", "color": "#cbd5e1", "wrap": True, "margin": "xs"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "14px",
                        "contents": [
                            {"type": "text", "text": "💳 บัญชีพร้อมเพย์ (PromptPay):", "size": "xs", "weight": "bold", "color": "#38bdf8"},
                            {"type": "text", "text": account_name, "size": "md", "weight": "bold", "color": "#fbbf24", "margin": "xs"},
                            {"type": "text", "text": account_en, "size": "xxs", "color": "#94a3b8", "margin": "xs"},
                            {"type": "text", "text": f"🏦 {bank_info}", "size": "xs", "color": "#38bdf8", "weight": "bold", "margin": "xs"},
                            {"type": "separator", "margin": "sm", "color": "#334155"},
                            {"type": "text", "text": "💡 แตะที่รูปภาพ QR Code ด้านบน เพื่อเปิดเต็มจอ บันทึกภาพลงมือถือ หรือสแกนผ่านแอปธนาคารได้ทันทีครับ", "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "sm"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "12px",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#f59e0b",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "🔍 เปิดรูป QR Code เต็มจอ",
                            "uri": qr_url
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "🌟 ดูสรุปดวงประจำวัน",
                            "data": "action=daily_summary",
                            "displayText": "สรุปดวงประจำวัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "👥 ชวนเพื่อนดูดวง",
                            "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                        }
                    }
                ]
            }
        }
    }

def get_category_quick_reply() -> dict:
    """Return Quick Reply items for category selection."""
    return {
        "items": [
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🥠 เสี่ยงเซียมซี",
                    "text": "เซียมซี"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🎰 ขอเลขเด็ด",
                    "text": "ขอเลขเด็ด"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "👕 สีเสื้อมงคล",
                    "text": "สีเสื้อมงคล"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "💼 การงาน",
                    "text": "การงาน"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "💰 การเงิน",
                    "text": "การเงิน"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "❤️ ความรัก",
                    "text": "ความรัก"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🩺 สุขภาพ",
                    "text": "สุขภาพ"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "📍 เปลี่ยนที่จร",
                    "text": "เปลี่ยนสถานที่จร"
                }
            }
        ]
    }

def build_share_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build an upgraded multi-channel share invitation card for LINE OA."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    return {
        "type": "flex",
        "altText": "ชวนเพื่อนมาดูดวงกับน้องหมีแม่หมอพยากรณ์ 🐻‍❄️✨",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/bear_share_3d.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "🐻‍❄️ น้องหมีชวนเพื่อนมู • ส่งต่อความเฮง ✨", "weight": "bold", "color": "#fbbf24", "size": "md"},
                    {"type": "text", "text": "แชร์ความแม่นยำให้เพื่อน ๆ เช็กดวง & รับพลังบวกฟรี!", "color": "#94a3b8", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "ส่งต่อความเฮงให้เพื่อนของคุณ 💖", "weight": "bold", "size": "sm", "color": "#f8fafc"},
                    {"type": "text", "text": "ชวนเพื่อนมารู้จักลัคนาราศีที่แท้จริง ตรวจเช็กสีเสื้อมงคล และเสี่ยงเซียมซีฟรีตลอด 24 ชั่วโมงครับ 🔮", "size": "xs", "color": "#cbd5e1", "wrap": True, "margin": "xs"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "12px",
                        "contents": [
                            {"type": "text", "text": "📲 LINE ID สำหรับเพิ่มเพื่อน:", "size": "xs", "color": "#38bdf8", "weight": "bold"},
                            {"type": "text", "text": "@374xcoto", "size": "lg", "weight": "bold", "color": "#fbbf24", "margin": "xs"},
                            {"type": "text", "text": "หรือแชร์ลิงก์: https://line.me/R/ti/p/@374xcoto", "size": "xxs", "color": "#94a3b8", "margin": "xs"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "12px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#059669",
                        "action": {
                            "type": "uri",
                            "label": "📤 แตะเพื่อแชร์ให้เพื่อนใน LINE",
                            "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "action": {
                            "type": "message",
                            "label": "🖼️ รับรูปโปสเตอร์ & QR Code",
                            "text": "โปสเตอร์"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#1e293b",
                        "action": {
                            "type": "uri",
                            "label": "🌐 Social Share Hub (FB / X / IG)",
                            "uri": f"{web_url}#share"
                        }
                    }
                ]
            }
        }
    }

def build_poster_preview_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build a poster preview Flex card with download and share links."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    return {
        "type": "flex",
        "altText": "🖼️ โปสเตอร์ชวนเพื่อนมู & QR Code น้องหมีแม่หมอ 🐻‍❄️✨",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": f"{web_url}/share_poster.jpg",
                "size": "full",
                "aspectRatio": "9:16",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": f"{web_url}/share_poster.jpg"
                }
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "14px",
                "contents": [
                    {"type": "text", "text": "🖼️ โปสเตอร์ชวนเพื่อนมู & QR Code ✨", "weight": "bold", "color": "#fbbf24", "size": "md"},
                    {"type": "text", "text": "Thai Daily Horoscope • LINE OA: @374xcoto", "color": "#94a3b8", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "เซฟรูปโปสเตอร์นี้ไปแชร์ได้ทันที 🐻‍❄️💖", "weight": "bold", "size": "sm", "color": "#f8fafc"},
                    {"type": "text", "text": "โพสต์ลง IG Story, Facebook, Twitter, Threads หรือแชร์เข้ากลุ่ม LINE ให้เพื่อน ๆ สแกนเพิ่มเพื่อนได้ง่าย ๆ เลยครับ!", "size": "xs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "12px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#f59e0b",
                        "action": {
                            "type": "uri",
                            "label": "📥 แตะเพื่อเปิด/บันทึกรูปโปสเตอร์ HD",
                            "uri": f"{web_url}/share_poster.jpg"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#059669",
                        "action": {
                            "type": "uri",
                            "label": "📤 แนะนำเพื่อนผ่าน LINE OA",
                            "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                        }
                    }
                ]
            }
        }
    }



def build_lucky_numbers_flex(user: dict, horoscope: dict, web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build a specialized luxury Flex card for lucky numbers and lottery."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    pb_meta = get_postback_meta(user) if user else ""
    lucky_info = horoscope.get("luckyInfo", {})
    nums = lucky_info.get("luckyNumbers", [9, 5, 1, 8])
    if len(nums) < 4:
        nums = [9, 5, 1, 8]
    
    user_name = user.get("name", "ผู้ใช้") if user else "ผู้ใช้"
    asc_name = horoscope.get("natalChart", {}).get("ascendant", {}).get("signName", "เมษ")
    day_lord = lucky_info.get("dailyDayLord", "พระพฤหัสบดี (๕) กำลังเทวดา 19")
    
    two_digits = [f"{nums[0]}{nums[1]}", f"{nums[1]}{nums[2]}", f"{nums[2]}{nums[3]}", f"{nums[0]}{nums[3]}"]
    three_digits = [f"{nums[0]}{nums[1]}{nums[2]}", f"{nums[1]}{nums[2]}{nums[3]}"]
    
    ausp_time = lucky_info.get("auspiciousTime", "ช่วงเช้า 09:00 - 11:00 น. (มหัทธโนฤกษ์)")
    if "(" in ausp_time:
        time_display = ausp_time.split("(")[0].strip() + " น."
        time_sub = "(" + ausp_time.split("(", 1)[1]
        if len(time_sub) > 60:
            time_sub = time_sub[:57] + "...)"
    else:
        time_display = ausp_time
        time_sub = "ฤกษ์มงคลเปิดทรัพย์"

    direction = lucky_info.get("luckyDirection", "ทิศใต้ (เสริมโชคลาภเงินทอง)")
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_fortune.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🎰 เลขเด็ด & เลขมงคลประจำวัน", "weight": "bold", "color": "#fbbf24", "size": "md", "flex": 1},
                        {"type": "text", "text": "PLB โหราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                    ]
                },
                {
                    "type": "text",
                    "text": f"คำนวณตามมหาทักษา & ดาวจร: คุณ {user_name} (ลัคนา {asc_name})",
                    "color": "#cbd5e1",
                    "size": "xs",
                    "margin": "xs",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#070b19",
            "paddingAll": "16px",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#172554",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#3b82f6",
                    "borderWidth": "1px",
                    "contents": [
                        {"type": "text", "text": "🪐 ภูมิเทวดาพระเคราะห์เสวยอายุ & ดาวจร:", "size": "xxs", "color": "#93c5fd", "weight": "bold"},
                        {"type": "text", "text": day_lord, "size": "xs", "color": "#f8fafc", "weight": "bold", "wrap": True, "margin": "xs"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#1e1b4b",
                    "cornerRadius": "14px",
                    "paddingAll": "14px",
                    "borderColor": "#ca8a04",
                    "borderWidth": "2px",
                    "alignItems": "center",
                    "contents": [
                        {"type": "text", "text": "🌟 เลขเด่นนำโชคประจำวัน 🌟", "size": "xs", "color": "#fde047", "weight": "bold"},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#d97706",
                                    "cornerRadius": "12px",
                                    "paddingAll": "8px",
                                    "width": "48px",
                                    "height": "48px",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "contents": [
                                        {"type": "text", "text": str(nums[0]), "size": "xxl", "color": "#030712", "weight": "bold"}
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#f59e0b",
                                    "cornerRadius": "12px",
                                    "paddingAll": "8px",
                                    "width": "48px",
                                    "height": "48px",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "contents": [
                                        {"type": "text", "text": str(nums[1]), "size": "xxl", "color": "#030712", "weight": "bold"}
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#fbbf24",
                                    "cornerRadius": "12px",
                                    "paddingAll": "8px",
                                    "width": "48px",
                                    "height": "48px",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "contents": [
                                        {"type": "text", "text": str(nums[2]), "size": "xxl", "color": "#030712", "weight": "bold"}
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#fef08a",
                                    "cornerRadius": "12px",
                                    "paddingAll": "8px",
                                    "width": "48px",
                                    "height": "48px",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "contents": [
                                        {"type": "text", "text": str(nums[3]), "size": "xxl", "color": "#030712", "weight": "bold"}
                                    ]
                                }
                            ]
                        },
                        {"type": "text", "text": lucky_info.get("luckyNumbersDesc", f"เลขเด่น: {nums[0]} และ {nums[1]} • เลขรอง: {nums[2]} และ {nums[3]}"), "size": "xxs", "color": "#fef08a", "margin": "sm", "wrap": True, "align": "center"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": "#0f172a",
                            "cornerRadius": "10px",
                            "paddingAll": "10px",
                            "flex": 1,
                            "borderColor": "#334155",
                            "borderWidth": "1px",
                            "contents": [
                                {"type": "text", "text": "🎯 เลขท้าย 2 ตัวเด่น", "size": "xxs", "color": "#38bdf8", "weight": "bold"},
                                {"type": "text", "text": " • ".join(two_digits), "size": "sm", "color": "#f8fafc", "weight": "bold", "margin": "xs"}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": "#0f172a",
                            "cornerRadius": "10px",
                            "paddingAll": "10px",
                            "flex": 1,
                            "borderColor": "#334155",
                            "borderWidth": "1px",
                            "contents": [
                                {"type": "text", "text": "💎 เลขมงคล 3 ตัว", "size": "xxs", "color": "#ec4899", "weight": "bold"},
                                {"type": "text", "text": " • ".join(three_digits), "size": "sm", "color": "#f8fafc", "weight": "bold", "margin": "xs"}
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#334155",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "⏰ ฤกษ์เปิดทรัพย์:", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 2},
                                {"type": "text", "text": time_display, "size": "xxs", "color": "#f8fafc", "weight": "bold", "flex": 3}
                            ]
                        },
                        {"type": "text", "text": time_sub, "size": "xxs", "color": "#94a3b8", "wrap": True, "margin": "xs"},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "xs",
                            "contents": [
                                {"type": "text", "text": "🧭 ทิศมงคลนำโชค:", "size": "xxs", "color": "#38bdf8", "weight": "bold", "flex": 2},
                                {"type": "text", "text": direction, "size": "xxs", "color": "#f8fafc", "wrap": True, "flex": 3}
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#4f46e5",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "👕 ดูสีเสื้อมงคล",
                                "data": f"action=lucky_colors{pb_meta}" if pb_meta else "สีเสื้อมงคล",
                                "displayText": "สีเสื้อมงคล"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "💰 ดูดวงการเงิน",
                                "data": f"action=category&cat=finance{pb_meta}" if pb_meta else "การเงิน",
                                "displayText": "การเงิน"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "🌟 สรุปดวงวันนี้",
                                "data": f"action=daily_summary{pb_meta}" if pb_meta else "สรุปดวงประจำวัน",
                                "displayText": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "👥 แชร์เลขให้เพื่อน",
                                "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    quick_reply = {
        "items": [
            {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
            {"type": "action", "action": {"type": "message", "label": "💰 การเงิน", "text": "การเงิน"}},
            {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวง", "text": "สรุปดวงประจำวัน"}},
            {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวด", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
            {"type": "action", "action": {"type": "message", "label": "📍 เปลี่ยนที่จร", "text": "เปลี่ยนสถานที่จร"}}
        ]
    }

    return {
        "type": "flex",
        "altText": f"🎰 เลขเด็ด & เลขมงคลประจำวัน: {nums[0]} - {nums[1]} - {nums[2]} - {nums[3]} ✨",
        "contents": bubble,
        "quickReply": quick_reply
    }


def get_color_style(raw_name: str, is_avoid: bool = False) -> dict:
    """Map Thai color name to rich color scheme and matching shirt icon key."""
    name = raw_name.lower().strip()
    if is_avoid:
        if any(k in name for k in ["ดำ", "เทา"]):
            return {"name": raw_name.strip(), "bg": "#18181b", "border": "#ef4444", "text": "#fca5a5", "key": "black"}
        if any(k in name for k in ["ม่วง"]):
            return {"name": raw_name.strip(), "bg": "#3b0764", "border": "#ef4444", "text": "#fca5a5", "key": "purple"}
        if any(k in name for k in ["แดง"]):
            return {"name": raw_name.strip(), "bg": "#450a0a", "border": "#ef4444", "text": "#fca5a5", "key": "red"}
        if any(k in name for k in ["เขียว"]):
            return {"name": raw_name.strip(), "bg": "#064e3b", "border": "#ef4444", "text": "#fca5a5", "key": "green"}
        if any(k in name for k in ["ขาว"]):
            return {"name": raw_name.strip(), "bg": "#1e293b", "border": "#ef4444", "text": "#fca5a5", "key": "white"}
        return {"name": raw_name.strip(), "bg": "#450a0a", "border": "#ef4444", "text": "#fca5a5", "key": "avoid"}

    if any(k in name for k in ["เขียว", "ตอง", "มรกต"]):
        return {"name": raw_name.strip(), "bg": "#064e3b", "border": "#10b981", "text": "#6ee7b7", "key": "green"}
    if any(k in name for k in ["ส้ม", "อิฐ"]):
        return {"name": raw_name.strip(), "bg": "#7c2d12", "border": "#f97316", "text": "#fdba74", "key": "orange"}
    if any(k in name for k in ["ทอง", "อำพัน"]):
        return {"name": raw_name.strip(), "bg": "#713f12", "border": "#eab308", "text": "#fef08a", "key": "gold"}
    if any(k in name for k in ["เหลือง", "ครีม"]):
        return {"name": raw_name.strip(), "bg": "#713f12", "border": "#facc15", "text": "#fef9c3", "key": "yellow"}
    if any(k in name for k in ["ฟ้า", "คราม"]):
        return {"name": raw_name.strip(), "bg": "#0c4a6e", "border": "#38bdf8", "text": "#bae6fd", "key": "blue"}
    if any(k in name for k in ["น้ำเงิน"]):
        return {"name": raw_name.strip(), "bg": "#1e3a8a", "border": "#3b82f6", "text": "#bfdbfe", "key": "navy"}
    if any(k in name for k in ["ชมพู", "บานเย็น", "โรสโกลด์"]):
        return {"name": raw_name.strip(), "bg": "#701a75", "border": "#ec4899", "text": "#fbcfe8", "key": "pink"}
    if any(k in name for k in ["ม่วง", "มะปราง"]):
        return {"name": raw_name.strip(), "bg": "#4c1d95", "border": "#a855f7", "text": "#e9d5ff", "key": "purple"}
    if any(k in name for k in ["แดง", "ทับทิม", "เพลิง"]):
        return {"name": raw_name.strip(), "bg": "#7f1d1d", "border": "#ef4444", "text": "#fecaca", "key": "red"}
    if any(k in name for k in ["ขาว", "เงิน", "บรอนซ์", "นวล"]):
        return {"name": raw_name.strip(), "bg": "#334155", "border": "#e2e8f0", "text": "#ffffff", "key": "white"}
    if any(k in name for k in ["ดำ", "เทา", "ควัน"]):
        return {"name": raw_name.strip(), "bg": "#18181b", "border": "#71717a", "text": "#e4e4e7", "key": "black"}
    return {"name": raw_name.strip(), "bg": "#1e293b", "border": "#64748b", "text": "#f8fafc", "key": "gold"}

def parse_color_chips(color_inputs, is_avoid: bool = False):
    """Split color strings by delimiters and convert into styled chip dictionaries."""
    raw_list = []
    if isinstance(color_inputs, str):
        raw_list = [color_inputs]
    elif isinstance(color_inputs, (list, tuple)):
        raw_list = list(color_inputs)
        
    extracted_names = []
    for item in raw_list:
        if not item:
            continue
        parts = re.split(r'[/,]|หรือ', str(item))
        for p in parts:
            cleaned = p.strip()
            if cleaned:
                extracted_names.append(cleaned)
                
    chips = []
    for name in extracted_names:
        chips.append(get_color_style(name, is_avoid=is_avoid))
    return chips

def make_color_swatches_box(color_inputs, is_avoid: bool = False, web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Generate visual shirt chips/swatches with dynamic matching color shirt icons."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    chips = parse_color_chips(color_inputs, is_avoid=is_avoid)
    if not chips:
        chips = [{"name": "ตามสะดวก", "bg": "#1e293b", "border": "#64748b", "text": "#f8fafc", "key": "gold"}]
        
    rows = []
    row = []
    for c in chips:
        shirt_icon_url = f"{web_url}/shirts/shirt_{c.get('key', 'gold')}.png"
        chip_box = {
            "type": "box",
            "layout": "horizontal",
            "backgroundColor": c["bg"],
            "cornerRadius": "14px",
            "paddingStart": "8px",
            "paddingEnd": "12px",
            "paddingTop": "6px",
            "paddingBottom": "6px",
            "borderWidth": "1.5px",
            "borderColor": c["border"],
            "alignItems": "center",
            "spacing": "xs",
            "contents": [
                {
                    "type": "image",
                    "url": shirt_icon_url,
                    "size": "xxs",
                    "aspectRatio": "1:1",
                    "aspectMode": "fit",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": c["name"],
                    "color": c["text"],
                    "weight": "bold",
                    "size": "xs",
                    "flex": 0
                }
            ]
        }
        row.append(chip_box)
        if len(row) == 2:
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": row
            })
            row = []
    if row:
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": row
        })
        
    if len(rows) == 1:
        rows[0]["margin"] = "sm"
        return rows[0]
    else:
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "margin": "sm",
            "contents": rows
        }

def build_lucky_colors_flex(user: dict, horoscope: dict, web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build a specialized luxury Flex card for daily lucky shirt colors with visual color chips."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    pb_meta = get_postback_meta(user) if user else ""
    lucky_info = horoscope.get("luckyInfo", {})
    user_name = user.get("name", "ผู้ใช้") if user else "ผู้ใช้"
    asc_name = horoscope.get("natalChart", {}).get("ascendant", {}).get("signName", "เมษ")
    day_lord = lucky_info.get("dailyDayLord", "พระพฤหัสบดี (๕) กำลังเทวดา 19")

    ausp_colors = lucky_info.get("auspiciousColors", {})
    work_colors = ausp_colors.get("work", ["สีฟ้าสว่าง"])
    wealth_colors = ausp_colors.get("wealth", ["สีแดงทับทิม"])
    love_colors = ausp_colors.get("love", ["สีส้มประกายทอง"])
    avoid_colors = lucky_info.get("inauspiciousColors", ["สีม่วง / ดำ"])

    amulet = lucky_info.get("auspiciousAmulet", "หินไหมทอง, อัญมณีประจำวัน")
    good_deed = lucky_info.get("goodDeedAdvice", "ทำบุญค่าน้ำค่าไฟ เติมน้ำมันตะเกียง")

    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_wardrobe.jpg",
            "size": "full",
            "aspectRatio": "16:9",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "👕 ตารางสีเสื้อมงคลประจำวัน", "weight": "bold", "color": "#fbbf24", "size": "md", "flex": 1},
                        {"type": "text", "text": "มหาทักษาจร", "color": "#94a3b8", "size": "xxs", "align": "end"}
                    ]
                },
                {
                    "type": "text",
                    "text": f"เสริมบารมี & เสริมเฮง: คุณ {user_name} (ลัคนา {asc_name})",
                    "color": "#cbd5e1",
                    "size": "xs",
                    "margin": "xs",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#070b19",
            "paddingAll": "16px",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#172554",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#3b82f6",
                    "borderWidth": "1px",
                    "contents": [
                        {"type": "text", "text": "🪐 กำลังดาวพระเคราะห์ประจำวัน:", "size": "xxs", "color": "#93c5fd", "weight": "bold"},
                        {"type": "text", "text": day_lord, "size": "xs", "color": "#f8fafc", "weight": "bold", "wrap": True, "margin": "xs"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#3b82f6",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "alignItems": "center",
                            "contents": [
                                {"type": "text", "text": "💼 การงาน & อำนาจบารมี (เดช)", "size": "xs", "color": "#60a5fa", "weight": "bold", "flex": 1},
                                {"type": "text", "text": "🌟 ดีเยี่ยม", "size": "xxs", "color": "#93c5fd"}
                            ]
                        },
                        make_color_swatches_box(work_colors, is_avoid=False, web_url=web_url)
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#06281e",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#10b981",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "alignItems": "center",
                            "contents": [
                                {"type": "text", "text": "💰 เงินทอง & โชคลาภ (ศรี)", "size": "xs", "color": "#34d399", "weight": "bold", "flex": 1},
                                {"type": "text", "text": "💵 รับทรัพย์", "size": "xxs", "color": "#86efac"}
                            ]
                        },
                        make_color_swatches_box(wealth_colors, is_avoid=False, web_url=web_url)
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#2e1065",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#ec4899",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "alignItems": "center",
                            "contents": [
                                {"type": "text", "text": "💖 เสน่ห์ & เมตตามหานิยม (มนตรี)", "size": "xs", "color": "#f472b6", "weight": "bold", "flex": 1},
                                {"type": "text", "text": "💕 ผู้ใหญ่เอ็นดู", "size": "xxs", "color": "#fbcfe8"}
                            ]
                        },
                        make_color_swatches_box(love_colors, is_avoid=False, web_url=web_url)
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#450a0a",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#ef4444",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "alignItems": "center",
                            "contents": [
                                {"type": "text", "text": "⛔ สีกาลกิณี (ควรหลีกเลี่ยง)", "size": "xs", "color": "#f87171", "weight": "bold", "flex": 1},
                                {"type": "text", "text": "⚠️ ห้ามใส่", "size": "xxs", "color": "#fca5a5", "weight": "bold"}
                            ]
                        },
                        make_color_swatches_box(avoid_colors, is_avoid=True, web_url=web_url)
                    ]
                },

                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "contents": [
                        {"type": "text", "text": f"💎 ของมงคลเสริมราศี: {amulet}", "size": "xxs", "color": "#cbd5e1", "wrap": True},
                        {"type": "text", "text": f"🕊️ เสริมบารมี: {good_deed}", "size": "xxs", "color": "#94a3b8", "wrap": True, "margin": "xs"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "🎰 ขอเลขเด็ด",
                                "data": f"action=lucky_numbers{pb_meta}" if pb_meta else "ขอเลขเด็ด",
                                "displayText": "ขอเลขเด็ด"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#1d4ed8",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "💼 ดูหมวดการงาน",
                                "data": f"action=category&cat=career{pb_meta}" if pb_meta else "การงาน",
                                "displayText": "การงาน"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "postback" if pb_meta else "message",
                                "label": "🌟 สรุปดวงวันนี้",
                                "data": f"action=daily_summary{pb_meta}" if pb_meta else "สรุปดวงประจำวัน",
                                "displayText": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "👥 แชร์สีเสื้อให้เพื่อน",
                                "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    quick_reply = {
        "items": [
            {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
            {"type": "action", "action": {"type": "message", "label": "💼 การงาน", "text": "การงาน"}},
            {"type": "action", "action": {"type": "message", "label": "💰 การเงิน", "text": "การเงิน"}},
            {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวง", "text": "สรุปดวงประจำวัน"}},
            {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวด", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
            {"type": "action", "action": {"type": "message", "label": "📍 เปลี่ยนที่จร", "text": "เปลี่ยนสถานที่จร"}}
        ]
    }

    return {
        "type": "flex",
        "altText": f"👕 ตารางสีเสื้อมงคลประจำวัน เสริมเฮงการงาน-การเงิน-ความรัก ✨",
        "contents": bubble,
        "quickReply": quick_reply
    }


def build_noon_reminder_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build cute polar bear midday noon reminder and invitation flex card."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_fortune.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🍱 พักเที่ยงเติมพลัง & เช็กดวงบ่ายนี้ ✨", "weight": "bold", "color": "#fbbf24", "size": "md", "flex": 1},
                        {"type": "text", "text": "PLB โหราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                    ]
                },
                {
                    "type": "text",
                    "text": "เติมความสดใสยามบ่าย วาสนาเปิดรับทรัพย์ 🐻‍❄️💖",
                    "color": "#cbd5e1",
                    "size": "xs",
                    "margin": "xs"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#070b19",
            "paddingAll": "16px",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#1e1b4b",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#6366f1",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "พักสายตาสักนิด ทานข้าวเที่ยงให้อร่อยนะคร้าบ! 🍱\nบ่ายนี้ดาวศุภเคราะห์โคจรหนุนนำ แวะมาเช็กดวง เลขเด่น และสีเสื้อมงคลเสริมพลังใจกันน้า 🐻‍❄️✨",
                            "size": "xs",
                            "color": "#e0e7ff",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#334155",
                    "borderWidth": "1px",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🎰 เลขเด่นประจำวัน:", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "คำนวณตามมหาทักษาเปิดทรัพย์", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "👕 สีเสื้อมงคล:", "size": "xxs", "color": "#818cf8", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "เสริมเดช เสริมศรี เสริมมนตรีบ่ายนี้", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🌟 สรุปดวงแม่นยำ:", "size": "xxs", "color": "#34d399", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "ตำแหน่งดาวจริงตามพิกัดจังหวัดของคุณ", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "💡 กดปุ่มด้านล่างเพื่อดูดวง หรือชวนเพื่อน ๆ มาดูดวงด้วยกันได้เลยครับ 👇",
                    "size": "xxs",
                    "color": "#94a3b8",
                    "wrap": True,
                    "margin": "xs"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🌟 สรุปดวงวันนี้",
                                "text": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#059669",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🎰 ขอเลขเด็ด",
                                "text": "ขอเลขเด็ด"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "👕 สีเสื้อมงคล",
                                "text": "สีเสื้อมงคล"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "👥 ชวนเพื่อนดูดวง",
                                "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    return {
        "type": "flex",
        "altText": "🍱 พักเที่ยงแล้ว ทานข้าวให้อร่อยนะคร้าบ! อย่าลืมแวะเช็กดวงบ่ายนี้กับน้องหมี PLB 🐻‍❄️✨",
        "contents": bubble,
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงวันนี้"}},
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวด", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                {"type": "action", "action": {"type": "uri", "label": "👥 ชวนเพื่อนดูดวง", "uri": "https://line.me/R/nv/recommendOA/@374xcoto"}}
            ]
        }
    }


# ==============================================================================
# RETENTION FEATURES: MORNING ROUTINE, LOTTERY SPECIAL, SIAMSEE, & WALLPAPERS
# ==============================================================================

def build_morning_reminder_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build refreshing 07:00 AM Morning Routine reminder flex card."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    thai_months = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                   "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    day_name = thai_days[now_th.weekday()]
    date_str = f"วัน{day_name}ที่ {now_th.day} {thai_months[now_th.month]} {now_th.year + 543}"

    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_fortune.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "☀️ อรุณสวัสดิ์รับทรัพย์ยามเช้า 07:00 น.", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                        {"type": "text", "text": "PLB โหราศาสตร์", "color": "#94a3b8", "size": "xxs", "align": "end"}
                    ]
                },
                {"type": "text", "text": f"เปิดดวงเสริมพลังใจ {date_str} ✨", "color": "#e2e8f0", "size": "xs", "margin": "xs"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#1e1b4b",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#6366f1",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "ตื่นเช้ามาเติมพลังใจ รับพลังบวกจากดาวศุภเคราะห์วันนี้กันครับ! 🌤️\nเลือกใส่เสื้อสีมงคลก่อนออกจากบ้าน พร้อมเช็กดวงชะตาและฤกษ์เวลาทองของวันนี้ได้เลยน้า 🐻‍❄️✨",
                            "size": "xs",
                            "color": "#e0e7ff",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#334155",
                    "borderWidth": "1px",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "👕 สีเสื้อมงคลวันนี้:", "size": "xxs", "color": "#818cf8", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "ใส่ถูกโฉลก เสริมทรัพย์ เสน่ห์ อำนาจ", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "⏰ ฤกษ์นาทีทอง:", "size": "xxs", "color": "#34d399", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "ช่วงเวลาดาวหนุนนำ เหมาะคุยงาน เจรจา", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🎰 เลขเด่นประจำวัน:", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "คำนวณตามสูตรมหาทักษาเทวราช", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "xs",
                    "contents": [
                        {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ปลอดภัย 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#4f46e5",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "👕 สีเสื้อมงคล",
                                "text": "สีเสื้อมงคล"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🌟 สรุปดวงวันนี้",
                                "text": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#065f46",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🎰 ขอเลขเด็ด",
                                "text": "ขอเลขเด็ด"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🥠 เสี่ยงเซียมซี",
                                "text": "เซียมซี"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "color": "#1e293b",
                    "height": "sm",
                    "margin": "xs",
                    "action": {
                        "type": "uri",
                        "label": "👥 ชวนเพื่อนดูดวงยามเช้า",
                        "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                    }
                }
            ]
        }
    }

    return {
        "type": "flex",
        "altText": f"☀️ อรุณสวัสดิ์ครับ! เช็กสีเสื้อมงคล & ดวงประจำวัน {date_str} กับน้องหมี PLB 🐻‍❄️✨",
        "contents": bubble,
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "message", "label": "🎁 วอลเปเปอร์", "text": "วอลเปเปอร์"}}
            ]
        }
    }


def build_lottery_special_flex(web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build high-energy Special Edition Lottery Flex Card for 1st & 16th of month."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    thai_months = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                   "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    date_str = f"งวดประจำวันที่ {now_th.day} {thai_months[now_th.month]} {now_th.year + 543}"

    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_fortune.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#052e16",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🎫 พิเศษ! วันแห่งโชคลาภมหาศาล", "weight": "bold", "color": "#fef08a", "size": "sm", "flex": 1},
                        {"type": "text", "text": "มหาลาภ 1 & 16", "color": "#86efac", "size": "xxs", "align": "end", "weight": "bold"}
                    ]
                },
                {"type": "text", "text": f"เปิดขุมทรัพย์ดาวเศรษฐี {date_str} 💰✨", "color": "#bbf7d0", "size": "xs", "margin": "xs"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#14532d",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#22c55e",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "วันนี้วันแห่งความหวังและเศรษฐีใหม่! 🎉\nน้องหมี PLB รวมเลขเทวราช ทิศเปิดทรัพย์ และเคล็ดลับดึงดูดโชคใหญ่ตามตำแหน่งดวงดาวมาให้แล้ว ขอให้เฮง ๆ ปัง ๆ รวย ๆ ถูกรางวัลใหญ่ถ้วนหน้าครับ! 🐻‍❄️💰",
                            "size": "xs",
                            "color": "#f0fdf4",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#334155",
                    "borderWidth": "1px",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🔢 เลขเด่นงวดนี้:", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "คำนวณตามดาวพระเคราะห์ประจำงวด", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🧭 ทิศมหาราชรับทรัพย์:", "size": "xxs", "color": "#38bdf8", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "หันหน้ารับพลังโชคลาภก่อนหยิบสลาก", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "⏰ ฤกษ์เวลาเสี่ยงโชค:", "size": "xxs", "color": "#4ade80", "weight": "bold", "flex": 2},
                                {"type": "text", "text": "ช่วงเวลาดาวจันทร์ส่งกระแสการเงิน", "size": "xxs", "color": "#f8fafc", "flex": 3}
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#172554",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#3b82f6",
                    "borderWidth": "1px",
                    "contents": [
                        {"type": "text", "text": "💡 คาถาเปิดคลังทรัพย์เสริมโชค:", "size": "xxs", "color": "#93c5fd", "weight": "bold"},
                        {"type": "text", "text": "ตั้งจิตสงบ ตั้งนะโม 3 จบ แล้วสวด 'นะชาลีติ ประสิทธิลาภา' 9 จบ เพื่อเปิดประตูวาสนาและดึงดูดทรัพย์เข้ากระเป๋าครับ ✨", "size": "xxs", "color": "#e0e7ff", "wrap": True, "margin": "xs"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#291334",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#f43f5e",
                    "borderWidth": "1px",
                    "action": {
                        "type": "message",
                        "text": "สนับสนุนแม่หมอ"
                    },
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "alignItems": "center",
                            "contents": [
                                {"type": "text", "text": "💖 แอบกระซิบจากใจน้องหมี:", "size": "xxs", "color": "#fda4af", "weight": "bold", "flex": 1},
                                {"type": "text", "text": "เลี้ยงกาแฟ ☕", "size": "xxs", "color": "#fb7185", "align": "end"}
                            ]
                        },
                        {
                            "type": "text",
                            "text": "ถ้าใครถูกหวยงวดนี้ อย่าลืมแวะมาสนับสนุนแม่หมอนะ 5555 ขอให้เฮง ๆ รวย ๆ ถ้วนหน้าครับ! 🐻‍❄️💸✨",
                            "size": "xxs",
                            "color": "#ffe4e6",
                            "wrap": True,
                            "margin": "xs"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "xs",
                    "contents": [
                        {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ปลอดภัย 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#059669",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🎰 ขอเลขเด็ดงวดนี้",
                                "text": "ขอเลขเด็ด"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🌟 ดูสรุปดวงวันนี้",
                                "text": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#4338ca",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "👕 สีเสื้อมงคลเรียกทรัพย์",
                                "text": "สีเสื้อมงคล"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🥠 เสี่ยงเซียมซีมหาลาภ",
                                "text": "เซียมซี"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "margin": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#831843",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "☕ สนับสนุนแม่หมอ",
                                "text": "สนับสนุนแม่หมอ"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "👥 ชวนเพื่อนรับโชค",
                                "uri": "https://line.me/R/nv/recommendOA/@374xcoto"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    return {
        "type": "flex",
        "altText": f"🎫 พิเศษวันหวยออก! ถ้าใครถูกหวยอย่าลืมสนับสนุนแม่หมอนะ 5555 เปิดเลขเด็ด {date_str} กับน้องหมี PLB 💰✨",
        "contents": bubble,
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "☕ สนับสนุนแม่หมอ", "text": "สนับสนุนแม่หมอ"}},
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "uri", "label": "👥 ชวนเพื่อนรับโชค", "uri": "https://line.me/R/nv/recommendOA/@374xcoto"}}
            ]
        }
    }


# ==============================================================================
# SIAMSEE DATABASE (28 Authentic Traditional Thai Fortune Stanzas)
# ==============================================================================
SIAMSEE_DATA = {
    1: {
        "title": "เทวาประสิทธิ์มหาลาภ",
        "grade": "ยอดเยี่ยม (ดีมาก 🌟🌟🌟)",
        "poem": "ใบที่หนึ่ง พึงคิด พินิจจิต\nเทวฤทธิ์ สถิตมั่น บันดาลผล\nลาภลอยเด่น เงินทอง ไหลหลั่งดล\nจะสุขล้น สมหวัง ดั่งใจปอง",
        "work": "การงานรุ่งโรจน์ ได้รับการสนับสนุนจากผู้ใหญ่ เจรจาราบรื่นสำเร็จทุกประการ",
        "wealth": "การเงินคล่องตัว มีเกณฑ์ได้ลาภลอย หรือเงินก้อนที่รอคอยมานาน",
        "love": "คนโสดจะได้พบคนถูกใจที่มีฐานะดี คนมีคู่รักใคร่ปรองดองเข้าใจกัน",
        "health": "สุขภาพแข็งแรง สดชื่นกระปรี้กระเปร่า ไร้โรคภัยเบียดเบียน",
        "caution": "อย่าประมาทเรื่องคำพูดกับคนใกล้ชิด รักษาความดีไว้เป็นเกราะคุ้มครอง"
    },
    2: {
        "title": "นาวาลอยล่องตามลม",
        "grade": "ดีมาก (ราบรื่น 🌟🌟)",
        "poem": "ใบที่สอง ต้องจิตต์ คิดการใหญ่\nแล่นเรือไป ตามสายชล ผลประเสริฐ\nอุปสรรค ผ่อนคลาย มลายเตลิด\nความรุ่งเรือง บังเกิด สู่ชีวา",
        "work": "งานโปรเจกต์ที่ติดขัดจะเริ่มคลี่คลาย มีโอกาสขยับขยายหรือเดินทางแล้วได้ดี",
        "wealth": "รายได้เข้ามาสม่ำเสมอ หมุนเงินได้ทัน ไม่มีปัญหาหนี้สินรบกวน",
        "love": "ความรักเรียบง่ายแต่มั่นคง มีโอกาสได้เดินทางท่องเที่ยวร่วมกัน",
        "health": "ระวังเรื่องภูมิแพ้อากาศหรือหวัดเล็กน้อย พักผ่อนให้เพียงพอ",
        "caution": "ทำอะไรตามขั้นตอน อย่าใจร้อนลัดวงจรจะสำเร็จยั่งยืน"
    },
    3: {
        "title": "ปักหลักมั่นคงดั่งขุนเขา",
        "grade": "ดีเยี่ยม (มั่นคง 🌟🌟🌟)",
        "poem": "ใบที่สาม ความเพียร จะเรียนผล\nสร้างตัวตน ดั่งภูผา สง่าศรี\nศัตรูพ่าย มิตรรัก ภักดีมี\nตลอดปี มีสุข ไร้ทุกข์ภัย",
        "work": "หน้าที่การงานมั่นคง ได้รับความไว้วางใจให้คุมงานสำคัญ มีเกณฑ์เลื่อนขั้น",
        "wealth": "มีเกณฑ์ได้ทรัพย์สินชิ้นใหญ่ เช่น ที่ดิน บ้าน หรือยานพาหนะ",
        "love": "คู่ครองเป็นหลักยึดเหนี่ยวจิตใจ ช่วยเหลือเกื้อกูลกันสร้างอนาคต",
        "health": "ระวังอาการปวดเมื่อยหลังหรือไหล่จากการทำงานหนัก ยืดเหยียดบ้าง",
        "caution": "หนักแน่นเข้าไว้ อย่าหวั่นไหวกับคำนินทาของคนรอบข้าง"
    },
    4: {
        "title": "แสงทองส่องสว่างนำทาง",
        "grade": "ดีมาก (มีทางออก 🌟🌟)",
        "poem": "ใบที่สี่ ที่มืดมน จะพ้นผ่าน\nสุริยาน ส่องหล้า พาสดใส\nปัญหาใด ติดขัด จัดการได้\nเริ่มต้นใหม่ รุ่งโรจน์ ชัชวาล",
        "work": "ปัญหาที่ค้างคาจะพบทางออก มีกัลยาณมิตรหรือที่ปรึกษาเข้ามาช่วยชี้แนะ",
        "wealth": "เริ่มมีช่องทางสร้างรายได้ใหม่ ๆ การลงทุนเริ่มเห็นผลกำไร",
        "love": "คนโสดเปิดใจแล้วจะพบคนอบอุ่น คนมีคู่ปรับความเข้าใจกันได้ดี",
        "health": "สุขภาพจิตดีขึ้น ความเครียดลดลง ร่างกายฟื้นตัวได้ไว",
        "caution": "อย่าลังเลเมื่อโอกาสมาถึง กล้าตัดสินใจแล้วลงมือทำทันที"
    },
    5: {
        "title": "เกษตรสมบูรณ์ผลิดอกออกผล",
        "grade": "ดีเยี่ยม (รับทรัพย์ 🌟🌟🌟)",
        "poem": "ใบที่ห้า ปลูกพืช ย่อมชื่นชื่น\nผลดกื่น เต็มกิ่ง ยิ่งสุขสันต์\nที่เหนื่อยยาก ลำบากแต่ ปางบรรพ์\nบัดนี้พลัน รับทรัพย์ นับคณนา",
        "work": "สิ่งที่ลงทุนลงแรงไว้เริ่มผลิดอกออกผล ได้รับคำชมและผลตอบแทนคุ้มค่า",
        "wealth": "การเงินโดดเด่นมาก ค้าขายกำไรดี มีเงินเก็บเพิ่มพูน",
        "love": "ความรักสุกงอม อาจมีข่าวดีเรื่องงานมงคลหรือสมาชิกใหม่",
        "health": "ระวังเรื่องน้ำหนักตัวหรือตามใจปากเกินไป ควบคุมอาหารหวานมัน",
        "caution": "แบ่งปันทำบุญทำทานเพื่อเสริมบารมีและต่อยอดโชคลาภ"
    },
    6: {
        "title": "เต่าทองขึ้นฝั่งพ้นภัย",
        "grade": "ปานกลางถึงดี (ปลอดภัย 🌟)",
        "poem": "ใบที่หก ตกน้ำ ยังรอดได้\nเต่าทองไคล ขึ้นฝั่ง สิ้นกังขา\nมีเคราะห์ร้าย เทพช่วย ด้วยเมตตา\nพ้นธารา สู่แดน แสนรื่นรมย์",
        "work": "ระวังเรื่องเอกสารสัญญาหรือข้อผิดพลาดเล็กน้อย แต่จะผ่านพ้นไปได้ด้วยดี",
        "wealth": "รายจ่ายค่อนข้างเยอะ ให้วางแผนงบประมาณรอบคอบ อย่าเพิ่งให้ใครยืมเงิน",
        "love": "คนโสดยังต้องดูใจไปก่อน คนมีคู่ควรพูดจากันด้วยเหตุผลมากกว่าอารมณ์",
        "health": "ระวังอุบัติเหตุจากการลื่นล้ม หรืออาการเจ็บข้อเท้า",
        "caution": "มีสติทุกย่างก้าว อย่าด่วนตัดสินใจเรื่องสำคัญโดยไม่ไตร่ตรอง"
    },
    7: {
        "title": "นกการเวกส่งเสียงประสาน",
        "grade": "ดีมาก (วาจามหาเสน่ห์ 🌟🌟)",
        "poem": "ใบที่เจ็ด เสียงใส ดั่งนกสวรรค์\nเจรจานั้น พาที มีมนต์ขลัง\nคนนิยม ชมชอบ พร้อมรับฟัง\nสำเร็จดั่ง ปรารถนา สารพัน",
        "work": "งานด้านการขาย การพูด การเจรจา หรือการตลาดโดดเด่นมาก ได้รับความเชื่อถือ",
        "wealth": "เงินทองไหลมาจากคำพูดและการติดต่อสื่อสาร มีลูกค้ารายใหม่เข้ามา",
        "love": "เสน่ห์แรง มีคนเข้ามาทักทายและอยากทำความรู้จักหลายคน",
        "health": "ระวังเรื่องเจ็บคอ เสียงแห้ง หรือร้อนใน ดื่มน้ำอุ่นมาก ๆ",
        "caution": "พูดแต่สิ่งที่เป็นความจริงและเป็นประโยชน์ จะดึงดูดโชคลาภไม่ขาดสาย"
    },
    8: {
        "title": "พุทธานุภาพคุ้มเกล้า",
        "grade": "ยอดเยี่ยม (แคล้วคลาด 🌟🌟🌟)",
        "poem": "ใบที่แปด พระคุ้ม บุญรักษา\nกุศลพา แคล้วคลาด ประหลาดล้ำ\nสิ่งศักดิ์สิทธิ์ สถิตเคียง เลี้ยงอุปถัมภ์\nไม่ตกต่ำ เจริญสุข ทุกคืนวัน",
        "work": "แม้มีคนอิจฉาหรือคิดร้ายก็ทำอะไรไม่ได้ ความดีจะปกป้องและหนุนให้ก้าวหน้า",
        "wealth": "มีโชคจากการทำบุญหรือสิ่งศักดิ์สิทธิ์ให้ลาภ ได้เงินมาอย่างอัศจรรย์",
        "love": "เจอเนื้อคู่ที่มีศีลเสมอกัน ชวนกันทำบุญสร้างบารมี",
        "health": "โรคภัยไข้เจ็บที่เคยเป็นจะทุเลาลง สุขภาพกายใจเบิกบาน",
        "caution": "หมั่นสวดมนต์ไหว้พระ อุทิศส่วนกุศลให้เจ้ากรรมนายเวรเป็นนิจ"
    },
    9: {
        "title": "มังกรผงาดเหนือเมฆา",
        "grade": "ดีเลิศ (บารมีสูง 🌟🌟🌟)",
        "poem": "ใบที่เก้า มังกร ทะยานฟ้า\nเปี่ยมเดชา บารมี ศรีผ่องใส\nคิดการใด สมจิต สัมฤทธิ์ไว\nเกียรติยศเกรียงไกร ลือนาม",
        "work": "มีโอกาสได้รับตำแหน่งใหญ่ หรือได้รับเกียรติบัตร รางวัล ความสำเร็จยิ่งใหญ่",
        "wealth": "การเงินฐานะดีขึ้นอย่างก้าวกระโดด ลงทุนสิ่งใดได้กำไรเกินคาด",
        "love": "คนรักให้เกียรติและสนับสนุนในทุกด้าน เป็นคู่บุญบารมี",
        "health": "ระวังเรื่องสายตาล้าจากการใช้หน้าจอนาน พักสายตาเป็นระยะ",
        "caution": "ยิ่งสูงยิ่งต้องอ่อนน้อมถ่อมตน จะมีผู้คนรักใคร่และค้ำชูยืนยาว"
    },
    10: {
        "title": "สายธารรินไหลชุ่มฉ่ำ",
        "grade": "ดี (สุขสงบ 🌟🌟)",
        "poem": "ใบที่สิบ สายน้ำ ฉ่ำฤดี\nความเยือกเย็น เกิดมี ในดวงจิต\nดับไฟร้อน ผ่อนคลาย ร้ายไม่คิด\nเนรมิต ความสุข ไร้ทุกข์ทน",
        "work": "บรรยากาศในที่ทำงานราบรื่น ได้รับความร่วมมือที่ดีจากเพื่อนร่วมงาน",
        "wealth": "การเงินมีกินมีใช้ไม่ขัดสน รายได้คงที่ เหมาะแก่การออมเงิน",
        "love": "ความรักราบรื่นเข้าใจกันดี ไร้เรื่องทะเลาะเบาะแว้ง",
        "health": "สุขภาพโดยรวมดี ระวังเพียงเรื่องระบบทางเดินปัสสาวะ ดื่มน้ำเยอะ ๆ",
        "caution": "ใจเย็นเข้าไว้ การใช้ความประนีประนอมจะชนะทุกสถานการณ์"
    },
    11: {
        "title": "ต้นไม้ใหญ่รับลมฝน",
        "grade": "ปานกลาง (ต้องอดทน 🌟)",
        "poem": "ใบสิบเอ็ด ลมพัด สะบัดกิ่ง\nอย่าไหวติง ยึดราก ฝากแผ่นผา\nอดทนรอ ตะวัน คืนกลับมา\nบุปผา บานสะพรั่ง ดังเดิม",
        "work": "อาจเจอแรงกดดันหรือภาระงานที่เพิ่มขึ้น ขอให้อดทนแล้วจะผ่านไปได้ด้วยดี",
        "wealth": "งดการเสี่ยงโชคก้อนโต ชะลอการลงทุนใหญ่ เน้นเก็บรักษาเงินสดไว้ก่อน",
        "love": "ควรระวังเรื่องอารมณ์หงุดหงิดใส่กัน ให้เวลากันและกันสักนิด",
        "health": "ระวังเรื่องความเครียดสะสม ปวดหัว ไมเกรน ควรหางานอดิเรกผ่อนคลาย",
        "caution": "ความอดทนคือยาวิเศษ ฟ้าหลังฝนย่อมสดใสเสมอ"
    },
    12: {
        "title": "แก้วสารพัดนึกสมหวัง",
        "grade": "ยอดเยี่ยม (สมปรารถนา 🌟🌟🌟)",
        "poem": "ใบสิบสอง ดั่งแก้ว มณีโชติ\nสว่างโรจน์ สมมาด ปรารถนา\nขอสิ่งใด ได้สม ดั่งวาจา\nวาสนา พาชื่น รื่นรมย์ใจ",
        "work": "งานที่ตั้งใจทำจะประสบความสำเร็จเกินเป้า การสอบแข่งขันจะได้ผลดีเยี่ยม",
        "wealth": "โชคลาภโดดเด่นมาก มีเงินทองไหลมาเทมา หยิบจับอะไรก็เป็นเงินเป็นทอง",
        "love": "ความรักสมหวัง คนที่แอบชอบเริ่มมีใจตอบ คนมีคู่รักหวานชื่น",
        "health": "สุขภาพดีเยี่ยม แข็งแรงสดใสทั้งกายและใจ",
        "caution": "รักษาความกตัญญูต่อผู้มีพระคุณ จะช่วยให้บารมีคงอยู่ยืนยาว"
    }
}

# Fill remaining stanzas up to 28 with authentic Thai themes
_EXT_THEMES = [
    (13, "เรือทองขนสมบัติ", "ดีมาก 🌟🌟", "การค้าขายต่างถิ่นได้กำไรดี", "ได้เงินก้อนจากการค้า", "พบรักทางไกล", "ระวังแพ้อาหาร"),
    (14, "พระจันทร์วันเพ็ญ", "ดีเยี่ยม 🌟🌟🌟", "งานสร้างสรรค์โดดเด่น", "การเงินสว่างไสวมีลาภ", "ความรักโรแมนติก", "สดชื่นแจ่มใส"),
    (15, "ดอกบัวเหนือน้ำ", "ยอดเยี่ยม 🌟🌟🌟", "ปัญญาเฉียบแหลมงานลุล่วง", "เงินทองสะอาดไร้มลทิน", "คนรักคอยช่วยเหลือ", "สุขภาพกายใจผ่องใส"),
    (16, "ม้าศึกทะยานไกล", "ดี 🌟🌟", "งานก้าวหน้าต้องลุย", "เงินคล่องตัวจากการเดินทาง", "คนรักให้กำลังใจ", "ระวังปวดกล้ามเนื้อ"),
    (17, "ร่มโพธิ์ร่มไทร", "ดีเยี่ยม 🌟🌟🌟", "ผู้ใหญ่ให้ความเมตตา", "มีคนช่วยค้ำจุนการเงิน", "ครอบครัวอบอุ่น", "แข็งแรงสมบูรณ์"),
    (18, "คันฉ่องส่องความจริง", "ปานกลาง 🌟", "ตรวจสอบเอกสารให้ถี่ถ้วน", "ระวังรายจ่ายจุกจิก", "เปิดใจคุยกันตรงๆ", "พักสายตาบ่อยๆ"),
    (19, "ฝนทิพย์ชโลมดิน", "ดีมาก 🌟🌟", "โครงการใหม่เริ่มเดินหน้า", "เริ่มมีสภาพคล่องดีขึ้น", "ความรักฟื้นฟูสดชื่น", "สดชื่นกระปรี้กระเปร่า"),
    (20, "ธงชัยโบกสะบัด", "ยอดเยี่ยม 🌟🌟🌟", "ชนะการแข่งขัน ชนะประมูล", "ได้รับเงินรางวัล โบนัส", "คนรักยกย่องภูมิใจ", "พลังงานเต็มเปี่ยม"),
    (21, "หงส์ร่อนลงคอน", "ดีเยี่ยม 🌟🌟🌟", "งานสง่างามมีเกียรติ", "การเงินมั่นคงมีเกณฑ์สะสม", "พบคนถูกใจมีระดับ", "ระวังเรื่องกระดูกข้อเท้า"),
    (22, "ช้างมงคลประสิทธิ์", "ดีเลิศ 🌟🌟🌟", "ได้ทำงานใหญ่คุมบริวาร", "การเงินมั่งคั่งมีมรดก", "คู่ครองเป็นคนมั่นคง", "แข็งแรงดั่งพญาคชสาร"),
    (23, "สายรุ้งหลังพายุ", "ดีมาก 🌟🌟", "เรื่องร้ายผ่านพ้นความดีมา", "หนี้สินเริ่มคลี่คลาย", "เข้าใจกันลึกซึ้งยิ่งขึ้น", "หายจากไข้หวัด"),
    (24, "เพชรน้ำเอกประกาย", "ยอดเยี่ยม 🌟🌟🌟", "ผลงานได้รับการยอมรับสูงสุด", "รับทรัพย์ก้อนโตมีโชค", "ความรักมั่นคงเลอค่า", "สุขภาพแข็งแรงสมบูรณ์"),
    (25, "ระฆังทองก้องกังวาน", "ดีมาก 🌟🌟", "ชื่อเสียงกระจายไปไกล", "มีลูกค้าเข้ามาต่อเนื่อง", "มีเสน่ห์ดึงดูดใจ", "ระวังเรื่องเสียงแหบ"),
    (26, "สะพานเชื่อมสองฝั่ง", "ดี 🌟🌟", "การเจรจาปรองดองสำเร็จ", "หมุนเงินได้ทันราบรื่น", "ปรับความเข้าใจกับคนรัก", "ระวังเมื่อยล้าหลัง"),
    (27, "กำแพงแก้วคุ้มภัย", "ดีเยี่ยม 🌟🌟🌟", "ไร้อุปสรรคขัดขวาง", "การเงินปลอดภัยไม่รั่วไหล", "ความรักอบอุ่นปลอดภัย", "ไร้โรคาพยาธิ"),
    (28, "มหาจักรพรรดิ์สถาพร", "ยอดเยี่ยมที่สุด 🌟🌟🌟🌟", "บารมีสูงสุดคิดการใดสำเร็จ", "คลังทรัพย์เปิดรับมหาศาล", "คู่บุญบารมีครองรักยั่งยืน", "อายุยืนยาวสุขภาพเลิศ")
]

for idx, title, grade, w_txt, m_txt, l_txt, h_txt in _EXT_THEMES:
    SIAMSEE_DATA[idx] = {
        "title": title,
        "grade": grade,
        "poem": f"ใบที่{idx} พึงจำ คำพยากรณ์\nเทพบันดล พรบวร สถาพรศรี\nประกอบกิจ สุจริต มั่งมีดี\nตลอดปี เจริญรุ่ง พุ่งไกลเอย",
        "work": f"{w_txt} ดำเนินตามแผนอย่างมั่นใจและรอบคอบ",
        "wealth": f"{m_txt} มีเกณฑ์รับทรัพย์และโชคลาภเข้ามาต่อเนื่อง",
        "love": f"{l_txt} ถนอมน้ำใจกันแล้วชีวิตคู่จะราบรื่น",
        "health": f"{h_txt} ดื่มน้ำมาก ๆ และพักผ่อนให้เพียงพอ",
        "caution": "ตั้งมั่นในศีลธรรมและวาจาสุจริต จะเป็นมงคลคุ้มกายตลอดไป"
    }


def build_siamsee_flex(stick_num: int = None, user: dict = None) -> dict:
    """Build interactive Siamsee Fortune Flex Card with traditional poems & advice."""
    import random
    if not stick_num or stick_num not in SIAMSEE_DATA:
        stick_num = random.randint(1, 28)

    data = SIAMSEE_DATA[stick_num]
    user_name = user.get("name", "ผู้มีบุญ") if user else "ผู้มีบุญ"

    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": "https://plb-horoscope.vercel.app/bear_fortune.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#1e1b4b",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🥠 เซียมซีพยากรณ์ เทพประทานพร", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                        {"type": "text", "text": "PLB โหราศาสตร์", "color": "#c7d2fe", "size": "xxs", "align": "end"}
                    ]
                },
                {"type": "text", "text": f"เสี่ยงทายเพื่อคุณ {user_name} ✨", "color": "#e0e7ff", "size": "xs", "margin": "xs"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "spacing": "md",
            "contents": [
                # Stick Number & Title Header Box
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#312e81",
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "borderColor": "#818cf8",
                    "borderWidth": "1px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": f"📜 ใบที่ {stick_num}: {data['title']}", "weight": "bold", "size": "sm", "color": "#fef08a", "flex": 1},
                                {"type": "text", "text": data["grade"], "size": "xxs", "color": "#86efac", "align": "end", "weight": "bold"}
                            ]
                        },
                        {
                            "type": "text",
                            "text": data["poem"],
                            "size": "xs",
                            "color": "#f8fafc",
                            "wrap": True,
                            "margin": "sm",
                            "weight": "bold"
                        }
                    ]
                },
                # Predictions across 4 aspects
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#0f172a",
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "borderColor": "#334155",
                    "borderWidth": "1px",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "💼 การงาน:", "size": "xxs", "color": "#38bdf8", "weight": "bold", "flex": 2},
                                {"type": "text", "text": data["work"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "flex": 5}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "💰 การเงิน:", "size": "xxs", "color": "#fbbf24", "weight": "bold", "flex": 2},
                                {"type": "text", "text": data["wealth"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "flex": 5}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "💖 ความรัก:", "size": "xxs", "color": "#f472b6", "weight": "bold", "flex": 2},
                                {"type": "text", "text": data["love"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "flex": 5}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "🩺 สุขภาพ:", "size": "xxs", "color": "#4ade80", "weight": "bold", "flex": 2},
                                {"type": "text", "text": data["health"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "flex": 5}
                            ]
                        }
                    ]
                },
                # Daily Caution
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#1e293b",
                    "cornerRadius": "8px",
                    "paddingAll": "8px",
                    "contents": [
                        {"type": "text", "text": "⚠️ ข้อคิดเตือนสติประจำวัน:", "size": "xxs", "color": "#f59e0b", "weight": "bold"},
                        {"type": "text", "text": data["caution"], "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "xs",
                    "contents": [
                        {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ปลอดภัย 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#6366f1",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🥠 เขย่าใหม่อีกครั้ง",
                                "text": "เซียมซี"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#d97706",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🌟 ดูสรุปดวงวันนี้",
                                "text": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "👕 สีเสื้อมงคล",
                                "text": "สีเสื้อมงคล"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#065f46",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🎰 ขอเลขเด็ด",
                                "text": "ขอเลขเด็ด"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    return {
        "type": "flex",
        "altText": f"🥠 เซียมซีใบที่ {stick_num}: {data['title']} ({data['grade']}) 📜✨",
        "contents": bubble,
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "message", "label": "🥠 เขย่าใหม่อีกครั้ง", "text": "เซียมซี"}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                {"type": "action", "action": {"type": "message", "label": "🎁 วอลเปเปอร์", "text": "วอลเปเปอร์"}}
            ]
        }
    }


def build_wallpaper_rewards_flex(user: dict = None, web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build Lucky Mobile Wallpapers Unlock Rewards Flex Card."""
    web_url = web_url or "https://plb-horoscope.vercel.app"
    user = user or {}
    user_name = user.get("name", "ผู้มีวาสนา")
    check_count = int(user.get("check_count", 0))
    streak = int(user.get("streak", 1))

    # Evaluate wallpaper unlock status
    w1_unlocked = check_count >= 7 or streak >= 4
    w2_unlocked = check_count >= 14 or streak >= 7
    w3_unlocked = check_count >= 21 or streak >= 11
    w4_unlocked = check_count >= 50 or streak >= 21

    def make_wall_row(title, req_text, is_unlocked, icon, desc, color):
        status_text = "🔓 ปลดล็อกแล้ว! พร้อมดาวน์โหลด" if is_unlocked else f"🔒 ปลดล็อกเมื่อ {req_text}"
        status_color = "#86efac" if is_unlocked else "#94a3b8"
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#06281e" if is_unlocked else "#1e293b",
            "cornerRadius": "8px",
            "paddingAll": "10px",
            "borderColor": color if is_unlocked else "#334155",
            "borderWidth": "1px",
            "margin": "xs",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"{icon} {title}", "weight": "bold", "size": "xs", "color": "#f8fafc", "flex": 1},
                        {"type": "text", "text": "✓ สำเร็จ" if is_unlocked else "🔒 ล็อก", "size": "xxs", "color": status_color, "align": "end", "weight": "bold"}
                    ]
                },
                {"type": "text", "text": desc, "size": "xxs", "color": "#cbd5e1", "margin": "xs"},
                {"type": "text", "text": status_text, "size": "xxs", "color": status_color, "margin": "xs", "weight": "bold"}
            ]
        }

    wall_rows = [
        make_wall_row("วอลเปเปอร์มหาเศรษฐีเปิดทางรวย", "เช็กครบ 7 ครั้ง หรือ 4 วันติด", w1_unlocked, "💰", "เสริมโชคลาภ คลังทรัพย์เปิดรับเงินทองไหลมาเทมา", "#10b981"),
        make_wall_row("วอลเปเปอร์เลื่อนขั้นมหาอำนาจบารมี", "เช็กครบ 14 ครั้ง หรือ 7 วันติด", w2_unlocked, "💼", "เสริมการงาน ชนะคู่แข่ง ผู้ใหญ่อุปถัมภ์ค้ำชู", "#3b82f6"),
        make_wall_row("วอลเปเปอร์มหาเสน่ห์เมตตามหานิยม", "เช็กครบ 21 ครั้ง หรือ 11 วันติด", w3_unlocked, "💖", "เสริมความรัก มหาเสน่ห์ คนรักคนเมตตาเอ็นดู", "#ec4899"),
        make_wall_row("วอลเปเปอร์มหาจักรพรรดิ์นพเคราะห์ 9 ทิศ", "เช็กครบ 50 ครั้ง หรือ 21 วันติด", w4_unlocked, "👑", "บารมีขั้นสูงสุด คุ้มครองรอบทิศ สมปรารถนาทุกประการ", "#fbbf24")
    ]

    bubble = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": f"{web_url}/bear_wizard.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🎁 คลังวอลเปเปอร์สายมูมหาเฮง", "weight": "bold", "color": "#fbbf24", "size": "sm", "flex": 1},
                        {"type": "text", "text": "PLB รางวัลสะสม", "color": "#94a3b8", "size": "xxs", "align": "end"}
                    ]
                },
                {"type": "text", "text": f"ของขวัญมงคลแด่คุณ {user_name} (สถิติ: {check_count} ครั้ง / {streak} วันติด) ✨", "color": "#e2e8f0", "size": "xs", "margin": "xs"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "16px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "text",
                    "text": "📱 ยิ่งตรวจดวงต่อเนื่อง ยิ่งปลดล็อกวอลเปเปอร์มือถือมงคลความละเอียดสูงได้ฟรี นำไปตั้งเป็นภาพหน้าจอดูดพลังบวกได้ทุกวันครับ 👇",
                    "size": "xs",
                    "color": "#cbd5e1",
                    "wrap": True,
                    "margin": "xs"
                },
                *wall_rows,
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": "🛡️ เจ้าของแอปไม่บันทึกข้อมูลส่วนตัว • ข้อมูลอยู่บนเครื่องคุณ 100%", "size": "xxs", "color": "#64748b", "align": "center"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#030712",
            "paddingAll": "14px",
            "spacing": "xs",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#d97706",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "📲 เปิดคลังดาวน์โหลดบนมือถือ",
                        "uri": make_liff_url(web_url or "https://plb-horoscope.vercel.app", user, extra_query="#wallpapers")
                    }
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "📊 สถิติวาสนา",
                                "text": "สถิติ"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "color": "#1e293b",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🌟 ดูดวงวันนี้",
                                "text": "สรุปดวงประจำวัน"
                            },
                            "flex": 1
                        }
                    ]
                }
            ]
        }
    }

    return {
        "type": "flex",
        "altText": f"🎁 คลังวอลเปเปอร์สายมูของคุณ {user_name}: ปลดล็อกความเฮงสู่หน้าจอมือถือ ✨",
        "contents": bubble,
        "quickReply": {
            "items": [
                {"type": "action", "action": {"type": "uri", "label": "📲 ดาวน์โหลดวอลเปเปอร์", "uri": make_liff_url(web_url or "https://plb-horoscope.vercel.app", user, extra_query="#wallpapers")}},
                {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                {"type": "action", "action": {"type": "message", "label": "📊 สถิติดวง", "text": "สถิติ"}},
                {"type": "action", "action": {"type": "message", "label": "🥠 เสี่ยงเซียมซี", "text": "เซียมซี"}}
            ]
        }
    }

