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

def build_daily_summary_flex(user: dict, horoscope: dict, liff_url: str = "", web_url: str = "https://plb-horoscope.vercel.app") -> dict:
    """Build the main daily horoscope summary Flex Card."""
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
    career = cats.get("career", {})
    finance = cats.get("finance", {})
    love = cats.get("love", {})
    health = cats.get("health", {})
    
    lucky = horoscope.get("luckyInfo", {})
    lucky_nums = " ".join([str(n) for n in lucky.get("numbers", [1, 5, 9])[:3]])
    lucky_colors = lucky.get("colors", "ทอง, เหลือง")
    lucky_dirs = lucky.get("directions", "ทิศตะวันออก")
    gemstones = lucky.get("gemstones", "บุษราคัม")
    
    date_str = horoscope.get("date", "")
    user_name = user.get("name", "ผู้ใช้")

    return {
        "type": "flex",
        "altText": f"🔮 สรุปดวงวันนี้: ลัคนาราศี{asc_name} (คะแนน {overall.get('score', 80)}%)",
        "contents": {
            "type": "bubble",
            "size": "mega",
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
                            {"type": "text", "text": "🔮 PLB โหราศาสตร์", "weight": "bold", "color": "#f59e0b", "size": "sm", "flex": 1},
                            {"type": "text", "text": f"📅 {date_str}", "color": "#94a3b8", "size": "xxs", "align": "end"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "contents": [
                            {"type": "text", "text": f"ดวงของคุณ {user_name}", "color": "#f8fafc", "size": "md", "weight": "bold", "flex": 1},
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#f59e0b",
                                "cornerRadius": "99px",
                                "paddingStart": "8px",
                                "paddingEnd": "8px",
                                "paddingTop": "2px",
                                "paddingBottom": "2px",
                                "contents": [
                                    {"type": "text", "text": f"ลัคนา {asc_name} {asc_deg}°{asc_min}'", "color": "#0f172a", "size": "xxs", "weight": "bold"}
                                ]
                            }
                        ]
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    # Location badge
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "8px",
                        "paddingAll": "8px",
                        "contents": [
                            {"type": "text", "text": f"📍 สถิตจร: {transit_prov} ({transit_dist}) • รุ่งอรุณ {sunrise} น.", "size": "xxs", "color": "#38bdf8", "flex": 1}
                        ]
                    },
                    # Theme & Score
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": "ภาพรวมวันนี้", "size": "xs", "color": "#cbd5e1", "weight": "bold", "flex": 1},
                                    {"type": "text", "text": f"{overall.get('score', 80)}% ({overall.get('grade', 'B+')})", "size": "sm", "color": "#f59e0b", "weight": "bold", "align": "end"}
                                ]
                            },
                            {"type": "text", "text": overall.get("theme", "จังหวะชีวิตราบรื่น มีเกณฑ์ก้าวหน้า"), "size": "xs", "color": "#e2e8f0", "wrap": True, "margin": "xs"}
                        ]
                    },
                    {"type": "separator", "color": "#334155", "margin": "md"},
                    # Category Scores
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "📊 คะแนนพลังชะตา 4 ด้าน:", "size": "xxs", "color": "#94a3b8", "weight": "bold"},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {"type": "text", "text": f"💼 งาน {career.get('score', 80)}%", "size": "xxs", "color": "#93c5fd", "flex": 1},
                                    {"type": "text", "text": f"💰 เงิน {finance.get('score', 80)}%", "size": "xxs", "color": "#86efac", "flex": 1},
                                    {"type": "text", "text": f"❤️ รัก {love.get('score', 80)}%", "size": "xxs", "color": "#f472b6", "flex": 1},
                                    {"type": "text", "text": f"🩺 สุขภาพ {health.get('score', 80)}%", "size": "xxs", "color": "#fde047", "flex": 1}
                                ]
                            }
                        ]
                    },
                    {"type": "separator", "color": "#334155", "margin": "md"},
                    # Lucky Boosters
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#172554",
                        "cornerRadius": "8px",
                        "paddingAll": "10px",
                        "contents": [
                            {"type": "text", "text": "✨ เคล็ดลับดวงมงคลวันนี้:", "size": "xxs", "color": "#fbbf24", "weight": "bold"},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {"type": "text", "text": f"🎯 เลขเด่น: {lucky_nums}", "size": "xxs", "color": "#e2e8f0", "flex": 1},
                                    {"type": "text", "text": f"🎨 สีมงคล: {lucky_colors}", "size": "xxs", "color": "#e2e8f0", "flex": 1}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {"type": "text", "text": f"🧭 ทิศมงคล: {lucky_dirs}", "size": "xxs", "color": "#cbd5e1", "flex": 1},
                                    {"type": "text", "text": f"💎 อัญมณี: {gemstones}", "size": "xxs", "color": "#cbd5e1", "flex": 1}
                                ]
                            }
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
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#d97706",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "🔮 เจาะลึกรายหมวด",
                                    "data": "action=select_category",
                                    "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
                                },
                                "flex": 1
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#334155",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "📍 เปลี่ยนสถานที่จร",
                                    "data": "action=change_transit",
                                    "displayText": "เปลี่ยนสถานที่จร"
                                },
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "color": "#1e293b",
                                "height": "sm",
                                "action": {
                                    "type": "uri",
                                    "label": "⚙️ แก้ไขวันเกิด",
                                    "uri": liff_url
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
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "🌐 ดูผังจักรราศีเต็มบนเว็บ",
                            "uri": web_url
                        }
                    }
                ]
            }
        }
    }

