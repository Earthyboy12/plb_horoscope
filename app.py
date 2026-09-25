#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thai Daily Horoscope Standalone Server
Zero dependencies - uses only Python standard library.
"""
import http.server
import socketserver
import json
import urllib.parse
import urllib.request
import os
import sys
import webbrowser
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from thai_astrology import get_horoscope, PROVINCES_DICT
from user_store import get_user, save_user, update_transit_location, record_user_check
from line_bot_engine import (
    verify_signature,
    handle_line_event,
    send_noon_reminder_broadcast,
    push_line_message,
    compute_user_horoscope,
    get_channel_access_token
)
from line_flex_builder import build_daily_summary_flex

PORT = 5173
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

class HoroscopeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.path = "/index.html"
            return super().do_GET()
        elif parsed.path == "/liff-register.html" or parsed.path == "/liff":
            self.path = "/liff-register.html"
            return super().do_GET()
        elif parsed.path in ("/api/cron/noon-reminder", "/cron/noon-reminder"):
            try:
                channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or get_channel_access_token()
                web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
                res = send_noon_reminder_broadcast(web_url, channel_access_token)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "action": "noon_reminder_cron",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "result": res
                }, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "Thai Horoscope App"}).encode("utf-8"))
            return
        elif parsed.path == "/api/astrology/provinces":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            provinces_list = [{"name": k, "lat": v["lat"], "lng": v["lng"]} for k, v in PROVINCES_DICT.items()]
            self.wfile.write(json.dumps({"success": True, "data": provinces_list}).encode("utf-8"))
            return
        elif parsed.path == "/api/line/user":
            query = urllib.parse.parse_qs(parsed.query)
            user_id = query.get("userId", [""])[0]
            user_data = get_user(user_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": user_data}, ensure_ascii=False).encode("utf-8"))
            return
        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/astrology/daily":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                payload = json.loads(body_bytes.decode("utf-8"))
                target_date = payload.get("targetDate", "")
                result = get_horoscope(payload, target_date)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "data": result}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return
        elif parsed.path == "/api/feedback":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
                now_iso = datetime.datetime.now().isoformat()
                if "submittedAt" not in payload:
                    payload["submittedAt"] = now_iso
                payload["server_received_at"] = now_iso

                # Normalize keys for unified format
                if "userName" not in payload and "name" in payload:
                    payload["userName"] = payload["name"]
                if "name" not in payload and "userName" in payload:
                    payload["name"] = payload["userName"]
                if "transitProvince" not in payload and "transit_province" in payload:
                    payload["transitProvince"] = payload["transit_province"]
                if "transit_province" not in payload and "transitProvince" in payload:
                    payload["transit_province"] = payload["transitProvince"]
                if "created_at" not in payload and "submittedAt" in payload:
                    payload["created_at"] = payload["submittedAt"]
                if "channel" not in payload:
                    payload["channel"] = "web"
                
                # Save locally to feedback.jsonl
                feedback_file = os.path.join(BASE_DIR, "feedback.jsonl")
                with open(feedback_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(payload, ensure_ascii=False) + "\n")
                
                # Forward to webhook
                DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"
                webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or os.environ.get("FEEDBACK_WEBHOOK_URL") or DEFAULT_WEBHOOK_URL
                if webhook_url:
                    try:
                        req = urllib.request.Request(
                            webhook_url,
                            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-Astrology-App"}
                        )
                        urllib.request.urlopen(req, timeout=5)
                    except Exception as we:
                        print(f"Webhook forward warning: {we}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "message": "Feedback recorded successfully"}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return
        elif parsed.path == "/api/line/webhook":
            signature = self.headers.get("X-Line-Signature", "")
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            channel_secret = os.environ.get("LINE_CHANNEL_SECRET", "")
            channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
            liff_id = os.environ.get("LIFF_ID", "")
            web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")

            if channel_secret and not verify_signature(body_bytes, signature, channel_secret):
                self.send_response(403)
                self.end_headers()
                return

            try:
                payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
                events = payload.get("events", [])
                for ev in events:
                    handle_line_event(ev, channel_access_token, liff_id, web_url)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                print(f"Error handling LINE webhook: {e}")
                self.send_response(500)
                self.end_headers()
            return
        elif parsed.path == "/api/line/register":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
                action = payload.get("action", "register_natal")
                user_id = payload.get("line_user_id", "")

                if action == "update_transit":
                    prov = payload.get("transit_province") or payload.get("transitProvince", "กรุงเทพมหานคร")
                    dist = payload.get("transit_district") or payload.get("transitDistrict", "")
                    user = update_transit_location(user_id, prov, dist)
                else:
                    user = save_user(user_id, payload)

                # Push celebration or updated summary to LINE chat if valid LINE user ID
                channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or get_channel_access_token()
                liff_id = os.environ.get("LIFF_ID", "")
                web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
                if channel_access_token and user_id.startswith("U"):
                    try:
                        horoscope = compute_user_horoscope(user)
                        record_user_check(user_id, horoscope.get("overallScore", 80))
                        summary_flex = build_daily_summary_flex(
                            user, horoscope,
                            f"https://liff.line.me/{liff_id}?userId={user_id}" if liff_id else f"{web_url}/liff-register.html?userId={user_id}",
                            web_url
                        )
                        if action == "update_transit":
                            msg_text = (
                                f"📍 อัปเดตสถานที่จรสำเร็จเรียบร้อยแล้วครับ!\n"
                                f"🧭 จังหวัดจรปัจจุบัน: {user.get('transit_province')}\n"
                                f"🗺️ เขต/อำเภอ: {user.get('transit_district')}\n\n"
                                f"แม่หมอได้คำนวณรุ่งอรุณและกระแสดาวจรตามพิกัดใหม่ให้คุณเรียบร้อยแล้วครับ ✨"
                            )
                        else:
                            msg_text = (
                                f"✅ ระบบบันทึกข้อมูลดวงชะตาของคุณเรียบร้อยแล้วครับ!\n\n"
                                f"👤 ชื่อ: {user.get('name', 'ผู้ใช้')}\n"
                                f"📅 วันเกิด: {user.get('birth_date')}\n"
                                f"⏰ เวลาเกิด: {user.get('birth_time')} น.\n"
                                f"📍 จังหวัดเกิด: {user.get('birth_province')}\n"
                                f"🧭 สถานที่จร: {user.get('transit_province')}\n\n"
                                f"แม่หมอผูกดวงและคำนวณลัคนาราศีให้เรียบร้อยแล้ว นี่คือสรุปดวงประจำวันของคุณครับ 👇✨"
                            )
                        push_line_message(user_id, [{"type": "text", "text": msg_text}, summary_flex], channel_access_token)
                    except Exception as pe:
                        print(f"Push to LINE warning: {pe}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "data": user}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HoroscopeHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🔮 =====================================================")
        print(f"   Thai Daily Horoscope App is running!")
        print(f"   URL: {url}")
        print(f"   เปิดเว็บแอปพลิเคชันดูดวงรายวันลัคนาราศีและดวงจร")
        print(f"=====================================================")
        sys.stdout.flush()
        
        # Automatically open default browser
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
