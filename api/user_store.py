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
                        for uid, prof in data.items():
                            if uid in _USER_CACHE:
                                # Preserve higher check count and streak
                                existing_cc = _USER_CACHE[uid].get("check_count", 0)
                                new_cc = prof.get("check_count", 0)
                                if new_cc > existing_cc:
                                    _USER_CACHE[uid] = prof
                                else:
                                    # Merge non-stat fields
                                    for k, v in prof.items():
                                        if k not in ["check_count", "streak", "last_check_date", "history"] and v:
                                            _USER_CACHE[uid][k] = v
                            else:
                                _USER_CACHE[uid] = prof
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
    if line_user_id not in _USER_CACHE:
        _load_cache()
    return _USER_CACHE.get(line_user_id)

def get_rank_title(check_count: int = 1, streak: int = 1, xp: int = 0) -> dict:
    """Get playful astrological rank and badges based on XP, check count & streak (7 Tiers)."""
    if xp >= 1200 or check_count >= 50 or streak >= 21:
        return {
            "tier": 7,
            "title": "👑 มหาจักรพรรดิ์สายมู",
            "badge": "ระดับ 7 • เกณฑ์วาสนาสูงสุด 👑",
            "color": "#fbbf24",
            "perk": "เกียรติยศสูงสุดแห่งจักรวาล PLB สถิติของคุณอยู่ในกลุ่มท็อป 1% ผู้อยู่เหนือกระแสดาวชะตาอย่างแท้จริง ✨"
        }
    elif xp >= 800 or check_count >= 35 or streak >= 15:
        return {
            "tier": 6,
            "title": "💎 เทพพยากรณ์จักรวาล",
            "badge": "ระดับ 6 • วิสุทธิญาณ 💎",
            "color": "#60a5fa",
            "perk": "เกณฑ์วาสนาอยู่ในกลุ่มท็อป 3% ดึงดูดพลังมงคลและหยั่งรู้จังหวะโชคชะตาได้อย่างแม่นยำ 🔮"
        }
    elif xp >= 500 or check_count >= 21 or streak >= 11:
        return {
            "tier": 5,
            "title": "🛡️ ปรมาจารย์ค้ำดวง",
            "badge": "ระดับ 5 • เหนือดวงชะตา 🛡️",
            "color": "#f472b6",
            "perk": "สถิติสะท้อนความสม่ำเสมอ พลังดวงชะตาเข้มแข็ง เกณฑ์ร้ายกลับกลายเป็นดีอย่างอัศจรรย์ ✨"
        }
    elif xp >= 300 or check_count >= 14 or streak >= 7:
        return {
            "tier": 4,
            "title": "🔮 ศิษย์เอกแม่หมอ PLB",
            "badge": "ระดับ 4 • ขั้นสูง 🔮",
            "color": "#c084fc",
            "perk": "ตรวจดวงสม่ำเสมอ ดาวพฤหัสบดีเริ่มคุ้มครองชะตา มั่นใจในทุกการตัดสินใจสำคัญ 🌟"
        }
    elif xp >= 150 or check_count >= 7 or streak >= 4:
        return {
            "tier": 3,
            "title": "🌟 ผู้หยั่งรู้กระแสดวง",
            "badge": "ระดับ 3 • หยั่งรู้ทิศทาง 🌟",
            "color": "#34d399",
            "perk": "เริ่มกุมจังหวะชีวิตได้คล่องแคล่ว โชคลาภเปิดรับอย่างเด่นชัด เช็กต่อเนื่องเพื่อก้าวสู่ระดับ 4!"
        }
    elif xp >= 50 or check_count >= 3 or streak >= 2:
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

