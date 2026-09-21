#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(base_dir)
root_dir = os.path.dirname(api_dir)
for p in [base_dir, api_dir, root_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from thai_astrology import get_horoscope
except ImportError:
    from api.thai_astrology import get_horoscope

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
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'endpoint': '/api/astrology/daily'}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        try:
            payload = json.loads(body_bytes.decode('utf-8'))
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
