#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import json

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
        
        # Test connectivity
        upstash_ok = False
        upstash_err = ""
        try:
            url = 'https://knowing-anchovy-295305.upstash.io'
            req = urllib.request.Request(url, headers={'User-Agent': 'Vercel-Test'})
            with urllib.request.urlopen(req, timeout=3) as r:
                upstash_ok = (r.status in (200, 401, 400))
        except Exception as e:
            upstash_err = str(e)

        resp = {
            'status': 'ok',
            'service': 'PLB Thai Horoscope API',
            'version': '3.1',
            'upstash_reachable': upstash_ok,
            'upstash_error': upstash_err
        }
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))

