import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from thai_astrology import date_to_julian_day, calculate_planets, ZODIAC_SIGNS

def calc_antona_ascendant(year, month, day, hour, minute, lng=100.5):
    lmt_offset = (105.0 - lng) * 4.0
    total_min = hour * 60 + minute - lmt_offset
    if total_min < 0:
        total_min += 1440
    
    jd = date_to_julian_day(year, month, day, 6 - 7, 0)
    planets = calculate_planets(jd)
    sun = next(p for p in planets if p['id'] == 1)
    
    sun_sign = sun['signId']
    sun_deg = sun['signDegree'] + sun['arcMinutes'] / 60.0
    
    antona_ti = [120, 96, 72, 120, 144, 168, 168, 144, 120, 72, 96, 120]
    elapsed = (total_min - 360) % 1440
    
    time_rem_sun = ((30.0 - sun_deg) / 30.0) * antona_ti[sun_sign]
    
    if elapsed < time_rem_sun:
        asc_sign = sun_sign
        asc_deg = sun_deg + (elapsed / antona_ti[sun_sign]) * 30.0
    else:
        elapsed -= time_rem_sun
        curr_sign = (sun_sign + 1) % 12
        while elapsed >= antona_ti[curr_sign]:
            elapsed -= antona_ti[curr_sign]
            curr_sign = (curr_sign + 1) % 12
        asc_sign = curr_sign
        asc_deg = (elapsed / antona_ti[curr_sign]) * 30.0
        
    s_name = ZODIAC_SIGNS[sun_sign]["thaiName"]
    a_name = ZODIAC_SIGNS[asc_sign]["thaiName"]
    lmt_h = int(total_min // 60)
    lmt_m = int(total_min % 60)
    print(f"Sun: ราศี{s_name} {sun_deg:.2f}° | LMT: {lmt_h:02d}:{lmt_m:02d} (-{lmt_offset:.1f}m) | Ascendant: ราศี{a_name} {asc_deg:.2f}°")
    return asc_sign, a_name

# Test
calc_antona_ascendant(1995, 5, 15, 9, 30, 100.5)
