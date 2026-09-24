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
DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"

# In-memory cache for fast lookup
_USER_CACHE = {}

def _load_cache():
    global _USER_CACHE
    for fpath in [LOCAL_USERS_FILE, TMP_USERS_FILE]:
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
        "created_at": existing.get("created_at", now),
        "updated_at": now
    }
    
    _USER_CACHE[line_user_id] = updated_profile
    _save_cache()
    
    # Sync with Google Sheets Webhook asynchronously/safely
    _sync_to_google_sheet("register", updated_profile)
    return updated_profile

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
    """Optionally sync user registration or update to Google Sheets Webhook."""
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
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        # Non-blocking warning
        print(f"Sync to Google Sheet notice: {e}")
