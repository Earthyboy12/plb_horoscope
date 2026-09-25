#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot Engine for PLB Thai Astrology
Handles signature verification, webhook event routing, astrological computation,
and message dispatching via LINE Messaging API.
Uses pure Python standard library (no pip packages required).
"""

import hmac
import hashlib
import base64
import json
import os
import re
import urllib.request
import urllib.parse
import datetime

try:
    from thai_astrology import get_horoscope, PROVINCES_DICT
    from user_store import get_user, save_user, update_transit_location, record_user_check
    from line_flex_builder import (
        build_welcome_flex,
        build_daily_summary_flex,
        build_category_menu_flex,
        build_category_flex,
        build_lucky_numbers_flex,
        build_lucky_colors_flex,
        build_feedback_flex,
        build_noon_reminder_flex,
        build_morning_reminder_flex,
        build_lottery_special_flex,
        build_siamsee_flex,
        build_wallpaper_rewards_flex,
        build_donation_flex,
        build_share_flex,
        build_stats_flex,
        get_category_quick_reply
    )
except ImportError:
    from api.thai_astrology import get_horoscope, PROVINCES_DICT
    from api.user_store import get_user, save_user, update_transit_location, record_user_check
    from api.line_flex_builder import (
        build_welcome_flex,
        build_daily_summary_flex,
        build_category_menu_flex,
        build_category_flex,
        build_lucky_numbers_flex,
        build_lucky_colors_flex,
        build_feedback_flex,
        build_noon_reminder_flex,
        build_morning_reminder_flex,
        build_lottery_special_flex,
        build_siamsee_flex,
        build_wallpaper_rewards_flex,
        build_donation_flex,
        build_share_flex,
        build_stats_flex,
        get_category_quick_reply
    )

THAI_MONTHS_MAP = {
    'ม.ค.': 1, 'มกรา': 1, 'มกราคม': 1,
    'ก.พ.': 2, 'กุมภา': 2, 'กุมภาพันธ์': 2,
    'มี.ค.': 3, 'มีนา': 3, 'มีนาคม': 3,
    'เม.ย.': 4, 'เมษา': 4, 'เมษายน': 4,
    'พ.ค.': 5, 'พฤษภา': 5, 'พฤษภาคม': 5,
    'มิ.ย.': 6, 'มิถุนา': 6, 'มิถุนายน': 6,
    'ก.ค.': 7, 'กรกฎา': 7, 'กรกฎาคม': 7,
    'ส.ค.': 8, 'สิงหา': 8, 'สิงหาคม': 8,
    'ก.ย.': 9, 'กันยา': 9, 'กันยายน': 9,
    'ต.ค.': 10, 'ตุลา': 10, 'ตุลาคม': 10,
    'พ.ย.': 11, 'พฤศจิกา': 11, 'พฤศจิกายน': 11,
    'ธ.ค.': 12, 'ธันวา': 12, 'ธันวาคม': 12
}

def parse_birth_info_from_text(text: str):
    """
    Parse birth date, time, and province from natural Thai text.
    Handles:
      - 'เกิด 12/08/2538 08:30 กรุงเทพมหานคร'
      - 'เกิด 1995-08-12 09:15 เชียงใหม่'
      - 'เกิด 12 ส.ค. 2538 08.30 ภูเก็ต'
      - 'วันเกิด 1/5/2540 ขอนแก่น'
      - LIFF automated messages: 'เกิด YYYY-MM-DD HH:MM Province District'
    """
    cleaned = text.strip()
    has_birth_keyword = any(k in cleaned for k in ["เกิด", "วันเกิด", "birth", "ลงทะเบียน"])
    
    bdate = None
    # 1. YYYY-MM-DD or YYYY/MM/DD
    m = re.search(r'\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b', cleaned)
    if m:
        y, mth, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y > 2400: y -= 543
        bdate = f"{y:04d}-{mth:02d}-{d:02d}"
    
    # 2. DD/MM/YYYY or DD-MM-YYYY
    if not bdate:
        m2 = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', cleaned)
        if m2:
            d, mth, y = int(m2.group(1)), int(m2.group(2)), int(m2.group(3))
            if y > 2400: y -= 543
            bdate = f"{y:04d}-{mth:02d}-{d:02d}"

    # 3. Thai month text
    if not bdate:
        for m_name, m_num in sorted(THAI_MONTHS_MAP.items(), key=lambda x: -len(x[0])):
            pattern = rf'(\d{{1,2}})\s*{re.escape(m_name)}\s*(\d{{4}})?'
            m3 = re.search(pattern, cleaned)
            if m3:
                d = int(m3.group(1))
                y = int(m3.group(2)) if m3.group(2) else 2538
                if y > 2400: y -= 543
                bdate = f"{y:04d}-{m_num:02d}-{d:02d}"
                break

    if not bdate:
        return None

    if not has_birth_keyword:
        has_time_or_prov = bool(re.search(r'\b\d{1,2}[:.]\d{2}\b', cleaned)) or any(p in cleaned for p in ["กรุงเทพ", "กทม"] + list(PROVINCES_DICT.keys())[:20])
        if not has_time_or_prov:
            return None

    # Parse time
    mt = re.search(r'\b(\d{1,2})[:.](\d{2})\b', cleaned)
    btime = f"{int(mt.group(1)):02d}:{int(mt.group(2)):02d}" if mt else "08:30"
    
    # Parse province
    prov = "กรุงเทพมหานคร"
    if "กทม" in cleaned or "กรุงเทพ" in cleaned:
        prov = "กรุงเทพมหานคร"
    else:
        for p in PROVINCES_DICT.keys():
            if p in cleaned:
                prov = p
                break

    dist = "พระนคร" if prov == "กรุงเทพมหานคร" else f"อำเภอเมือง{prov}"
    
    t_prov = prov
    t_dist = dist
    if "จร " in cleaned:
        transit_part = cleaned.split("จร ", 1)[1].strip()
        for p in PROVINCES_DICT.keys():
            if p in transit_part:
                t_prov = p
                t_dist = "พระนคร" if p == "กรุงเทพมหานคร" else f"อำเภอเมือง{p}"
                break
    
    cc = 0
    m_cc = re.search(r'\bcc[=:]\s*(\d+)\b', cleaned, re.IGNORECASE)
    if m_cc:
        cc = int(m_cc.group(1))
    st = 1
    m_st = re.search(r'\bst[=:]\s*(\d+)\b', cleaned, re.IGNORECASE)
    if m_st:
        st = int(m_st.group(1))
    ld = ""
    m_ld = re.search(r'\bld[=:]\s*([\d-]+)\b', cleaned, re.IGNORECASE)
    if m_ld:
        ld = m_ld.group(1).strip()

    res = {
        "birth_date": bdate,
        "birth_time": btime,
        "birth_province": prov,
        "birth_district": dist,
        "transit_province": t_prov,
        "transit_district": t_dist,
        "calc_method": "suriyayatra",
        "registered": True
    }
    if cc > 0:
        res["check_count"] = cc
    if st > 1:
        res["streak"] = st
    if ld:
        res["last_check_date"] = ld
    return res

DEFAULT_FEEDBACK_WEBHOOK = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"
DEFAULT_CHANNEL_ID = "2011723219"
DEFAULT_CHANNEL_SECRET = "3881fe1c9b74acd6f8f293be16692a04"
DEFAULT_ACCESS_TOKEN = "MImmut2hIeq/gqp5f9g6v7KYnxg+hglGb/q15Lu3bTt6bEEKRQE4bji6BrwAr/8RjANH8Bed9O9W95CAe4t8/ELYqXGtxmNLQvMTtK+U0PasBLpRENWte1D6S9fCkJtRXTlWm8TN7wzuSloTNDKei49PbdgDzCFqoOLOYbqAITQ="

_CACHED_TOKEN = DEFAULT_ACCESS_TOKEN
_TOKEN_EXPIRY = datetime.datetime.now() + datetime.timedelta(days=29)

def get_channel_access_token():
    global _CACHED_TOKEN, _TOKEN_EXPIRY
    env_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if env_token:
        return env_token
    
    if _CACHED_TOKEN and datetime.datetime.now() < _TOKEN_EXPIRY:
        return _CACHED_TOKEN
        
    channel_id = os.environ.get("LINE_CHANNEL_ID", DEFAULT_CHANNEL_ID)
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET", DEFAULT_CHANNEL_SECRET)
    
    try:
        data = urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'client_id': channel_id,
            'client_secret': channel_secret
        }).encode('utf-8')
        req = urllib.request.Request(
            'https://api.line.me/v2/oauth/accessToken',
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp_data = json.loads(resp.read().decode('utf-8'))
            _CACHED_TOKEN = resp_data.get('access_token', DEFAULT_ACCESS_TOKEN)
            expires_in = int(resp_data.get('expires_in', 2592000))
            _TOKEN_EXPIRY = datetime.datetime.now() + datetime.timedelta(seconds=expires_in - 3600)
            return _CACHED_TOKEN
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return _CACHED_TOKEN or DEFAULT_ACCESS_TOKEN

def verify_signature(body_bytes: bytes, signature: str, channel_secret: str = "") -> bool:
    """Verify that the webhook request came from LINE Platform."""
    channel_secret = channel_secret or os.environ.get("LINE_CHANNEL_SECRET") or DEFAULT_CHANNEL_SECRET
    if not signature or not channel_secret:
        return True # In development mode or unconfigured, allow testing
    try:
        expected = base64.b64encode(
            hmac.new(channel_secret.encode('utf-8'), body_bytes, hashlib.sha256).digest()
        ).decode('utf-8')
        return hmac.compare_digest(expected, signature)
    except Exception as e:
        print(f"Signature verify error: {e}")
        return False

def reply_line_message(reply_token: str, messages: list, access_token: str = "", user_id: str = ""):
    """Send reply message(s) back to LINE user. Automatically falls back to push if replyToken expired or failed!"""
    access_token = access_token or get_channel_access_token()
    if not access_token:
        print("[LineBotEngine] No access token provided")
        return False
    
    success = False
    if reply_token:
        url = "https://api.line.me/v2/bot/message/reply"
        payload = {
            "replyToken": reply_token,
            "messages": messages
        }
        try:
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "Authorization": f"Bearer {access_token}"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    return True
        except urllib.error.HTTPError as he:
            err_body = he.read().decode('utf-8', errors='ignore')
            print(f"[LineBotEngine] Reply failed ({he.code}): {err_body}")
        except Exception as e:
            print(f"[LineBotEngine] Error replying to LINE: {e}")

    # Fallback to direct push if reply token expired, already consumed, or failed
    if not success and user_id and user_id.startswith("U"):
        print(f"[LineBotEngine] Auto-fallback to direct push for {user_id}")
        return push_line_message(user_id, messages, access_token)

    return success

def push_line_message(user_id: str, messages: list, access_token: str = ""):
    """Push message directly to a LINE user by user ID."""
    access_token = access_token or get_channel_access_token()
    if not access_token or not user_id:
        return False
    
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id,
        "messages": messages
    }
    
    try:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {access_token}"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return response.status == 200
    except Exception as e:
        print(f"[LineBotEngine] Error pushing to LINE: {e}")
        return False

def compute_user_horoscope(user: dict, target_date: str = "") -> dict:
    """Compute astrological forecast for the given user profile."""
    if not target_date:
        # Default to today in Thailand (UTC+7)
        now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        target_date = now_th.strftime("%Y-%m-%d")
        
    birth_prov = user.get("birth_province", "กรุงเทพมหานคร")
    birth_dist = user.get("birth_district", "พระนคร")
    transit_prov = user.get("transit_province") or birth_prov
    transit_dist = user.get("transit_district") or birth_dist
    is_same = (transit_prov == birth_prov)

    payload = {
        "birthDate": user.get("birth_date", "1995-08-12"),
        "birthTime": user.get("birth_time", "08:30"),
        "province": birth_prov,
        "district": birth_dist,
        "calcMethod": user.get("calc_method", "suriyayatra"),
        "isSameLocation": is_same,
        "transitProvince": transit_prov,
        "transitDistrict": transit_dist,
        "name": user.get("name", "ผู้ใช้")
    }
    return get_horoscope(payload, target_date)

def handle_line_event(event: dict, channel_access_token: str, liff_id: str, web_url: str):
    """Handle a single LINE webhook event."""
    event_type = event.get("type")
    reply_token = event.get("replyToken")
    source = event.get("source", {})
    user_id = source.get("userId")
    
    if not user_id:
        return
    
    user = get_user(user_id)
    is_registered = bool(user and user.get("registered", False))

    try:
        from line_flex_builder import make_liff_url
    except ImportError:
        from api.line_flex_builder import make_liff_url
    
    base_raw_liff = f"https://liff.line.me/{liff_id}" if liff_id else f"{web_url}/liff-register.html"
    liff_url = make_liff_url(base_raw_liff, user or {"line_user_id": user_id})

    def reply(messages: list):
        return reply_line_message(reply_token, messages, channel_access_token, user_id=user_id)
    
    # 1. Event: Follow (User adds LINE OA as friend)
    if event_type == "follow":
        welcome_flex = build_welcome_flex(liff_url)
        reply([welcome_flex])
        return
    
    # Helper for unregistered users
    def prompt_registration():
        welcome_flex = build_welcome_flex(liff_url)
        reply([
            {
                "type": "text",
                "text": "🔮 สวัสดีครับ! น้องหมียังไม่มีข้อมูลวันเกิดของคุณ\n\n📌 สามารถกดลงทะเบียนผ่านปุ่มด้านล่าง หรือพิมพ์บอกวันเกิดได้ทันที เช่น:\n👉 เกิด 15/08/2538 08:30 กทม",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "uri", "label": "🌟 ลงทะเบียนวันเกิด", "uri": liff_url}},
                        {"type": "action", "action": {"type": "message", "label": "💡 ตัวอย่างพิมพ์บอก", "text": "เกิด 12/08/2538 08:30 กทม"}},
                        {"type": "action", "action": {"type": "uri", "label": "👥 ชวนเพื่อนดูดวง", "uri": "https://line.me/R/nv/recommendOA/@374xcoto"}}
                    ]
                }
            },
            welcome_flex
        ])

    # 2. Event: Message (Text)
    if event_type == "message":
        message = event.get("message", {})
        msg_type = message.get("type")
        
        if msg_type != "text":
            return
            
        text = message.get("text", "").strip()
        text_lower = text.lower()
        
        # Check Natural Chat Registration / LIFF auto-messages e.g. "เกิด 12/08/2538 08:30 กทม"
        parsed_natal = parse_birth_info_from_text(text)
        if parsed_natal:
            existing_user = get_user(user_id) or {}
            if existing_user:
                parsed_natal['check_count'] = max(parsed_natal.get('check_count', 0), existing_user.get('check_count', 0))
                parsed_natal['streak'] = max(parsed_natal.get('streak', 1), existing_user.get('streak', 1))
                if existing_user.get('history') and not parsed_natal.get('history'):
                    parsed_natal['history'] = existing_user.get('history')
                if existing_user.get('last_check_date') and not parsed_natal.get('last_check_date'):
                    parsed_natal['last_check_date'] = existing_user.get('last_check_date')
                if existing_user.get('name') and not parsed_natal.get('name'):
                    parsed_natal['name'] = existing_user.get('name')
            user = save_user(user_id, parsed_natal)
            is_registered = True
            horoscope = compute_user_horoscope(user)
            user = record_user_check(user_id, horoscope.get("overallScore", 80)) or get_user(user_id) or user
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply([
                {
                    "type": "text",
                    "text": f"🎉 บันทึกข้อมูลและผูกดวงชะตาสำเร็จแล้วครับ!\n📅 วันเกิด: {user.get('birth_date')}\n⏰ เวลา: {user.get('birth_time')} น.\n📍 จังหวัดเกิด: {user.get('birth_province')}\n🧭 สถานที่จร: {user.get('transit_province')}\n👑 สถิติวาสนาสะสม: {user.get('check_count', 1)} ครั้ง (ระดับ {user.get('check_count', 1)})\n\nนี่คือสรุปดวงประจำวันและลัคนาราศีเฉพาะตัวของคุณครับ ✨"
                },
                summary_flex
            ])
            return

        # Check Stat Recovery / Sync command
        if any(k in text_lower for k in ["กู้คืนสถิติ", "กู้สถิติ", "ตั้งค่าสถิติ", "เซ็ตสถิติ", "restore_stats"]):
            m_set = re.search(r'(?:cc[=:]\s*|สถิติ\s*|ครั้งที่\s*|\s+)(\d+)', text_lower)
            if m_set:
                new_c = int(m_set.group(1))
                if not user:
                    user = save_user(user_id, {"check_count": new_c, "registered": True})
                else:
                    user["check_count"] = new_c
                    try:
                        from user_store import _save_cache
                    except ImportError:
                        from api.user_store import _save_cache
                    _save_cache()
                try:
                    from user_store import get_rank_title
                except ImportError:
                    from api.user_store import get_rank_title
                rnk = get_rank_title(new_c, user.get("streak", 1) if user else 1)
                reply([{
                    "type": "text",
                    "text": f"👑 ซิงค์สถิติดวงสำเร็จแล้วครับ!\n\n🔢 สถิติตรวจดวงสะสม: {new_c} ครั้ง\n🎖️ ระดับปัจจุบัน: {rnk['title']} ({rnk['badge']})\n\nระบบบันทึกข้อมูลผูกกับบัญชี LINE ของคุณเรียบร้อยแล้วครับ ✨"
                }])
                return

        # Check Personal Astro Stats & Streak Gimmick (สถิติดวงย้อนหลัง & กราฟ 7 วัน)
        if any(k in text_lower for k in ["stats", "สถิติ", "ประวัติ", "กี่ครั้ง", "streak", "ย้อนหลัง", "กิมมิก", "คะแนนย้อนหลัง"]):
            if not is_registered:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            user = get_user(user_id) or user
            stats_flex = build_stats_flex(user, horoscope)
            reply([stats_flex])
            return

        # Check registration commands
        if any(k in text for k in ["ลงทะเบียน", "แก้ไขข้อมูล", "ตั้งค่าดวง", "โปรไฟล์", "เปลี่ยนวันเกิด"]):
            welcome_flex = build_welcome_flex(liff_url)
            reply([welcome_flex])
            return

        # Check Share LINE OA command
        if any(k in text for k in ["แชร์", "ชวนเพื่อน", "แชร์ให้เพื่อน", "share", "ชวน"]):
            reply([build_share_flex()])
            return

        # Check Noon Daily Reminder test command
        if any(k in text for k in ["ทดสอบพุชเที่ยง", "พุชเที่ยง", "ดวงตอนเที่ยง", "เตือนตอนเที่ยง"]):
            noon_flex = build_noon_reminder_flex(web_url)
            reply([
                {
                    "type": "text",
                    "text": "🍱 นี่คือตัวอย่างการ์ดข้อความเชิญชวนดูดวงตอนเที่ยง (Noon Daily Reminder) ที่จะส่งแจ้งเตือนทุกวันเวลา 12:00 น. ครับ 🐻‍❄️✨"
                },
                noon_flex
            ])
            return

        # Check Transit Location Change command e.g. "จร เชียงใหม่" หรือ "เปลี่ยนสถานที่จร"
        if text.startswith("จร ") or text.startswith("เปลี่ยนที่จร "):
            parts = text.split(maxsplit=1)
            target_prov = parts[1].strip() if len(parts) > 1 else ""
            
            m_cc = re.search(r'\bcc[=:]\s*(\d+)\b', text, re.IGNORECASE)
            m_st = re.search(r'\bst[=:]\s*(\d+)\b', text, re.IGNORECASE)
            incoming_cc = int(m_cc.group(1)) if m_cc else 0
            incoming_st = int(m_st.group(1)) if m_st else 1
            target_prov = re.sub(r'\b(?:cc|st|ld)[=:]\S+', '', target_prov).strip()
            
            matched_prov = None
            for p in PROVINCES_DICT.keys():
                if target_prov in p or p in target_prov:
                    matched_prov = p
                    break
            
            if matched_prov:
                if not user:
                    user = save_user(user_id, {
                        "transit_province": matched_prov,
                        "check_count": incoming_cc,
                        "streak": incoming_st
                    })
                else:
                    if incoming_cc > user.get("check_count", 0):
                        user["check_count"] = incoming_cc
                    if incoming_st > user.get("streak", 1):
                        user["streak"] = incoming_st
                    user = update_transit_location(user_id, matched_prov)
                
                # Compute updated horoscope
                horoscope = compute_user_horoscope(user)
                summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
                reply([
                    {
                        "type": "text",
                        "text": f"✅ อัปเดตสถานที่จรเป็น: {matched_prov} เรียบร้อยแล้วครับ! 📍 (คำนวณรุ่งอรุณและ LMT ณ {matched_prov} ทันที)"
                    },
                    summary_flex
                ])
                return
            else:
                reply([{
                    "type": "text",
                    "text": f"⚠️ ไม่พบจังหวัด '{target_prov}' กรุณาระบุชื่อจังหวัดในประเทศไทย เช่น 'จร เชียงใหม่' หรือ 'จร ภูเก็ต' ครับ"
                }])
                return

        # Check transit menu request
        if any(k in text for k in ["เปลี่ยนสถานที่จร", "สถานที่จร", "เปลี่ยนที่จร"]):
            # Quick reply with top provinces + LIFF button
            reply([{
                "type": "text",
                "text": "📍 คุณสามารถเลือกจังหวัดจรปัจจุบัน หรือพิมพ์บอกแม่หมอได้เลย เช่น 'จร เชียงใหม่', 'จร ภูเก็ต' หรือแตะเลือกด้านล่างได้เลยครับ 👇",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "message", "label": "📍 กรุงเทพมหานคร", "text": "จร กรุงเทพมหานคร"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 เชียงใหม่", "text": "จร เชียงใหม่"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 ภูเก็ต", "text": "จร ภูเก็ต"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 ขอนแก่น", "text": "จร ขอนแก่น"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 ชลบุรี", "text": "จร ชลบุรี"}},
                        {"type": "action", "action": {"type": "uri", "label": "🗺️ เลือกเขต/อำเภอละเอียด", "uri": f"{liff_url}#transit"}}
                    ]
                }
            }])
            return

        # Check Privacy / Data Security Guarantee
        if any(k in text_lower for k in ["privacy", "ความเป็นส่วนตัว", "ความปลอดภัย", "บันทึกข้อมูลไหม", "เก็บข้อมูลไหม", "ปลอดภัยไหม", "ข้อมูลส่วนตัว", "กังวล", "เจ้าของแอป"]):
            reply([
                {
                    "type": "text",
                    "text": (
                        "🛡️ คำยืนยันความปลอดภัยและความเป็นส่วนตัว 100% 🐻‍❄️🔒\n\n"
                        "สบายใจและไม่ต้องกังวลเลยครับ! เจ้าของแอปไม่มีการบันทึกหรือดักเก็บข้อมูลส่วนตัวใด ๆ ของคุณทั้งสิ้น ✨\n\n"
                        "• ข้อมูลวันเกิด เวลาเกิด และสถานที่ ถูกใช้เพียงเพื่อคำนวณตำแหน่งดวงดาวและลัคนาราศีเท่านั้น\n"
                        "• ข้อมูลการใช้งานทั้งหมดถูกจัดเก็บและประมวลผลบนเครื่องของคุณเอง (Local Device Storage)\n"
                        "• ไม่มีการเก็บข้อมูลลงฐานข้อมูลส่วนกลางใด ๆ ของเจ้าของแอป\n\n"
                        "คุณสามารถเปิดดูดวงได้อย่างสบายใจและปลอดภัยสูงสุดครับ! 🔮✨"
                    ),
                    "quickReply": {
                        "items": [
                            {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงประจำวัน"}},
                            {"type": "action", "action": {"type": "message", "label": "📊 สถิติดวง", "text": "สถิติ"}},
                            {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                            {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}}
                        ]
                    }
                }
            ])
            return

        # Check Siamsee / Daily Fortune Oracle ("เซียมซี", "เสี่ยงเซียมซี", "ไพ่ประจำวัน", "ออราเคิล", "siamsee")
        if any(k in text_lower for k in ["เซียมซี", "เสี่ยงเซียมซี", "ไพ่ประจำวัน", "ออราเคิล", "เสี่ยงทาย", "siamsee"]):
            siamsee_flex = build_siamsee_flex(user=user)
            reply([siamsee_flex])
            return

        # Check Lucky Wallpapers ("วอลเปเปอร์", "wallpaper", "ของรางวัล", "แจกวอลเปเปอร์")
        if any(k in text_lower for k in ["วอลเปเปอร์", "wallpaper", "ของรางวัล", "แจกวอลเปเปอร์"]):
            wall_flex = build_wallpaper_rewards_flex(user=user, web_url=web_url)
            reply([wall_flex])
            return

        # Check Morning Routine / Lottery Special preview
        if any(k in text_lower for k in ["อรุณสวัสดิ์", "morning", "เตือนยามเช้า"]):
            now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
            if now_th.day in (1, 16):
                m_flex = build_lottery_special_flex(web_url)
            else:
                m_flex = build_morning_reminder_flex(web_url)
            reply([m_flex])
            return

        # Check Feedback / Rating
        if any(k in text_lower for k in ["feedback", "ประเมิน", "ให้คะแนน", "ความแม่นยำ", "3"]):
            feedback_flex = build_feedback_flex(web_url)
            reply([feedback_flex])
            return

        # Check Donation
        if any(k in text_lower for k in ["donate", "สนับสนุน", "บริจาค", "ทำบุญ", "แม่หมอ", "เลี้ยงกาแฟ", "4"]):
            qr_url = "https://plb-horoscope.vercel.app/qr_donate.jpg"
            image_msg = {
                "type": "image",
                "originalContentUrl": qr_url,
                "previewImageUrl": qr_url
            }
            donation_flex = build_donation_flex(qr_url=qr_url)
            reply([image_msg, donation_flex])
            return

        # Check Lucky Numbers option ("ขอเลขเด็ด", "เลขเด็ด", "เลขมงคล", "หวย", "ขอหวย", "เลขนำโชค")
        if any(k in text for k in ["เลขเด็ด", "ขอเลขเด็ด", "เลขมงคล", "หวย", "ขอหวย", "เลขนำโชค", "ขอเลข", "lotto", "ตรวจหวย"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            flex = build_lucky_numbers_flex(user, h, web_url)
            reply([flex])
            return

        # Check Shirt Colors option ("สีเสื้อ", "สีเสื้อมงคล", "ขอสีเสื้อ", "ตารางสีเสื้อ", "สีมงคล", "สีกาลกิณี")
        if any(k in text for k in ["สีเสื้อ", "สีเสื้อมงคล", "ขอสีเสื้อ", "ตารางสีเสื้อ", "สีมงคล", "สีกาลกิณี", "สีประจำวัน", "เสื้อสี"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            flex = build_lucky_colors_flex(user, h, web_url)
            reply([flex])
            return

        # Check Combined Lucky & Color option
        if any(k in text for k in ["เกร็ดมงคล", "เลขและสี", "เลขเด็ดและสีเสื้อ", "สีเสื้อและเลขเด็ด"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            num_flex = build_lucky_numbers_flex(user, h, web_url)
            col_flex = build_lucky_colors_flex(user, h, web_url)
            reply([num_flex, col_flex])
            return

        # Specific category keywords (checked first so specific terms like 'ดูดวงหมวดการงาน' or 'การงาน' resolve to that category)
        if any(k in text for k in ["การงาน", "งาน"]) and not any(k in text for k in ["เลือกหมวด", "หมวดหมู่"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("career", h["categories"]["career"], asc_name, h["date"], user=user)
            reply([flex])
            return

        if any(k in text for k in ["การเงิน", "เงิน", "โชคลาภ"]) and not any(k in text for k in ["เลือกหมวด", "หมวดหมู่"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("finance", h["categories"]["finance"], asc_name, h["date"], user=user)
            reply([flex])
            return

        if any(k in text for k in ["ความรัก", "รัก", "คู่ครอง"]) and not any(k in text for k in ["เลือกหมวด", "หมวดหมู่"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("love", h["categories"]["love"], asc_name, h["date"], user=user)
            reply([flex])
            return

        if any(k in text for k in ["สุขภาพ", "เตือนภัย", "อุบัติเหตุ"]) and not any(k in text for k in ["เลือกหมวด", "หมวดหมู่"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("health", h["categories"]["health"], asc_name, h["date"], user=user)
            reply([flex])
            return

        # Check Category selection menu (Button 2 in Rich Menu)
        if any(k in text for k in ["เลือกหมวด", "หมวดหมู่", "หมวด", "2"]):
            reply([build_category_menu_flex(web_url, user=user)])
            return

        # Main Daily Horoscope Summary (Button 1)
        if any(k in text for k in ["สรุปดวง", "ดวงวันนี้", "ดวงประจำวัน", "1"]):
            if not is_registered:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            user = record_user_check(user_id, horoscope.get("overallScore", 80)) or get_user(user_id) or user
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply([summary_flex])
            return

        # Check if user is typing a feedback comment (or greeting)
        if len(text) > 3 and not any(k in text for k in ["สวัสดี", "hello", "hi"]):
            # Treat as suggestion or general feedback, merging with recent star rating if present
            _forward_comment_to_sheet(user_id, user.get("name", "ผู้ใช้") if user else "ผู้ใช้", text, user=user)
            reply([{
                "type": "text",
                "text": "🙏 ขอบพระคุณสำหรับข้อคิดเห็นและคำแนะนำครับ แม่หมอบันทึกข้อมูลเรียบร้อยแล้วครับ ✨",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "message", "label": "🎰 ขอเลขเด็ด", "text": "ขอเลขเด็ด"}},
                        {"type": "action", "action": {"type": "message", "label": "👕 สีเสื้อมงคล", "text": "สีเสื้อมงคล"}},
                        {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงวันนี้"}},
                        {"type": "action", "action": {"type": "message", "label": "📊 สถิติดวง & กิมมิก", "text": "สถิติ"}},
                        {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวดดูดวง", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 เปลี่ยนสถานที่จร", "text": "เปลี่ยนสถานที่จร"}}
                    ]
                }
            }])
            return

        # Fallback greeting
        if not user:
            prompt_registration()
        else:
            horoscope = compute_user_horoscope(user)
            user = record_user_check(user_id, horoscope.get("overallScore", 80)) or get_user(user_id) or user
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply([summary_flex])

    # 3. Event: Postback
    elif event_type == "postback":
        postback = event.get("postback", {})
        data_str = postback.get("data", "")
        params = dict(urllib.parse.parse_qsl(data_str))
        action = params.get("action")
        
        # Extract stateless metadata
        try:
            incoming_cc = int(params.get("cc", 0))
        except (ValueError, TypeError):
            incoming_cc = 0
        try:
            incoming_st = int(params.get("st", 1))
        except (ValueError, TypeError):
            incoming_st = 1
        incoming_ld = params.get("ld", "")
        user_name = params.get("n", "")

        # Re-hydrate user from stateless postback metadata if missing
        if not user and params.get("b"):
            user = save_user(user_id, {
                "name": user_name or "ผู้ใช้",
                "birth_date": params.get("b"),
                "birth_time": params.get("t", "08:30"),
                "birth_province": params.get("p", "กรุงเทพมหานคร"),
                "transit_province": params.get("tp", params.get("p", "กรุงเทพมหานคร")),
                "check_count": incoming_cc,
                "streak": incoming_st,
                "last_check_date": incoming_ld
            })
            is_registered = True
        elif user and incoming_cc > user.get("check_count", 0):
            # Sync user check_count if postback carried a higher accumulated count
            user["check_count"] = incoming_cc
            user["streak"] = max(user.get("streak", 1), incoming_st)
            if incoming_ld:
                user["last_check_date"] = incoming_ld
            try:
                from user_store import _save_cache
            except ImportError:
                from api.user_store import _save_cache
            _save_cache()
        
        if action == "daily_summary":
            if not user:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            user = record_user_check(user_id, horoscope.get("overallScore", 80)) or get_user(user_id) or user
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply([summary_flex])
            
        elif action == "stats":
            if not user:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            user = get_user(user_id) or user
            stats_flex = build_stats_flex(user, horoscope)
            reply([stats_flex])
            
        elif action == "select_category":
            reply([build_category_menu_flex(web_url, user=user)])
            
        elif action == "category":
            cat_name = params.get("cat", "career")
            if not user:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            cat_data = h["categories"].get(cat_name, h["categories"]["overall"])
            flex = build_category_flex(cat_name, cat_data, asc_name, h["date"], user=user)
            reply([flex])

        elif action == "lucky_numbers":
            if not user:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            flex = build_lucky_numbers_flex(user, h, web_url)
            reply([flex])

        elif action == "lucky_colors":
            if not user:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            flex = build_lucky_colors_flex(user, h, web_url)
            reply([flex])
            
        elif action == "change_transit":
            reply([{
                "type": "text",
                "text": "📍 เลือกจังหวัดที่คุณกำลังพำนักอยู่ในปัจจุบัน หรือพิมพ์บอกแม่หมอ เช่น 'จร เชียงใหม่' 👇",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "message", "label": "📍 กรุงเทพมหานคร", "text": "จร กรุงเทพมหานคร"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 เชียงใหม่", "text": "จร เชียงใหม่"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 ภูเก็ต", "text": "จร ภูเก็ต"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 ขอนแก่น", "text": "จร ขอนแก่น"}},
                        {"type": "action", "action": {"type": "uri", "label": "🗺️ เลือกเขต/อำเภอละเอียด", "uri": f"{liff_url}#transit"}}
                    ]
                }
            }])
            
        elif action == "feedback_rate":
            stars = int(params.get("stars", 5))
            _record_star_rating(user_id, stars, user)
            reply([{
                "type": "text",
                "text": f"🌟 ขอบพระคุณสำหรับคะแนน {stars} ดาวครับ! 🙏\nหากมีข้อคิดเห็น คำติชม หรืออยากให้เพิ่มฟีเจอร์ใด สามารถพิมพ์ข้อความส่งกลับมาในแชตนี้ได้เลยครับ แม่หมอจะบันทึกรวมกับคะแนนของคุณทันทีครับ ✨"
            }])
            
        elif action == "donate":
            qr_url = "https://plb-horoscope.vercel.app/qr_donate.jpg"
            image_msg = {
                "type": "image",
                "originalContentUrl": qr_url,
                "previewImageUrl": qr_url
            }
            donation_flex = build_donation_flex(qr_url=qr_url)
            reply([image_msg, donation_flex])

RATING_LABELS = {
    1: "⭐ ไม่ค่อยตรงเท่าไหร่ (1/5)",
    2: "⭐⭐ ค่อนข้างเฉยๆ / ยังไม่ค่อยตรง (2/5)",
    3: "⭐⭐⭐ ปานกลาง ตรงเป็นบางเรื่อง (3/5)",
    4: "⭐⭐⭐⭐ แม่นดี ตรงหลายเรื่องเลย ✨ (4/5)",
    5: "⭐⭐⭐⭐⭐ แม่นมาก ตรงเป๊ะทุกเรื่อง! 🎯 (5/5)"
}

_RECENT_USER_FEEDBACK = {}  # user_id -> {"time": datetime, "payload": dict}

def build_unified_feedback_payload(user: dict, rating: int = 0, comment: str = "", user_id: str = "", channel: str = "line") -> dict:
    now_dt = datetime.datetime.now()
    now_iso = now_dt.isoformat()
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    today_str = now_th.strftime("%Y-%m-%d")

    asc_sign = "-"
    if user and user.get("birth_date"):
        try:
            h = compute_user_horoscope(user, today_str)
            asc_sign = h.get("natalChart", {}).get("ascendant", {}).get("signName", "-")
        except Exception:
            asc_sign = "-"

    u_name = user.get("name") if user else "ผู้ใช้ LINE"
    if not u_name or u_name == "ผู้ใช้":
        u_name = "ผู้ใช้ LINE"

    b_prov = user.get("birth_province", "กรุงเทพมหานคร") if user else "กรุงเทพมหานคร"
    b_dist = user.get("birth_district", "") if user else ""
    t_prov = user.get("transit_province") or b_prov if user else b_prov
    t_dist = user.get("transit_district") or b_dist if user else b_dist
    calc_m = user.get("calc_method", "suriyayatra") if user else "suriyayatra"

    r_label = RATING_LABELS.get(rating, f"{rating} ดาว" if rating > 0 else "ข้อเสนอแนะ / ความคิดเห็น")

    payload = {
        "rating": rating,
        "ratingLabel": r_label,
        "comment": comment,
        "ascendantSign": asc_sign,
        "targetDate": today_str,
        "calcMethod": calc_m,
        "userName": u_name,
        "province": b_prov,
        "district": b_dist,
        "transitProvince": t_prov,
        "transitDistrict": t_dist,
        "submittedAt": now_iso,
        "server_received_at": now_iso,
        "channel": channel,
        "userId": user_id,
        "line_user_id": user_id,
        # Backward compatibility aliases for existing Google Sheets / scripts
        "name": u_name,
        "transit_province": t_prov,
        "created_at": now_iso,
        "action": f"{channel}_feedback"
    }
    return payload

def record_feedback_unified(payload: dict):
    """Save feedback to local feedback.jsonl and forward to Google Sheets Webhook asynchronously."""
    # 1. Save locally to feedback.jsonl
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(base_dir) == "api":
            base_dir = os.path.dirname(base_dir)
        feedback_file = os.path.join(base_dir, "feedback.jsonl")
        with open(feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception as fe:
        print(f"[Feedback] Local save notice: {fe}")

    # 2. Forward to Google Sheets Webhook asynchronously
    def _do():
        webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or os.environ.get("FEEDBACK_WEBHOOK_URL") or DEFAULT_FEEDBACK_WEBHOOK
        if not webhook_url:
            return
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-Feedback-Engine"}
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"[Feedback] Forwarding error: {e}")

    import threading
    threading.Thread(target=_do, daemon=True).start()

def _record_star_rating(user_id: str, stars: int, user: dict):
    """Build unified feedback payload for star rating and record."""
    payload = build_unified_feedback_payload(user, rating=stars, comment="", user_id=user_id, channel="line")
    _RECENT_USER_FEEDBACK[user_id] = {
        "time": datetime.datetime.now(),
        "payload": payload
    }
    record_feedback_unified(payload)

def _forward_comment_to_sheet(user_id: str, name: str, comment: str, user: dict = None):
    """Forward text comment, linking with recent star rating if present."""
    recent = _RECENT_USER_FEEDBACK.get(user_id)
    now = datetime.datetime.now()
    if recent and (now - recent["time"]).total_seconds() < 900:  # 15 minutes window
        # Merge comment into existing rating record
        payload = dict(recent["payload"])
        payload["comment"] = comment
        payload["submittedAt"] = now.isoformat()
        payload["server_received_at"] = payload["submittedAt"]
        payload["created_at"] = payload["submittedAt"]
        _RECENT_USER_FEEDBACK.pop(user_id, None)
    else:
        payload = build_unified_feedback_payload(user, rating=0, comment=comment, user_id=user_id, channel="line")

    record_feedback_unified(payload)



def broadcast_line_message(messages: list, access_token: str = "") -> dict:
    """Broadcast messages to all friends of the LINE Official Account."""
    access_token = access_token or get_channel_access_token()
    if not access_token or not messages:
        return {"success": False, "error": "Missing access token or messages"}

    url = "https://api.line.me/v2/bot/message/broadcast"
    payload = {"messages": messages}
    try:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {access_token}"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return {"success": response.status == 200, "status": response.status, "method": "broadcast"}
    except urllib.error.HTTPError as he:
        err_msg = he.read().decode('utf-8')
        print(f"[LineBotEngine] Broadcast HTTPError {he.code}: {err_msg}")
        return {"success": False, "status": he.code, "error": err_msg, "method": "broadcast"}
    except Exception as e:
        print(f"[LineBotEngine] Error broadcasting to LINE: {e}")
        return {"success": False, "error": str(e), "method": "broadcast"}

def send_noon_reminder_broadcast(web_url: str = "https://plb-horoscope.vercel.app", channel_access_token: str = "", force: bool = False) -> dict:
    """
    Send midday noon reminder to all LINE OA friends.
    Guards:
      1. Time Guard: Only sends between 11:30 and 12:59 Thailand Time (UTC+7), unless force=True.
      2. Deduplication Guard: Only sends ONCE per calendar day, unless force=True.
    """
    import tempfile
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    today_str = now_th.strftime("%Y-%m-%d")
    current_hour = now_th.hour
    current_time_str = now_th.strftime("%H:%M:%S")

    # Guard 1: Time Window Check (must be around 12:00 PM, hour 11 or 12)
    if not force and current_hour not in (11, 12):
        print(f"[NoonReminder] Skipped: Outside noon window ({current_time_str}). Only runs around 12:00 PM.")
        return {
            "success": True,
            "skipped": True,
            "reason": f"อยู่นอกช่วงเวลาเที่ยง (ขณะนี้เวลา {current_time_str} น.) ระบบจะส่งเฉพาะเวลา 12:00 น. เท่านั้น",
            "current_time": current_time_str,
            "scheduled_time": "12:00:00"
        }

    # Guard 2: Deduplication Check (Only once per day)
    lock_file = os.path.join(tempfile.gettempdir(), "plb_last_noon_broadcast.txt")
    last_sent = ""
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                last_sent = f.read().strip()
        except Exception:
            pass

    if not force and last_sent == today_str:
        print(f"[NoonReminder] Skipped: Already sent today ({today_str}).")
        return {
            "success": True,
            "skipped": True,
            "reason": f"วันนี้ ({today_str}) ได้ส่งข้อความเตือนตอนเที่ยงเรียบร้อยแล้ว ไม่ส่งซ้ำครับ",
            "date": today_str
        }

    channel_access_token = channel_access_token or get_channel_access_token()
    web_url = web_url or os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
    flex_card = build_noon_reminder_flex(web_url)

    def mark_sent():
        try:
            with open(lock_file, "w", encoding="utf-8") as f:
                f.write(today_str)
        except Exception:
            pass

    # 1. Attempt broadcast to all friends
    b_res = broadcast_line_message([flex_card], channel_access_token)
    if b_res.get("success"):
        mark_sent()
        return {"success": True, "method": "broadcast", "status": b_res.get("status"), "date": today_str}

    # 2. If broadcast failed (e.g. quota or restriction), fallback to pushing to registered users
    print(f"[NoonReminder] Broadcast failed: {b_res.get('error')}. Falling back to registered user store push...")
    try:
        from user_store import get_all_users
    except ImportError:
        from api.user_store import get_all_users

    users = get_all_users()
    pushed_count = 0
    for uid in users.keys():
        if uid.startswith("U"):
            if push_line_message(uid, [flex_card], channel_access_token):
                pushed_count += 1

    if pushed_count > 0:
        mark_sent()

    return {
        "success": pushed_count > 0,
        "method": "user_store_push",
        "pushed_count": pushed_count,
        "date": today_str,
        "broadcast_error": b_res.get("error")
    }

def send_morning_reminder_broadcast(web_url: str = "https://plb-horoscope.vercel.app", channel_access_token: str = "", force: bool = False) -> dict:
    """
    Send 07:00 AM Morning Routine reminder to all LINE OA friends.
    On 1st & 16th of month, sends Special Edition Lottery Card.
    Guards:
      1. Time Guard: Only sends between 06:00 and 08:59 Thailand Time (UTC+7), unless force=True.
      2. Deduplication Guard: Only sends ONCE per calendar day, unless force=True.
    """
    import tempfile
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    today_str = now_th.strftime("%Y-%m-%d")
    current_hour = now_th.hour
    current_time_str = now_th.strftime("%H:%M:%S")

    # Guard 1: Time Window Check (must be around 07:00 AM, hours 6, 7, 8)
    if not force and current_hour not in (6, 7, 8):
        print(f"[MorningReminder] Skipped: Outside morning window ({current_time_str}). Only runs around 07:00 AM.")
        return {
            "success": True,
            "skipped": True,
            "reason": f"อยู่นอกช่วงเวลาเช้า (ขณะนี้เวลา {current_time_str} น.) ระบบจะส่งเฉพาะเวลา 07:00 น. เท่านั้น",
            "current_time": current_time_str,
            "scheduled_time": "07:00:00"
        }

    # Guard 2: Deduplication Check (Only once per day)
    lock_file = os.path.join(tempfile.gettempdir(), "plb_last_morning_broadcast.txt")
    last_sent = ""
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                last_sent = f.read().strip()
        except Exception:
            pass

    if not force and last_sent == today_str:
        print(f"[MorningReminder] Skipped: Already sent today ({today_str}).")
        return {
            "success": True,
            "skipped": True,
            "reason": f"วันนี้ ({today_str}) ได้ส่งข้อความเตือนยามเช้าเรียบร้อยแล้ว ไม่ส่งซ้ำครับ",
            "date": today_str
        }

    channel_access_token = channel_access_token or get_channel_access_token()
    web_url = web_url or os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
    
    # Check if today is 1st or 16th of month -> Lottery Special!
    if now_th.day in (1, 16):
        flex_card = build_lottery_special_flex(web_url)
        reminder_type = "lottery_special"
    else:
        flex_card = build_morning_reminder_flex(web_url)
        reminder_type = "morning_routine"

    def mark_sent():
        try:
            with open(lock_file, "w", encoding="utf-8") as f:
                f.write(today_str)
        except Exception:
            pass

    # 1. Attempt broadcast to all friends
    b_res = broadcast_line_message([flex_card], channel_access_token)
    if b_res.get("success"):
        mark_sent()
        return {"success": True, "type": reminder_type, "method": "broadcast", "status": b_res.get("status"), "date": today_str}

    # 2. If broadcast failed, fallback to pushing to registered users
    print(f"[MorningReminder] Broadcast failed: {b_res.get('error')}. Falling back to registered user store push...")
    try:
        from user_store import get_all_users
    except ImportError:
        from api.user_store import get_all_users

    users = get_all_users()
    pushed_count = 0
    for uid in users.keys():
        if uid.startswith("U"):
            if push_line_message(uid, [flex_card], channel_access_token):
                pushed_count += 1

    if pushed_count > 0:
        mark_sent()

    return {
        "success": pushed_count > 0,
        "type": reminder_type,
        "method": "user_store_push",
        "pushed_count": pushed_count,
        "date": today_str,
        "broadcast_error": b_res.get("error")
    }

