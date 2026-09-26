#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
import os
import sys
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
for p in [base_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from thai_astrology import get_horoscope, compute_28day_forecast, compute_synastry, compute_wedding_muhurta, PROVINCES_DICT
    from user_store import get_user, save_user, update_transit_location, record_user_check
    from line_bot_engine import (
        verify_signature,
        handle_line_event,
        send_morning_reminder_broadcast,
        send_noon_reminder_broadcast,
        push_line_message,
        compute_user_horoscope,
        get_channel_access_token
    )
    from line_flex_builder import build_daily_summary_flex
except ImportError:
    from api.thai_astrology import get_horoscope, compute_28day_forecast, compute_synastry, compute_wedding_muhurta, PROVINCES_DICT
    from api.user_store import get_user, save_user, update_transit_location, record_user_check
    from api.line_bot_engine import (
        verify_signature,
        handle_line_event,
        send_morning_reminder_broadcast,
        send_noon_reminder_broadcast,
        push_line_message,
        compute_user_horoscope,
        get_channel_access_token
    )
    from api.line_flex_builder import build_daily_summary_flex

class handler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Line-Signature')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        matched = self.headers.get('x-matched-path', '')
        forwarded = self.headers.get('x-forwarded-uri', '')
        check_str = f"{self.path} {matched} {forwarded}".lower()

        if 'line/user' in check_str or 'user' in check_str:
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            user_id = query.get("userId", [""])[0]
            user_data = get_user(user_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'data': user_data}, ensure_ascii=False).encode('utf-8'))
            return

        if 'province' in check_str:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            provinces_list = [{'name': k, 'lat': v['lat'], 'lng': v['lng']} for k, v in PROVINCES_DICT.items()]
            resp = {'success': True, 'data': provinces_list}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        if 'morning-reminder' in check_str or 'cron/morning' in check_str or 'noon-reminder' in check_str or 'cron/noon' in check_str:
            try:
                parsed_url = urllib.parse.urlparse(self.path)
                qs = urllib.parse.parse_qs(parsed_url.query)
                is_force = qs.get("force", ["false"])[0].lower() in ("true", "1")
                channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or get_channel_access_token()
                web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
                if 'morning' in check_str:
                    res = send_morning_reminder_broadcast(web_url, channel_access_token, force=is_force)
                    act_name = "morning_reminder_cron"
                else:
                    res = send_noon_reminder_broadcast(web_url, channel_access_token, force=is_force)
                    act_name = "noon_reminder_cron"
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "action": act_name,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "result": res
                }, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # Default GET response is Health Check
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        resp = {
            'status': 'ok',
            'service': 'PLB Thai Horoscope API & LINE OA Engine',
            'version': '3.2',
            'path': self.path
        }
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))


    def do_POST(self):
        matched = self.headers.get('x-matched-path', '')
        forwarded = self.headers.get('x-forwarded-uri', '')
        check_str = f"{self.path} {matched} {forwarded}".lower()
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        payload = {}
        if body_bytes:
            try:
                payload = json.loads(body_bytes.decode('utf-8'))
            except Exception:
                payload = {}

        # 1. LINE Webhook
        if 'line/webhook' in check_str or 'x-line-signature' in self.headers or ('events' in payload and 'destination' in payload):
            signature = self.headers.get("X-Line-Signature", "")
            channel_secret = os.environ.get("LINE_CHANNEL_SECRET", "")
            channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
            liff_id = os.environ.get("LIFF_ID", "")
            web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")

            if channel_secret and not verify_signature(body_bytes, signature, channel_secret):
                self.send_response(403)
                self.end_headers()
                return

            try:
                events = payload.get("events", [])
                for ev in events:
                    handle_line_event(ev, channel_access_token, liff_id, web_url)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                import traceback
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e), "trace": traceback.format_exc()}).encode('utf-8'))
            return

        # 2. LIFF Registration / Transit Location
        if ('line/register' in check_str or payload.get("action") in ("register_natal", "update_transit")) and ('daily' not in check_str and 'synastry' not in check_str and 'wedding' not in check_str):
            try:
                action = payload.get("action", "register_natal")
                user_id = payload.get("line_user_id", "")

                if action == "update_transit":
                    prov = payload.get("transit_province") or payload.get("transitProvince", "กรุงเทพมหานคร")
                    dist = payload.get("transit_district") or payload.get("transitDistrict", "")
                    user = update_transit_location(user_id, prov, dist)
                else:
                    user = save_user(user_id, payload)

                channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or get_channel_access_token()
                liff_id = os.environ.get("LIFF_ID", "")
                web_url = os.environ.get("APP_URL", "https://plb-horoscope.vercel.app")
                if channel_access_token and user_id.startswith("U"):
                    try:
                        horoscope = compute_user_horoscope(user)
                        user = record_user_check(user_id, horoscope.get("overallScore", 80)) or get_user(user_id) or user
                        try:
                            from line_flex_builder import make_liff_url
                        except ImportError:
                            from api.line_flex_builder import make_liff_url
                        liff_target = f"https://liff.line.me/{liff_id}" if liff_id else f"{web_url}/liff-register.html"
                        summary_flex = build_daily_summary_flex(
                            user, horoscope,
                            make_liff_url(liff_target, user),
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
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': user}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # 3. Feedback Submission
        if 'feedback' in check_str:
            try:
                payload = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
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
                DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"
                webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or os.environ.get("FEEDBACK_WEBHOOK_URL") or DEFAULT_WEBHOOK_URL
                if webhook_url:
                    try:
                        req = urllib.request.Request(
                            webhook_url,
                            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PLB-Astrology-App"}
                        )
                        urllib.request.urlopen(req, timeout=5)
                    except Exception as we:
                        print(f"Webhook forward warning: {we}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'Feedback recorded'}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # 4. Monthly 28-day Forecast endpoint
        if 'monthly' in check_str or payload.get("action") in ("compute_28day", "monthly_forecast"):
            try:
                target_date = payload.get('targetDate', '')
                forecast_28 = compute_28day_forecast(payload, target_date)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': forecast_28}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # 5. Astrological Compatibility / Synastry endpoint
        if 'synastry' in check_str or 'compatibility' in check_str or payload.get("action") in ("compute_synastry", "synastry_check", "compatibility"):
            try:
                person1 = payload.get("person1", {})
                person2 = payload.get("person2", {})
                rel_type = payload.get("relationshipType", "love")
                synastry_res = compute_synastry(person1, person2, rel_type)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': synastry_res}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # 6. Wedding Muhurta endpoint
        if 'wedding' in check_str or 'muhurta' in check_str or payload.get("action") in ("compute_wedding", "wedding_muhurta"):
            try:
                person1 = payload.get("person1", {})
                person2 = payload.get("person2", {})
                days_ahead = int(payload.get("daysAhead", 365))
                top_n = int(payload.get("topN", 5))
                wedding_res = compute_wedding_muhurta(person1, person2, days_ahead, top_n)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': wedding_res}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        # 7. Standard Daily Astrology Calculation
        try:
            payload = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
            target_date = payload.get('targetDate', '')
            result = get_horoscope(payload, target_date)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            resp = {'success': True, 'data': result}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            resp = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
