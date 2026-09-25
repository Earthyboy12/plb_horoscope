#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Store for LINE OA Thai Astrology Bot
Handles persistent storage of user birth charts and transit locations.
Supports local JSON storage + optional Google Sheets Webhook synchronization.
"""

import json
import os
import datetime
import urllib.request

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_USERS_FILE = os.path.join(tempfile.gettempdir(), "line_users.json")
LOCAL_USERS_FILE = os.path.join(BASE_DIR, "line_users.json")
PARENT_USERS_FILE = os.path.join(os.path.dirname(BASE_DIR), "line_users.json")
DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"

# In-memory cache for fast lookup
_USER_CACHE = {}

def _load_cache():
    global _USER_CACHE
    for fpath in [LOCAL_USERS_FILE, PARENT_USERS_FILE, TMP_USERS_FILE]:
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        _USER_CACHE.update(data)
            except Exception as e:
                pass
    return _USER_CACHE

def _save_cache():
    for fpath in [TMP_USERS_FILE, LOCAL_USERS_FILE]:
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(_USER_CACHE, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

# Initialize cache on module load
_load_cache()

def get_user(line_user_id: str):
    """Retrieve user birth profile and transit location by LINE User ID."""
    if not line_user_id:
        return None
    return _USER_CACHE.get(line_user_id)

def save_user(line_user_id: str, data: dict):
    """Save or update user profile."""
    if not line_user_id:
        return False
    
    now = datetime.datetime.now().isoformat()
    existing = _USER_CACHE.get(line_user_id, {})
    
    # Merge data
    updated_profile = {
        "line_user_id": line_user_id,
        "name": data.get("name") or existing.get("name") or "ผู้ใช้",
        "birth_date": data.get("birth_date") or data.get("birthDate") or existing.get("birth_date", "1995-08-12"),
        "birth_time": data.get("birth_time") or data.get("birthTime") or existing.get("birth_time", "08:30"),
        "birth_province": data.get("birth_province") or data.get("province") or existing.get("birth_province", "กรุงเทพมหานคร"),
        "birth_district": data.get("birth_district") or data.get("district") or existing.get("birth_district", "พระนคร"),
        "calc_method": data.get("calc_method") or data.get("calcMethod") or existing.get("calc_method", "suriyayatra"),
        "transit_province": data.get("transit_province") or data.get("transitProvince") or existing.get("transit_province") or data.get("birth_province") or "กรุงเทพมหานคร",
        "transit_district": data.get("transit_district") or data.get("transitDistrict") or existing.get("transit_district") or data.get("birth_district") or "พระนคร",
        "registered": True,
        "check_count": existing.get("check_count", 0),
        "streak": existing.get("streak", 1),
        "last_check_date": existing.get("last_check_date", ""),
        "created_at": existing.get("created_at", now),
        "updated_at": now
    }
    
    _USER_CACHE[line_user_id] = updated_profile
    _save_cache()
    
    # Sync with Google Sheets Webhook asynchronously/safely
    _sync_to_google_sheet("register", updated_profile)
    return updated_profile

def record_user_check(line_user_id: str, daily_score: int = 80):
    """Increment user check count, record streak and daily score history."""
    if not line_user_id:
        return
    user = _USER_CACHE.get(line_user_id)
    if not user:
        return
    
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    today_str = now_th.strftime("%Y-%m-%d")
    
    user["check_count"] = user.get("check_count", 0) + 1
    last_date = user.get("last_check_date", "")
    current_streak = user.get("streak", 1)
    
    if last_date == today_str:
        pass  # Already checked today
    elif last_date:
        try:
            last_dt = datetime.datetime.strptime(last_date, "%Y-%m-%d")
            diff = (now_th.date() - last_dt.date()).days
            if diff == 1:
                current_streak += 1
            elif diff > 1:
                current_streak = 1
        except Exception:
            current_streak = 1
    else:
        current_streak = 1
        
    user["streak"] = current_streak
    user["last_check_date"] = today_str
    
    # Keep score history (last 14 check records)
    history = user.get("history", [])
    history.append({
        "date": today_str,
        "score": daily_score,
        "time": now_th.strftime("%H:%M")
    })
    user["history"] = history[-14:]
    
    _save_cache()
    _sync_to_google_sheet("check_stats", user)
    return user

def get_rank_title(check_count: int = 1, streak: int = 1) -> dict:
    """Get playful astrological rank and badges based on check count & streak (7 Tiers)."""
    if check_count >= 50 or streak >= 21:
        return {
            "tier": 7,
            "title": "👑 มหาจักรพรรดิ์สายมู",
            "badge": "ระดับ 7 • เกณฑ์วาสนาสูงสุด 👑",
            "color": "#fbbf24",
            "perk": "เกียรติยศสูงสุดแห่งจักรวาล PLB สถิติของคุณอยู่ในกลุ่มท็อป 1% ผู้อยู่เหนือกระแสดาวชะตาอย่างแท้จริง ✨"
        }
    elif check_count >= 35 or streak >= 15:
        return {
            "tier": 6,
            "title": "💎 เทพพยากรณ์จักรวาล",
            "badge": "ระดับ 6 • วิสุทธิญาณ 💎",
            "color": "#60a5fa",
            "perk": "เกณฑ์วาสนาอยู่ในกลุ่มท็อป 3% ดึงดูดพลังมงคลและหยั่งรู้จังหวะโชคชะตาได้อย่างแม่นยำ 🔮"
        }
    elif check_count >= 21 or streak >= 11:
        return {
            "tier": 5,
            "title": "🛡️ ปรมาจารย์ค้ำดวง",
            "badge": "ระดับ 5 • เหนือดวงชะตา 🛡️",
            "color": "#f472b6",
            "perk": "สถิติสะท้อนความสม่ำเสมอ พลังดวงชะตาเข้มแข็ง เกณฑ์ร้ายกลับกลายเป็นดีอย่างอัศจรรย์ ✨"
        }
    elif check_count >= 14 or streak >= 7:
        return {
            "tier": 4,
            "title": "🔮 ศิษย์เอกแม่หมอ PLB",
            "badge": "ระดับ 4 • ขั้นสูง 🔮",
            "color": "#c084fc",
            "perk": "ตรวจดวงสม่ำเสมอ ดาวพฤหัสบดีเริ่มคุ้มครองชะตา มั่นใจในทุกการตัดสินใจสำคัญ 🌟"
        }
    elif check_count >= 7 or streak >= 4:
        return {
            "tier": 3,
            "title": "🌟 ผู้หยั่งรู้กระแสดวง",
            "badge": "ระดับ 3 • หยั่งรู้ทิศทาง 🌟",
            "color": "#34d399",
            "perk": "เริ่มกุมจังหวะชีวิตได้คล่องแคล่ว โชคลาภเปิดรับอย่างเด่นชัด เช็กต่อเนื่องเพื่อก้าวสู่ระดับ 4!"
        }
    elif check_count >= 3 or streak >= 2:
        return {
            "tier": 2,
            "title": "⚡ นักสำรวจดวงชะตา",
            "badge": "ระดับ 2 • จุดประกายโชค ⚡",
            "color": "#38bdf8",
            "perk": "เริ่มจับทางกระแสดาวได้ดีเยี่ยม เช็กต่อเนื่องทุกวันเพื่อสะสมแต้มวาสนาสู่ขั้นถัดไป!"
        }
    else:
        return {
            "tier": 1,
            "title": "🌱 ผู้เริ่มต้นสู่ดวงดาว",
            "badge": "ระดับ 1 • สมาชิกใหม่ 🌱",
            "color": "#94a3b8",
            "perk": "ก้าวแรกแห่งการเปิดดวงชะตา ขอต้อนรับสู่จักรวาล PLB โหราศาสตร์ครับ ✨"
        }

def update_transit_location(line_user_id: str, transit_province: str, transit_district: str = ""):
    """Update current transit location for the user."""
    user = _USER_CACHE.get(line_user_id)
    if not user:
        return None
    
    now = datetime.datetime.now().isoformat()
    user["transit_province"] = transit_province
    user["transit_district"] = transit_district or ("พระนคร" if transit_province == "กรุงเทพมหานคร" else f"อำเภอเมือง{transit_province}")
    user["updated_at"] = now
    
    _save_cache()
    _sync_to_google_sheet("update_transit", user)
    return user

def _sync_to_google_sheet(action_type: str, data: dict):
    """Optionally sync user registration or update to Google Sheets Webhook asynchronously."""
    def _do_sync():
        webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or DEFAULT_WEBHOOK_URL
        if not webhook_url:
            return
        
        payload = {
            "action": f"line_user_{action_type}",
            "timestamp": datetime.datetime.now().isoformat(),
            **data
        }
        
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-LineBot"}
            )
            urllib.request.urlopen(req, timeout=4)
        except Exception as e:
            # Non-blocking warning
            print(f"Sync to Google Sheet notice: {e}")

    import threading
    threading.Thread(target=_do_sync, daemon=True).start()


def get_all_users() -> dict:
    """Return dictionary of all registered users."""
    _load_cache()
    return dict(_USER_CACHE)
