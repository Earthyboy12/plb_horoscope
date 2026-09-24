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
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "Thai Horoscope App"}).encode("utf-8"))
            return
        elif parsed.path == "/api/astrology/provinces":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            provinces_list = [{"name": k, "lat": v["lat"], "lng": v["lng"]} for k, v in PROVINCES_DICT.items()]
            self.wfile.write(json.dumps({"success": True, "data": provinces_list}).encode("utf-8"))
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
                payload["server_received_at"] = datetime.datetime.now().isoformat()
                
                # Save locally to feedback.jsonl
                feedback_file = os.path.join(BASE_DIR, "feedback.jsonl")
                with open(feedback_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(payload, ensure_ascii=False) + "\n")
                
                # Forward to webhook if configured
                webhook_url = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL") or os.environ.get("FEEDBACK_WEBHOOK_URL")
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
