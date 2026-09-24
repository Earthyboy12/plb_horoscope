#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script to automatically register and upload the Rich Menu to LINE Messaging API.
Usage:
  python setup_line_rich_menu.py <CHANNEL_ACCESS_TOKEN>
Or set environment variable LINE_CHANNEL_ACCESS_TOKEN.
"""

import sys
import os
import json
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "rich_menu.png")

RICH_MENU_SCHEMA = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "PLB Horoscope Rich Menu",
    "chatBarText": "🔮 เมนูดูดวง",
    "areas": [
        # Top-Left: สรุปดวงประจำวัน
        {
            "bounds": {"x": 0, "y": 0, "width": 1250, "height": 843},
            "action": {
                "type": "message",
                "label": "สรุปดวงประจำวัน",
                "text": "สรุปดวงประจำวัน"
            }
        },
        # Top-Right: เลือกหมวดอยากจะดูหมวดไหน
        {
            "bounds": {"x": 1250, "y": 0, "width": 1250, "height": 843},
            "action": {
                "type": "message",
                "label": "เลือกหมวดดูดวง",
                "text": "เลือกหมวดอยากจะดูหมวดไหน"
            }
        },
        # Bottom-Left: ให้ feedback
        {
            "bounds": {"x": 0, "y": 843, "width": 1250, "height": 843},
            "action": {
                "type": "message",
                "label": "ให้ feedback",
                "text": "ให้ feedback"
            }
        },
        # Bottom-Right: สนับสนุนแม่หมอ
        {
            "bounds": {"x": 1250, "y": 843, "width": 1250, "height": 843},
            "action": {
                "type": "message",
                "label": "สนับสนุนแม่หมอ",
                "text": "สนับสนุนแม่หมอ"
            }
        }
    ]
}

def setup_rich_menu(access_token: str):
    if not access_token:
        print("❌ Error: Missing Channel Access Token.")
        print("Usage: python setup_line_rich_menu.py <YOUR_CHANNEL_ACCESS_TOKEN>")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Step 1: Create Rich Menu
    print("1. Creating Rich Menu definition via LINE API...")
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/richmenu",
        data=json.dumps(RICH_MENU_SCHEMA).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            rich_menu_id = data.get("richMenuId")
            print(f"   ✅ Rich Menu created! ID: {rich_menu_id}")
    except Exception as e:
        print(f"❌ Failed to create Rich Menu: {e}")
        return

    # Step 2: Upload Rich Menu Image
    print("2. Uploading Rich Menu image (rich_menu.png)...")
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file not found at {IMAGE_PATH}")
        return

    with open(IMAGE_PATH, "rb") as f:
        img_bytes = f.read()

    img_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "image/png"
    }
    upload_url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    req_upload = urllib.request.Request(upload_url, data=img_bytes, headers=img_headers, method="POST")
    try:
        with urllib.request.urlopen(req_upload) as resp:
            print("   ✅ Image uploaded successfully!")
    except Exception as e:
        print(f"❌ Failed to upload image: {e}")
        return

    # Step 3: Set as Default Rich Menu
    print("3. Setting as default Rich Menu for all users...")
    default_url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
    req_default = urllib.request.Request(default_url, data=b"", headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req_default) as resp:
            print("   ✅ Set as default Rich Menu successfully!")
    except Exception as e:
        print(f"❌ Failed to set default Rich Menu: {e}")
        return

    print(f"\n🎉 Rich Menu is now LIVE on your LINE Official Account!")

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
    setup_rich_menu(token)
