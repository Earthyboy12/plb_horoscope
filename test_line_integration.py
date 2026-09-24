#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test LINE Bot and Astrology Engine Integration"""
import json
import datetime
from user_store import save_user, get_user, update_transit_location
from line_bot_engine import compute_user_horoscope, verify_signature
from line_flex_builder import (
    build_welcome_flex,
    build_daily_summary_flex,
    build_category_flex,
    build_feedback_flex,
    build_donation_flex
)

def test_all():
    print("1. Testing User Store...")
    mock_uid = "U1234567890abcdef"
    user = save_user(mock_uid, {
        "name": "ทดสอบระบบ",
        "birth_date": "1995-08-12",
        "birth_time": "08:30",
        "birth_province": "กรุงเทพมหานคร",
        "birth_district": "พระนคร",
        "calc_method": "suriyayatra",
        "transit_province": "กรุงเทพมหานคร",
        "transit_district": "พระนคร"
    })
    assert user["name"] == "ทดสอบระบบ"
    fetched = get_user(mock_uid)
    assert fetched["line_user_id"] == mock_uid
    print("   User Store: PASS")

    print("2. Testing Astrological Calculation for LINE User...")
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    horoscope = compute_user_horoscope(fetched, today_str)
    assert "natalChart" in horoscope
    assert "transitLocation" in horoscope
    assert "categories" in horoscope
    asc_name = horoscope["natalChart"]["ascendant"]["signName"]
    print(f"   Lagna calculated: {asc_name}")
    print(f"   Daily score: {horoscope['categories']['overall']['score']}%")
    print("   Astrology Calculation: PASS")

    print("3. Testing Changing Transit Location...")
    user_updated = update_transit_location(mock_uid, "เชียงใหม่", "อำเภอเมืองเชียงใหม่")
    assert user_updated["transit_province"] == "เชียงใหม่"
    horoscope_cm = compute_user_horoscope(user_updated, today_str)
    assert horoscope_cm["transitLocation"]["province"] == "เชียงใหม่"
    print(f"   Sunrise at Chiang Mai: {horoscope_cm['transitLocation']['sunriseTime']}")
    print("   Transit Location Switcher: PASS")

    print("4. Testing Flex Message Builders...")
    w_flex = build_welcome_flex("https://liff.line.me/test-liff")
    assert w_flex["type"] == "flex"
    
    s_flex = build_daily_summary_flex(user_updated, horoscope_cm)
    assert s_flex["type"] == "flex"
    
    cat_flex = build_category_flex("career", horoscope_cm["categories"]["career"], asc_name, today_str)
    assert cat_flex["type"] == "flex"
    
    fb_flex = build_feedback_flex()
    assert fb_flex["type"] == "flex"
    
    dn_flex = build_donation_flex("081-234-5678", "พร้อมเพย์ Earth PLB")
    assert dn_flex["type"] == "flex"
    print("   Flex Message Builders: PASS (All JSON valid)")

    print("5. Testing Signature Verification...")
    valid = verify_signature(b'{"events":[]}', "", "")
    assert valid is True
    print("   Signature Verification: PASS")

    print("6. Testing Gamification & Streak History...")
    from user_store import record_user_check, get_rank_title
    user_with_check = record_user_check(mock_uid, 85)
    assert user_with_check["check_count"] >= 1
    assert "streak" in user_with_check
    rank = get_rank_title(user_with_check["check_count"], user_with_check["streak"])
    assert "title" in rank and "badge" in rank
    print(f"   Rank: {rank['title']} ({rank['badge']})")
    print(f"   Checks: {user_with_check['check_count']}, Streak: {user_with_check['streak']}")
    print("   Gamification & Streak: PASS")

    print("7. Testing Personal Astro Stats & 7-Day Luck Wave Flex Card...")
    from line_flex_builder import build_stats_flex
    stats_flex = build_stats_flex(user_with_check, horoscope_cm)
    assert stats_flex["type"] == "flex"
    assert "สถิติดวงชะตา" in stats_flex["altText"]
    assert stats_flex["contents"]["type"] == "bubble"
    print("   Personal Astro Stats Flex Card: PASS (Valid Flex JSON)")

    print("8. Testing Chat Natural Language Birth Parser...")
    from line_bot_engine import parse_birth_info_from_text
    parsed1 = parse_birth_info_from_text("เกิด 12/08/2538 08:30 กรุงเทพมหานคร")
    assert parsed1 is not None
    assert parsed1["birth_date"] == "1995-08-12"
    assert parsed1["birth_time"] == "08:30"
    assert parsed1["birth_province"] == "กรุงเทพมหานคร"

    parsed2 = parse_birth_info_from_text("เกิด 1995-08-12 09.15 เชียงใหม่")
    assert parsed2 is not None
    assert parsed2["birth_province"] == "เชียงใหม่"

    parsed3 = parse_birth_info_from_text("สวัสดีครับ วันนี้ดวงเป็นไงบ้าง")
    assert parsed3 is None
    print("   Chat Birth Parser: PASS")

    print("\n🎉 ALL 8 TESTS PASSED SUCCESSFULLY! 🔮")

if __name__ == "__main__":
    test_all()
