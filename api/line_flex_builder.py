#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Flex Message Builder for PLB Thai Astrology Bot
Produces pixel-perfect, dark cosmic & luxury gold themed Flex Messages.
Compatible with LINE Messaging API specifications.
"""

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
                    {"type": "text", "text": "กรุณาลงทะเบียนข้อมูลวันเกิดและสถานที่เกิด เพื่อเริ่มคำนวณดวงชะตาเฉพาะตัวของคุณ 👇", "size": "xs", "color": "#38bdf8", "wrap": True, "margin": "lg"}
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
    
    # Stateless postback fallback payload
    b_date = user.get("birth_date", "1995-08-12")
    b_time = user.get("birth_time", "08:30")
    b_prov = user.get("birth_province", "กรุงเทพมหานคร")
    t_prov = user.get("transit_province", b_prov)
    pb_meta = f"&b={b_date}&t={b_time}&p={b_prov}&tp={t_prov}"

    # Visual gauge color based on score
    gauge_color = "#fbbf24" if overall_score >= 85 else ("#38bdf8" if overall_score >= 75 else "#a78bfa")

    return {
        "type": "flex",
        "altText": f"👑 ดวงประจำวัน: ลัคนาราศี{asc_name} (เกณฑ์วาสนา {overall_score}%)",
        "contents": {
            "type": "bubble",
            "size": "mega",
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
                            {"type": "text", "text": "🏛️ จตุสดมภ์โชคลาภ 4 ด้าน:", "size": "xxs", "color": "#fbbf24", "weight": "bold"},
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
                                        "contents": [
                                            {"type": "text", "text": f"💼 งาน {career.get('score', 80)}%", "size": "xxs", "color": "#93c5fd", "weight": "bold"},
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
                                        "contents": [
                                            {"type": "text", "text": f"💰 เงิน {finance.get('score', 80)}%", "size": "xxs", "color": "#fef08a", "weight": "bold"},
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
                                        "contents": [
                                            {"type": "text", "text": f"❤️ รัก {love.get('score', 80)}%", "size": "xxs", "color": "#f472b6", "weight": "bold"},
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
                                        "contents": [
                                            {"type": "text", "text": f"🩺 กาย {health.get('score', 80)}%", "size": "xxs", "color": "#86efac", "weight": "bold"},
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
                            "label": "📊 สถิติดวงย้อนหลัง & กิมมิกดวง",
                            "data": f"action=stats{pb_meta}",
                            "displayText": "สถิติดวงย้อนหลัง"
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
                                    "label": "🔮 เจาะลึกรายหมวด",
                                    "data": f"action=select_category{pb_meta}",
                                    "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
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
                                    "uri": f"{liff_url}?userId={user.get('line_user_id','')}" if '?' not in liff_url else liff_url
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

    # Stateless postback metadata
    b_date = user.get("birth_date", "1995-08-12")
    b_time = user.get("birth_time", "08:30")
    b_prov = user.get("birth_province", "กรุงเทพมหานคร")
    t_prov = user.get("transit_province", b_prov)
    pb_meta = f"&b={b_date}&t={b_time}&p={b_prov}&tp={t_prov}"

    return {
        "type": "flex",
        "altText": f"📊 แดชบอร์ดสถิติดวงชะตา: คุณ {user_name} ({rank['title']})",
        "contents": {
            "type": "bubble",
            "size": "mega",
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
                                            {"type": "text", "text": "🔢 ตรวจดวงสะสม", "size": "xxs", "color": "#94a3b8"},
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
                                            {"type": "text", "text": "🔥 ต่อเนื่อง", "size": "xxs", "color": "#94a3b8"},
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
                                    "label": "🔮 เจาะลึกรายหมวด",
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
        }
    }

def build_category_menu_flex() -> dict:
    """Build an interactive luxury card to choose horoscope categories."""
    return {
        "type": "flex",
        "altText": "🔮 เลือกหมวดดูดวงเจาะลึก (การงาน, การเงิน, ความรัก, สุขภาพ)",
        "contents": {
            "type": "bubble",
            "size": "mega",
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
                            "type": "message",
                            "label": "💼 ดูหมวดการงาน & ธุรกิจ",
                            "text": "การงาน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#047857",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "💰 ดูหมวดการเงิน & โชคลาภ",
                            "text": "การเงิน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#be185d",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "❤️ ดูหมวดความรัก & เสน่ห์",
                            "text": "ความรัก"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#b45309",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "🩺 ดูหมวดสุขภาพ & เตือนภัย",
                            "text": "สุขภาพ"
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

def build_category_flex(category_key: str, category_data: dict, asc_name: str, date_str: str) -> dict:
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

    return {
        "type": "flex",
        "altText": f"{title} (ลัคนาราศี{asc_name}): {score}%",
        "contents": {
            "type": "bubble",
            "size": "mega",
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
                            "type": "message",
                            "label": "🔮 เลือกหมวดอื่น",
                            "text": "เลือกหมวดอยากจะดูหมวดไหน"
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
                                    "label": "🌟 สรุปดวงรวม",
                                    "text": "สรุปดวงประจำวัน"
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
                                    "label": "📊 สถิติ & กิมมิก",
                                    "text": "สถิติ"
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

def build_feedback_flex() -> dict:
    """Build the 5-star accuracy rating and comment card."""
    return {
        "type": "flex",
        "altText": "ประเมินความแม่นยำดวงวันนี้ ⭐",
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
                                    "label": "⭐⭐⭐ ปานกลาง พอใช้ได้ 🔮",
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
                                    "label": "⭐ - ⭐⭐ ยังไม่ค่อยตรง / เฉยๆ 💭",
                                    "data": "action=feedback_rate&stars=2",
                                    "displayText": "ให้คะแนนความแม่นยำ: 2 ดาว ⭐⭐"
                                }
                            }
                        ]
                    },
                    {"type": "text", "text": "💡 หลังกดดาว คุณสามารถพิมพ์ข้อความคอมเมนต์หรือข้อเสนอแนะส่งเข้ามาในแชตนี้ได้ทันทีครับ", "size": "xxs", "color": "#94a3b8", "wrap": True, "margin": "md"}
                ]
            }
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

def build_share_flex() -> dict:
    """Build a cute share invitation card for LINE OA."""
    return {
        "type": "flex",
        "altText": "ชวนเพื่อนมาดูดวงกับน้องหมี PLB โหราศาสตร์ 🐻‍❄️✨",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "🐻‍❄️ PLB หมีดูดวง • ชวนเพื่อน", "weight": "bold", "color": "#fbbf24", "size": "md"},
                    {"type": "text", "text": "แชร์ความแม่นยำให้เพื่อนๆ เช็คดวงฟรี!", "color": "#94a3b8", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "ส่งต่อความเฮงให้เพื่อนของคุณ ✨", "weight": "bold", "size": "sm", "color": "#f8fafc"},
                    {"type": "text", "text": "ชวนเพื่อนมารู้จักลัคนาราศีที่แท้จริง พร้อมคำนวณคะแนนชีวิต 4 ด้านและเลขมงคลประจำวันได้ฟรีทุกวันครับ 🔮", "size": "xs", "color": "#cbd5e1", "wrap": True, "margin": "xs"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "12px",
                        "paddingAll": "12px",
                        "contents": [
                            {"type": "text", "text": "📲 LINE ID สำหรับเพิ่มเพื่อน:", "size": "xs", "color": "#38bdf8", "weight": "bold"},
                            {"type": "text", "text": "@374xcoto", "size": "lg", "weight": "bold", "color": "#fbbf24", "margin": "xs"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0b0f19",
                "paddingAll": "12px",
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
                    }
                ]
            }
        }
    }

