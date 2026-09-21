import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

payload = {
    'name': 'เจ้าชะตา',
    'birthDate': '1995-05-15',
    'birthTime': '09:30',
    'province': 'กรุงเทพมหานคร',
    'district': 'พระนคร',
    'calcMethod': 'suriyayatra',
    'targetDate': '2026-09-21'
}

req = urllib.request.Request(
    'http://localhost:5173/api/astrology/daily',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

resp = urllib.request.urlopen(req)
res = json.loads(resp.read().decode('utf-8'))
asc = res['data']['natalChart']['ascendant']
print(f"✓ ผลลัพธ์: ลัคนาราศี{asc['signName']} ({asc['signDegree']}° {asc['arcMinutes']}') | วิธี: {asc['method']} | เวลา LMT: {asc['lmtTime']} น.")
