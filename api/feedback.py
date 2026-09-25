#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import datetime

class handler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "PLB Feedback Endpoint"}, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            payload = json.loads(body.decode('utf-8')) if body else {}
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
            
            # Forward to Google Sheets Webhook
            DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwBA-NdVNPQSC_M-a_dMWinkH1-5zSADD0xxkXJkE42TYIa-fvQNGMrVoq2Yu5zJ1_-6A/exec"
            webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or os.environ.get("FEEDBACK_WEBHOOK_URL") or DEFAULT_WEBHOOK_URL
            webhook_status = "not_configured"
            if webhook_url:
                try:
                    req_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
                    req = urllib.request.Request(
                        webhook_url,
                        data=req_data,
                        headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'PLB-Astrology-App'}
                    )
                    with urllib.request.urlopen(req, timeout=6) as response:
                        webhook_status = f"forwarded_{response.getcode()}"
                except Exception as we:
                    webhook_status = f"error_{str(we)}"

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "บันทึกผลการประเมินเรียบร้อยแล้ว ขอบคุณครับ",
                "webhook_status": webhook_status
            }, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "error": str(e)
            }, ensure_ascii=False).encode('utf-8'))
