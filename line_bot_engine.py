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
import urllib.request
import urllib.parse
import datetime

from thai_astrology import get_horoscope, PROVINCES_DICT
from user_store import get_user, save_user, update_transit_location
from line_flex_builder import (
    build_welcome_flex,
    build_daily_summary_flex,
    build_category_flex,
    build_feedback_flex,
    build_donation_flex,
    build_share_flex,
    get_category_quick_reply
)

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

def reply_line_message(reply_token: str, messages: list, access_token: str = ""):
    """Send reply message(s) back to LINE user."""
    access_token = access_token or get_channel_access_token()
    if not access_token or not reply_token:
        print("[LineBotEngine] No access token or reply token provided")
        return False
    
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
        with urllib.request.urlopen(req, timeout=8) as response:
            return response.status == 200
    except Exception as e:
        print(f"[LineBotEngine] Error replying to LINE: {e}")
        return False

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
    
    liff_url = f"https://liff.line.me/{liff_id}" if liff_id else f"{web_url}/liff-register.html?userId={user_id}"
    
    # 1. Event: Follow (User adds LINE OA as friend)
    if event_type == "follow":
        welcome_flex = build_welcome_flex(liff_url)
        reply_line_message(reply_token, [welcome_flex], channel_access_token)
        return
    
    user = get_user(user_id)
    is_registered = bool(user and user.get("registered", False))
    
    # Helper for unregistered users
    def prompt_registration():
        welcome_flex = build_welcome_flex(liff_url)
        reply_line_message(reply_token, [
            {
                "type": "text",
                "text": "🔮 สวัสดีครับ! น้องหมียังไม่มีข้อมูลวันเกิดของคุณ กรุณาแตะปุ่ม 'ลงทะเบียนข้อมูลดวงชะตา' ด้านล่างเพื่อเริ่มคำนวณลัคนาราศีนะครับ 👇",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "uri", "label": "🌟 ลงทะเบียนวันเกิด", "uri": liff_url}},
                        {"type": "action", "action": {"type": "uri", "label": "👥 ชวนเพื่อนดูดวง", "uri": "https://line.me/R/nv/recommendOA/@374xcoto"}}
                    ]
                }
            },
            welcome_flex
        ], channel_access_token)

    # 2. Event: Message (Text)
    if event_type == "message":
        message = event.get("message", {})
        msg_type = message.get("type")
        
        if msg_type != "text":
            return
            
        text = message.get("text", "").strip()
        text_lower = text.lower()
        
        # Check registration commands
        if any(k in text for k in ["ลงทะเบียน", "แก้ไขข้อมูล", "ตั้งค่าดวง", "โปรไฟล์", "เปลี่ยนวันเกิด"]):
            welcome_flex = build_welcome_flex(liff_url)
            reply_line_message(reply_token, [welcome_flex], channel_access_token)
            return

        # Check Share LINE OA command
        if any(k in text for k in ["แชร์", "ชวนเพื่อน", "แชร์ให้เพื่อน", "share", "ชวน"]):
            reply_line_message(reply_token, [build_share_flex()], channel_access_token)
            return

        # Check Transit Location Change command e.g. "จร เชียงใหม่" หรือ "เปลี่ยนสถานที่จร"
        if text.startswith("จร ") or text.startswith("เปลี่ยนที่จร "):
            parts = text.split(maxsplit=1)
            target_prov = parts[1].strip() if len(parts) > 1 else ""
            matched_prov = None
            for p in PROVINCES_DICT.keys():
                if target_prov in p or p in target_prov:
                    matched_prov = p
                    break
            
            if matched_prov:
                if not user:
                    user = save_user(user_id, {"transit_province": matched_prov})
                else:
                    user = update_transit_location(user_id, matched_prov)
                
                # Compute updated horoscope
                horoscope = compute_user_horoscope(user)
                summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
                reply_line_message(reply_token, [
                    {
                        "type": "text",
                        "text": f"✅ อัปเดตสถานที่จรเป็น: {matched_prov} เรียบร้อยแล้วครับ! 📍 (คำนวณรุ่งอรุณและ LMT ณ {matched_prov} ทันที)"
                    },
                    summary_flex
                ], channel_access_token)
                return
            else:
                reply_line_message(reply_token, [{
                    "type": "text",
                    "text": f"⚠️ ไม่พบจังหวัด '{target_prov}' กรุณาระบุชื่อจังหวัดในประเทศไทย เช่น 'จร เชียงใหม่' หรือ 'จร ภูเก็ต' ครับ"
                }], channel_access_token)
                return

        # Check transit menu request
        if any(k in text for k in ["เปลี่ยนสถานที่จร", "สถานที่จร", "เปลี่ยนที่จร"]):
            # Quick reply with top provinces + LIFF button
            reply_line_message(reply_token, [{
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
            }], channel_access_token)
            return

        # Check Feedback / Rating
        if any(k in text_lower for k in ["feedback", "ประเมิน", "ให้คะแนน", "ความแม่นยำ", "3"]):
            feedback_flex = build_feedback_flex()
            reply_line_message(reply_token, [feedback_flex], channel_access_token)
            return

        # Check Donation
        if any(k in text_lower for k in ["donate", "สนับสนุน", "บริจาค", "ทำบุญ", "4"]):
            donation_flex = build_donation_flex()
            reply_line_message(reply_token, [donation_flex], channel_access_token)
            return

        # Check Category selection
        if any(k in text for k in ["เลือกหมวด", "หมวดหมู่", "ดูดวง", "2"]):
            reply_line_message(reply_token, [{
                "type": "text",
                "text": "🔮 เลือกหมวดดูดวงที่ท่านต้องการเจาะลึกได้เลยครับ 👇",
                "quickReply": get_category_quick_reply()
            }], channel_access_token)
            return

        # Specific category keywords
        if any(k in text for k in ["การงาน", "งาน"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("career", h["categories"]["career"], asc_name, h["date"])
            reply_line_message(reply_token, [flex], channel_access_token)
            return

        if any(k in text for k in ["การเงิน", "เงิน", "โชคลาภ"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("finance", h["categories"]["finance"], asc_name, h["date"])
            reply_line_message(reply_token, [flex], channel_access_token)
            return

        if any(k in text for k in ["ความรัก", "รัก", "คู่ครอง"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("love", h["categories"]["love"], asc_name, h["date"])
            reply_line_message(reply_token, [flex], channel_access_token)
            return

        if any(k in text for k in ["สุขภาพ", "เตือนภัย", "อุบัติเหตุ"]):
            if not is_registered:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            flex = build_category_flex("health", h["categories"]["health"], asc_name, h["date"])
            reply_line_message(reply_token, [flex], channel_access_token)
            return

        # Main Daily Horoscope Summary (Button 1)
        if any(k in text for k in ["สรุปดวง", "ดวงวันนี้", "ดวงประจำวัน", "1"]):
            if not is_registered:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply_line_message(reply_token, [summary_flex], channel_access_token)
            return

        # Check if user is typing a feedback comment (or greeting)
        if len(text) > 3 and not any(k in text for k in ["สวัสดี", "hello", "hi"]):
            # Treat as suggestion or general feedback
            _forward_comment_to_sheet(user_id, user.get("name", "ผู้ใช้") if user else "ผู้ใช้", text)
            reply_line_message(reply_token, [{
                "type": "text",
                "text": "🙏 ขอบพระคุณสำหรับข้อความและคำแนะนำครับ แม่หมอบันทึกข้อมูลเรียบร้อยแล้วครับ ✨",
                "quickReply": {
                    "items": [
                        {"type": "action", "action": {"type": "message", "label": "🌟 สรุปดวงวันนี้", "text": "สรุปดวงวันนี้"}},
                        {"type": "action", "action": {"type": "message", "label": "🔮 เลือกหมวดดูดวง", "text": "เลือกหมวดอยากจะดูหมวดไหน"}},
                        {"type": "action", "action": {"type": "message", "label": "📍 เปลี่ยนสถานที่จร", "text": "เปลี่ยนสถานที่จร"}}
                    ]
                }
            }], channel_access_token)
            return

        # Fallback greeting
        if not user:
            prompt_registration()
        else:
            horoscope = compute_user_horoscope(user)
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply_line_message(reply_token, [summary_flex], channel_access_token)

    # 3. Event: Postback
    elif event_type == "postback":
        postback = event.get("postback", {})
        data_str = postback.get("data", "")
        params = dict(urllib.parse.parse_qsl(data_str))
        action = params.get("action")
        
        if action == "daily_summary":
            if not user:
                prompt_registration()
                return
            horoscope = compute_user_horoscope(user)
            summary_flex = build_daily_summary_flex(user, horoscope, liff_url, web_url)
            reply_line_message(reply_token, [summary_flex], channel_access_token)
            
        elif action == "select_category":
            reply_line_message(reply_token, [{
                "type": "text",
                "text": "🔮 เลือกหมวดดูดวงที่ท่านต้องการเจาะลึกได้เลยครับ 👇",
                "quickReply": get_category_quick_reply()
            }], channel_access_token)
            
        elif action == "category":
            cat_name = params.get("cat", "career")
            if not user:
                prompt_registration()
                return
            h = compute_user_horoscope(user)
            asc_name = h["natalChart"]["ascendant"]["signName"]
            cat_data = h["categories"].get(cat_name, h["categories"]["overall"])
            flex = build_category_flex(cat_name, cat_data, asc_name, h["date"])
            reply_line_message(reply_token, [flex], channel_access_token)
            
        elif action == "change_transit":
            reply_line_message(reply_token, [{
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
            }], channel_access_token)
            
        elif action == "feedback_rate":
            stars = int(params.get("stars", 5))
            _record_star_rating(user_id, stars, user)
            reply_line_message(reply_token, [{
                "type": "text",
                "text": f"🌟 ขอบพระคุณสำหรับคะแนน {stars} ดาวครับ! 🙏\nหากมีข้อคิดเห็น คำติชม หรืออยากให้เพิ่มฟีเจอร์ใด สามารถพิมพ์ข้อความส่งกลับมาในแชตนี้ได้เลยครับ แม่หมอจะบันทึกไว้พัฒนาต่อไปครับ ✨"
            }], channel_access_token)
            
        elif action == "donate":
            donation_flex = build_donation_flex()
            reply_line_message(reply_token, [donation_flex], channel_access_token)

def _record_star_rating(user_id: str, stars: int, user: dict):
    """Forward star rating to Google Sheets Webhook."""
    webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or DEFAULT_FEEDBACK_WEBHOOK
    payload = {
        "action": "line_feedback_rating",
        "rating": stars,
        "line_user_id": user_id,
        "name": user.get("name") if user else "ผู้ใช้",
        "transit_province": user.get("transit_province", "") if user else "",
        "created_at": datetime.datetime.now().isoformat()
    }
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-LineBot"}
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        print(f"Error forwarding rating: {e}")

def _forward_comment_to_sheet(user_id: str, name: str, comment: str):
    """Forward text comment to Google Sheets Webhook."""
    webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or DEFAULT_FEEDBACK_WEBHOOK
    payload = {
        "action": "line_feedback_comment",
        "comment": comment,
        "line_user_id": user_id,
        "name": name,
        "created_at": datetime.datetime.now().isoformat()
    }
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-LineBot"}
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        print(f"Error forwarding comment: {e}")