def build_category_flex(category_key: str, category_data: dict, asc_name: str, date_str: str) -> dict:
    """Build a detailed single-category horoscope flex message."""
    CAT_NAMES = {
        "career": ("💼 การงาน & ธุรกิจ", "#3b82f6"),
        "finance": ("💰 การเงิน & โชคลาภ", "#10b981"),
        "love": ("❤️ ความรัก & เสน่ห์", "#ec4899"),
        "health": ("🩺 สุขภาพ & เตือนภัย", "#eab308"),
        "zodiac": ("☸ ผังจักรราศี 12 ช่อง", "#8b5cf6")
    }
    
    title, color = CAT_NAMES.get(category_key, ("🔮 คำทำนายดวงชะตา", "#f59e0b"))
    score = category_data.get("score", 80)
    grade = category_data.get("grade", "B+")
    theme = category_data.get("theme", "จังหวะดวงกำลังเปิด")
    forecast = category_data.get("forecast", "")
    advice = category_data.get("advice", "")
    highlights = category_data.get("highlights", [])
    
    hl_contents = []
    for h in highlights[:4]:
        hl_contents.append({
            "type": "text",
            "text": f"• {h}",
            "size": "xxs",
            "color": "#cbd5e1",
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
                "backgroundColor": "#0b0f19",
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
                    {"type": "text", "text": f"ลัคนาราศี{asc_name} • วันที่ {date_str}", "size": "xxs", "color": "#94a3b8", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f172a",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": theme, "weight": "bold", "size": "sm", "color": "#fbbf24", "wrap": True},
                    {"type": "separator", "color": "#334155", "margin": "sm"},
                    {"type": "text", "text": forecast, "size": "xs", "color": "#e2e8f0", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "backgroundColor": "#1e293b",
                        "cornerRadius": "8px",
                        "paddingAll": "10px",
                        "contents": [
                            {"type": "text", "text": "💡 คำแนะนำเชิงโหราศาสตร์:", "weight": "bold", "size": "xxs", "color": "#38bdf8"},
                            {"type": "text", "text": advice, "size": "xxs", "color": "#cbd5e1", "wrap": True, "margin": "xs"}
                        ]
                    },
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
                "layout": "horizontal",
                "backgroundColor": "#0b0f19",
                "paddingAll": "12px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#d97706",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "หมวดอื่น 🔄",
                            "data": "action=select_category",
                            "displayText": "เลือกหมวดอยากจะดูหมวดไหน"
                        },
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#334155",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "ดวงสรุป 🌟",
                            "data": "action=daily_summary",
                            "displayText": "สรุปดวงประจำวัน"
                        },
                        "flex": 1
                    }
                ]
            }
        }
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
                            {"type": "text", "text": account_en, "size": "xxs", "color": "#94a3b8", "margin": "xxs"},
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
                    "type": "postback",
                    "label": "💼 การงาน",
                    "data": "action=category&cat=career",
                    "displayText": "ดูดวงหมวดการงาน"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "💰 การเงิน",
                    "data": "action=category&cat=finance",
                    "displayText": "ดูดวงหมวดการเงิน"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "❤️ ความรัก",
                    "data": "action=category&cat=love",
                    "displayText": "ดูดวงหมวดความรัก"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "🩺 สุขภาพ",
                    "data": "action=category&cat=health",
                    "displayText": "ดูดวงหมวดสุขภาพ"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "📍 เปลี่ยนที่จร",
                    "data": "action=change_transit",
                    "displayText": "เปลี่ยนสถานที่จร"
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

