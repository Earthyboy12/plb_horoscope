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
    from thai_astrology import PROVINCES_DICT
except ImportError:
    from api.thai_astrology import PROVINCES_DICT

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
        provinces_list = [{'name': k, 'lat': v['lat'], 'lng': v['lng']} for k, v in PROVINCES_DICT.items()]
        resp = {'success': True, 'data': provinces_list}
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