def save_user(line_user_id: str, data: dict):
    """Save or update user profile while safely preserving check_count, streak, and xp."""
    if not line_user_id:
        return False
    
    now = datetime.datetime.now().isoformat()
    existing = get_user(line_user_id) or {}
    
    # Extract incoming check_count / streak / xp / last_check_date from data or short keys
    try:
        incoming_cc = int(data.get("check_count") or data.get("cc") or 0)
    except (ValueError, TypeError):
        incoming_cc = 0
    existing_cc = int(existing.get("check_count", 0))
    final_cc = max(incoming_cc, existing_cc)
    
    try:
        incoming_st = int(data.get("streak") or data.get("st") or 1)
    except (ValueError, TypeError):
        incoming_st = 1
    existing_st = int(existing.get("streak", 1))
    final_st = max(incoming_st, existing_st)

    try:
        incoming_xp = int(data.get("xp") or 0)
    except (ValueError, TypeError):
        incoming_xp = 0
    existing_xp = int(existing.get("xp", 0))
    final_xp = max(incoming_xp, existing_xp)
    
    final_ld = data.get("last_check_date") or data.get("ld") or existing.get("last_check_date", "")
    
    rank_info = get_rank_title(final_cc if final_cc > 0 else 1, final_st, final_xp)
    
    # Merge data
    updated_profile = {
        "line_user_id": line_user_id,
        "name": data.get("name") or data.get("n") or existing.get("name") or "ผู้ใช้",
        "birth_date": data.get("birth_date") or data.get("birthDate") or data.get("b") or existing.get("birth_date", "1995-08-12"),
        "birth_time": data.get("birth_time") or data.get("birthTime") or data.get("t") or existing.get("birth_time", "08:30"),
        "birth_province": data.get("birth_province") or data.get("province") or data.get("p") or existing.get("birth_province", "กรุงเทพมหานคร"),
        "birth_district": data.get("birth_district") or data.get("district") or existing.get("birth_district", "พระนคร"),
        "calc_method": data.get("calc_method") or data.get("calcMethod") or existing.get("calc_method", "suriyayatra"),
        "transit_province": data.get("transit_province") or data.get("transitProvince") or data.get("tp") or existing.get("transit_province") or data.get("birth_province") or "กรุงเทพมหานคร",
        "transit_district": data.get("transit_district") or data.get("transitDistrict") or existing.get("transit_district") or data.get("birth_district") or "พระนคร",
        "registered": True,
        "check_count": final_cc if final_cc > 0 else 1,
        "streak": final_st,
        "xp": final_xp,
        "level": rank_info["tier"],
        "last_check_date": final_ld,
        "history": existing.get("history") or data.get("history") or [],
        "last_partner": data.get("last_partner") or existing.get("last_partner"),
        "created_at": existing.get("created_at", now),
        "updated_at": now
    }
    
    _USER_CACHE[line_user_id] = updated_profile
    _save_cache()
    
    # Sync with Google Sheets Webhook asynchronously/safely
    _sync_to_google_sheet("register", updated_profile)
    return updated_profile

def record_user_check(line_user_id: str, daily_score: int = 80):
    """Increment user check/message count, record streak, xp, and daily score history."""
    if not line_user_id:
        return None
    user = get_user(line_user_id)
    now_th = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    today_str = now_th.strftime("%Y-%m-%d")
    
    if not user:
        user = {
            "line_user_id": line_user_id,
            "name": "ผู้ใช้",
            "registered": False,
            "check_count": 0,
            "streak": 1,
            "xp": 5,
            "level": 1,
            "last_check_date": today_str,
            "history": [],
            "created_at": now_th.isoformat()
        }
    
    user["check_count"] = user.get("check_count", 0) + 1
    user["xp"] = user.get("xp", 0) + 5
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
    
    rank_info = get_rank_title(user.get("check_count", 1), user.get("streak", 1), user.get("xp", 0))
    user["level"] = rank_info["tier"]
    
    # Keep score history (last 14 check records)
    history = user.get("history", [])
    if daily_score:
        history.append({
            "date": today_str,
            "score": daily_score,
            "time": now_th.strftime("%H:%M")
        })
    user["history"] = history[-14:]
    
    _USER_CACHE[line_user_id] = user
    _save_cache()
    _sync_to_google_sheet("check_stats", user)
    return user

def update_transit_location(line_user_id: str, transit_province: str, transit_district: str = ""):
    """Update current transit location for the user."""
    user = _USER_CACHE.get(line_user_id)
    if not user:
        _load_cache()
        user = _USER_CACHE.get(line_user_id)
    if not user:
        user = save_user(line_user_id, {
            "transit_province": transit_province,
            "transit_district": transit_district
        })
        return user
    
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
