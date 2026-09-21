#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
for p in [base_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from thai_astrology import get_horoscope, PROVINCES_DICT
except ImportError:
    from .thai_astrology import get_horoscope, PROVINCES_DICT

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
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.lower()
        if 'health' in path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            resp = {'status': 'ok', 'service': 'PLB Thai Horoscope API', 'version': '2.0'}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return
        if 'provinces' in path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            provinces_list = [{'name': k, 'lat': v['lat'], 'lng': v['lng']} for k, v in PROVINCES_DICT.items()]
            resp = {'success': True, 'data': provinces_list}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return
        self.send_response(404)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.lower()
        if 'daily' in path or 'astrology' in path:
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
            return
        self.send_response(404)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))
