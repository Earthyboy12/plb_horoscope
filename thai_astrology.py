# Thai Astrology Core Calculation Engine in Python (Pure Standard Library - Zero Dependencies)
import math
import datetime
from detailed_forecast import synthesize_detailed_categories, synthesize_detailed_lucky

DEG2RAD = math.pi / 180.0
RAD2DEG = 180.0 / math.pi

def sin_d(deg):
    return math.sin(deg * DEG2RAD)

def cos_d(deg):
    return math.cos(deg * DEG2RAD)

def normalize_degrees(deg):
    d = deg % 360.0
    if d < 0:
        d += 360.0
    return d

def date_to_julian_day(year, month, day, hour=0, minute=0, second=0):
    d = day + (hour + minute / 60.0 + second / 3600.0) / 24.0
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + d + B - 1524.5

def get_lahiri_ayanamsa(jd):
    T = (jd - 2451545.0) / 36525.0
    return 23.857092 + 1.396042 * T - 0.000308 * T * T

def degree_to_sign_detail(deg):
    normalized = normalize_degrees(deg)
    sign_id = int(normalized // 30)
    sign_deg_float = normalized - sign_id * 30.0
    sign_deg = int(sign_deg_float)
    arc_min = int((sign_deg_float - sign_deg) * 60.0)
    return {
        "signId": sign_id,
        "signDegree": sign_deg,
        "arcMinutes": arc_min,
        "totalDegree": normalized
    }

ZODIAC_SIGNS = {
    0: {"id": 0, "thaiName": "เมษ", "engName": "Aries", "symbol": "♈", "rulerPlanet": 3, "element": "ไฟ"},
    1: {"id": 1, "thaiName": "พฤษภ", "engName": "Taurus", "symbol": "♉", "rulerPlanet": 6, "element": "ดิน"},
    2: {"id": 2, "thaiName": "เมถุน", "engName": "Gemini", "symbol": "♊", "rulerPlanet": 4, "element": "ลม"},
    3: {"id": 3, "thaiName": "กรกฎ", "engName": "Cancer", "symbol": "♋", "rulerPlanet": 2, "element": "น้ำ"},
    4: {"id": 4, "thaiName": "สิงห์", "engName": "Leo", "symbol": "♌", "rulerPlanet": 1, "element": "ไฟ"},
    5: {"id": 5, "thaiName": "กันย์", "engName": "Virgo", "symbol": "♍", "rulerPlanet": 4, "element": "ดิน"},
    6: {"id": 6, "thaiName": "ตุลย์", "engName": "Libra", "symbol": "♎", "rulerPlanet": 6, "element": "ลม"},
    7: {"id": 7, "thaiName": "พิจิก", "engName": "Scorpio", "symbol": "♏", "rulerPlanet": 3, "element": "น้ำ"},
    8: {"id": 8, "thaiName": "ธนู", "engName": "Sagittarius", "symbol": "♐", "rulerPlanet": 5, "element": "ไฟ"},
    9: {"id": 9, "thaiName": "มังกร", "engName": "Capricorn", "symbol": "♑", "rulerPlanet": 7, "element": "ดิน"},
    10: {"id": 10, "thaiName": "กุมภ์", "engName": "Aquarius", "symbol": "♒", "rulerPlanet": 8, "element": "ลม"},
    11: {"id": 11, "thaiName": "มีน", "engName": "Pisces", "symbol": "♓", "rulerPlanet": 5, "element": "น้ำ"},
}

PLANETS_META = {
    1: {"id": 1, "symbol": "๑", "name": "อาทิตย์", "keyword": "ยศศักดิ์ เกียรติยศ ผู้นำ"},
    2: {"id": 2, "symbol": "๒", "name": "จันทร์", "keyword": "เสน่ห์ อารมณ์ ความอ่อนโยน จิตใจ"},
    3: {"id": 3, "symbol": "๓", "name": "อังคาร", "keyword": "กล้าหาญ ขยันขันแข็ง การแข่งขัน"},
    4: {"id": 4, "symbol": "๔", "name": "พุธ", "keyword": "เจรจา ไหวพริบ ค้าขาย การสื่อสาร"},
    5: {"id": 5, "symbol": "๕", "name": "พฤหัสบดี", "keyword": "ปัญญา คุณธรรม ผู้ใหญ่ช่วยเหลือ โชคลาภ"},
    6: {"id": 6, "symbol": "๖", "name": "ศุกร์", "keyword": "การเงิน ความรัก โภคทรัพย์ ความสุข"},
    7: {"id": 7, "symbol": "๗", "name": "เสาร์", "keyword": "ความอดทน ภาระหน้าที่ สิ่งเก่าแก่"},
    8: {"id": 8, "symbol": "๘", "name": "ราหู", "keyword": "ลุ่มหลง เสี่ยงโชค ต่างแดน พลิกแพลง"},
    9: {"id": 9, "symbol": "๙", "name": "เกตุ", "keyword": "สิ่งศักดิ์สิทธิ์ ลางสังหรณ์ โชคประหลาด"},
    0: {"id": 0, "symbol": "๐", "name": "มฤตยู", "keyword": "การเปลี่ยนแปลงฉับพลัน นวัตกรรม เทคโนโลยี"}
}

BHAVAS_LIST = [
    {"id": 1, "name": "ตนุ", "meaning": "ตัวตน จิตใจ ร่างกาย สุขภาพโดยรวม"},
    {"id": 2, "name": "กดุมภะ", "meaning": "ทรัพย์สิน เงินทอง รายได้ สภาพคล่อง"},
    {"id": 3, "name": "สหัชชะ", "meaning": "เพื่อนฝูง สังคม การติดต่อสื่อสาร การเดินทางใกล้"},
    {"id": 4, "name": "พันธุ", "meaning": "ครอบครัว บ้าน ยานพาหนะ ความมั่นคง"},
    {"id": 5, "name": "ปุตตะ", "meaning": "บริวาร ลูกน้อง โครงการใหม่ โชคเสี่ยง"},
    {"id": 6, "name": "อริ", "meaning": "อุปสรรค ปัญหา หนี้สิน ศัตรู โรคภัย"},
    {"id": 7, "name": "ปัตนิ", "meaning": "คู่ครอง หุ้นส่วน คู่ค้า คนรัก"},
    {"id": 8, "name": "มรณะ", "meaning": "การเปลี่ยนแปลง การสูญเสีย มรดก สิ่งเร้นลับ"},
    {"id": 9, "name": "ศุภะ", "meaning": "ความเจริญก้าวหน้า ความสำเร็จ ผู้ใหญ่อุปถัมภ์"},
    {"id": 10, "name": "กัมมะ", "meaning": "การงาน อาชีพ หน้าที่ความรับผิดชอบ"},
    {"id": 11, "name": "ลาภะ", "meaning": "โชคลาภ ผลประโยชน์ ความสำเร็จ มิตรภาพ"},
    {"id": 12, "name": "วินาศ", "meaning": "ความลับ ความสูญเสียที่ไม่คาดคิด ปลีกวิเวก"}
]

# อันโตนาทีสามัญตามคัมภีร์สุริยยาตร์ (หน่วยเป็นนาทีสากล รวม 1,440 นาที = 24 ชม.)
ANTONA_TI_SAMANYA = [
    120, # 0 เมษ
    96,  # 1 พฤษภ
    72,  # 2 เมถุน
    120, # 3 กรกฎ
    144, # 4 สิงห์
    168, # 5 กันย์
    168, # 6 ตุลย์
    144, # 7 พิจิก
    120, # 8 ธนู
    72,  # 9 มังกร
    96,  # 10 กุมภ์
    120  # 11 มีน
]

# Database of Bangkok Districts (50 เขต) with exact coordinates for Local Mean Time (LMT) calculation
BANGKOK_DISTRICTS = {
    "พระนคร": {"lat": 13.7644, "lng": 100.4990},
    "ดุสิต": {"lat": 13.7769, "lng": 100.5209},
    "หนองจอก": {"lat": 13.8557, "lng": 100.8655},
    "บางรัก": {"lat": 13.7307, "lng": 100.5238},
    "บางเขน": {"lat": 13.8741, "lng": 100.5983},
    "บางกะปิ": {"lat": 13.7658, "lng": 100.6439},
    "ปทุมวัน": {"lat": 13.7444, "lng": 100.5319},
    "ป้อมปราบศัตรูพ่าย": {"lat": 13.7581, "lng": 100.5108},
    "พระโขนง": {"lat": 13.7022, "lng": 100.6033},
    "มีนบุรี": {"lat": 13.8139, "lng": 100.7483},
    "ลาดกระบัง": {"lat": 13.7239, "lng": 100.7819},
    "ยานนาวา": {"lat": 13.6972, "lng": 100.5336},
    "สัมพันธวงศ์": {"lat": 13.7381, "lng": 100.5097},
    "พญาไท": {"lat": 13.7803, "lng": 100.5408},
    "ธนบุรี": {"lat": 13.7258, "lng": 100.4858},
    "บางกอกใหญ่": {"lat": 13.7228, "lng": 100.4744},
    "ห้วยขวาง": {"lat": 13.7781, "lng": 100.5786},
    "คลองสาน": {"lat": 13.7303, "lng": 100.5069},
    "ตลิ่งชัน": {"lat": 13.7769, "lng": 100.4497},
    "บางกอกน้อย": {"lat": 13.7608, "lng": 100.4728},
    "บางขุนเทียน": {"lat": 13.6261, "lng": 100.4350},
    "ภาษีเจริญ": {"lat": 13.7144, "lng": 100.4336},
    "หนองแขม": {"lat": 13.7058, "lng": 100.3547},
    "ราษฎร์บูรณะ": {"lat": 13.6819, "lng": 100.5019},
    "บางพลัด": {"lat": 13.7928, "lng": 100.4972},
    "ดินแดง": {"lat": 13.7697, "lng": 100.5603},
    "บึงกุ่ม": {"lat": 13.7853, "lng": 100.6653},
    "สาทร": {"lat": 13.7214, "lng": 100.5261},
    "บางซื่อ": {"lat": 13.8097, "lng": 100.5303},
    "จตุจักร": {"lat": 13.8286, "lng": 100.5600},
    "บางคอแหลม": {"lat": 13.6933, "lng": 100.5025},
    "ประเวศ": {"lat": 13.7169, "lng": 100.6978},
    "คลองเตย": {"lat": 13.7081, "lng": 100.5844},
    "สวนหลวง": {"lat": 13.7306, "lng": 100.6447},
    "จอมทอง": {"lat": 13.6775, "lng": 100.4572},
    "ดอนเมือง": {"lat": 13.9133, "lng": 100.5919},
    "ราชเทวี": {"lat": 13.7589, "lng": 100.5347},
    "ลาดพร้าว": {"lat": 13.8036, "lng": 100.6056},
    "วัฒนา": {"lat": 13.7381, "lng": 100.5853},
    "บางแค": {"lat": 13.6922, "lng": 100.3956},
    "หลักสี่": {"lat": 13.8875, "lng": 100.5756},
    "สายไหม": {"lat": 13.9189, "lng": 100.6458},
    "คันนายาว": {"lat": 13.8267, "lng": 100.6861},
    "สะพานสูง": {"lat": 13.7700, "lng": 100.6828},
    "วังทองหลาง": {"lat": 13.7856, "lng": 100.6075},
    "คลองสามวา": {"lat": 13.8597, "lng": 100.7244},
    "บางนา": {"lat": 13.6681, "lng": 100.6053},
    "ทวีวัฒนา": {"lat": 13.7886, "lng": 100.3347},
    "ทุ่งครุ": {"lat": 13.6472, "lng": 100.5044},
    "บางบอน": {"lat": 13.6592, "lng": 100.3958}
}

PROVINCES_DICT = {
    "กรุงเทพมหานคร": {"lat": 13.7563, "lng": 100.5018, "districts": BANGKOK_DISTRICTS},
    "กระบี่": {"lat": 8.0863, "lng": 98.9063},
    "กาญจนบุรี": {"lat": 14.0228, "lng": 99.5328},
    "กาฬสินธุ์": {"lat": 16.4322, "lng": 103.5061},
    "กำแพงเพชร": {"lat": 16.4828, "lng": 99.5227},
    "ขอนแก่น": {"lat": 16.4419, "lng": 102.8359},
    "จันทบุรี": {"lat": 12.6114, "lng": 102.1039},
    "ฉะเชิงเทรา": {"lat": 13.6904, "lng": 101.0779},
    "ชลบุรี": {"lat": 13.3611, "lng": 100.9847},
    "ชัยนาท": {"lat": 15.1852, "lng": 100.1252},
    "ชัยภูมิ": {"lat": 15.8063, "lng": 102.0315},
    "ชุมพร": {"lat": 10.4930, "lng": 99.1800},
    "เชียงราย": {"lat": 19.9105, "lng": 99.8406},
    "เชียงใหม่": {"lat": 18.7883, "lng": 98.9853},
    "ตรัง": {"lat": 7.5563, "lng": 99.6114},
    "ตราด": {"lat": 12.2428, "lng": 102.5175},
    "ตาก": {"lat": 16.8839, "lng": 99.1258},
    "นครนายก": {"lat": 14.2069, "lng": 101.2131},
    "นครปฐม": {"lat": 13.8196, "lng": 100.0443},
    "นครพนม": {"lat": 17.3999, "lng": 104.7844},
    "นครราชสีมา": {"lat": 14.9799, "lng": 102.0978},
    "นครศรีธรรมราช": {"lat": 8.4304, "lng": 99.9631},
    "นครสวรรค์": {"lat": 15.6987, "lng": 100.1199},
    "นนทบุรี": {"lat": 13.8621, "lng": 100.5134},
    "นราธิวาส": {"lat": 6.4255, "lng": 101.8253},
    "น่าน": {"lat": 18.7831, "lng": 100.7782},
    "บึงกาฬ": {"lat": 18.3609, "lng": 103.6465},
    "บุรีรัมย์": {"lat": 14.9930, "lng": 103.1029},
    "ปทุมธานี": {"lat": 14.0208, "lng": 100.5250},
    "ประจวบคีรีขันธ์": {"lat": 11.8124, "lng": 99.7972},
    "ปราจีนบุรี": {"lat": 14.0509, "lng": 101.3734},
    "ปัตตานี": {"lat": 6.8696, "lng": 101.2501},
    "พระนครศรีอยุธยา": {"lat": 14.3532, "lng": 100.5684},
    "พะเยา": {"lat": 19.1664, "lng": 99.9022},
    "พังงา": {"lat": 8.4509, "lng": 98.5255},
    "พัทลุง": {"lat": 7.6167, "lng": 100.0740},
    "พิจิตร": {"lat": 16.4415, "lng": 100.3488},
    "พิษณุโลก": {"lat": 16.8211, "lng": 100.2659},
    "เพชรบุรี": {"lat": 13.1114, "lng": 99.9391},
    "เพชรบูรณ์": {"lat": 16.4190, "lng": 101.1567},
    "แพร่": {"lat": 18.1446, "lng": 100.1410},
    "ภูเก็ต": {"lat": 7.8804, "lng": 98.3923},
    "มหาสารคาม": {"lat": 16.1848, "lng": 103.3007},
    "มุกดาหาร": {"lat": 16.5436, "lng": 104.7235},
    "แม่ฮ่องสอน": {"lat": 19.3020, "lng": 97.9654},
    "ยโสธร": {"lat": 15.7926, "lng": 104.1453},
    "ยะลา": {"lat": 6.5411, "lng": 101.2813},
    "ร้อยเอ็ด": {"lat": 16.0538, "lng": 103.6520},
    "ระนอง": {"lat": 9.9658, "lng": 98.6348},
    "ระยอง": {"lat": 12.6814, "lng": 101.2816},
    "ราชบุรี": {"lat": 13.5283, "lng": 99.8134},
    "ลพบุรี": {"lat": 14.7995, "lng": 100.6534},
    "ลำปาง": {"lat": 18.2888, "lng": 99.4928},
    "ลำพูน": {"lat": 18.5744, "lng": 99.0087},
    "เลย": {"lat": 17.4860, "lng": 101.7223},
    "ศรีสะเกษ": {"lat": 15.1186, "lng": 104.3220},
    "สกลนคร": {"lat": 17.1546, "lng": 104.1486},
    "สงขลา": {"lat": 7.1898, "lng": 100.5954},
    "สตูล": {"lat": 6.6238, "lng": 100.0674},
    "สมุทรปราการ": {"lat": 13.5991, "lng": 100.5998},
    "สมุทรสงคราม": {"lat": 13.4098, "lng": 99.9968},
    "สมุทรสาคร": {"lat": 13.5475, "lng": 100.2744},
    "สระแก้ว": {"lat": 13.8140, "lng": 102.0726},
    "สระบุรี": {"lat": 14.5289, "lng": 100.9108},
    "สิงห์บุรี": {"lat": 14.8936, "lng": 100.4015},
    "สุโขทัย": {"lat": 17.0078, "lng": 99.8230},
    "สุพรรณบุรี": {"lat": 14.4745, "lng": 100.1177},
    "สุราษฎร์ธานี": {"lat": 9.1382, "lng": 99.3217},
    "สุรินทร์": {"lat": 14.8818, "lng": 103.4936},
    "หนองคาย": {"lat": 17.8783, "lng": 102.7420},
    "หนองบัวลำภู": {"lat": 17.2044, "lng": 102.4407},
    "อ่างทอง": {"lat": 14.5896, "lng": 100.4550},
    "อำนาจเจริญ": {"lat": 15.8585, "lng": 104.6258},
    "อุดรธานี": {"lat": 17.4157, "lng": 102.7859},
    "อุตรดิตถ์": {"lat": 17.6201, "lng": 100.0993},
    "อุทัยธานี": {"lat": 15.3835, "lng": 100.0245},
    "อุบลราชธานี": {"lat": 15.2448, "lng": 104.8473}
}

def solve_kepler(M_deg, e):
    M = normalize_degrees(M_deg) * DEG2RAD
    E = M
    for _ in range(15):
        delta = E - e * math.sin(E) - M
        if abs(delta) < 1e-7:
            break
        E -= delta / (1.0 - e * math.cos(E))
    return E

def get_planet_helio(a, e, I, L, w, node):
    M_deg = L - w
    E = solve_kepler(M_deg, e)
    x_prime = a * (math.cos(E) - e)
    y_prime = a * math.sqrt(1.0 - e * e) * math.sin(E)
    w_rad = (w - node) * DEG2RAD
    node_rad = node * DEG2RAD
    inc_rad = I * DEG2RAD

    x = (cos_d(node) * math.cos(w_rad) - sin_d(node) * math.sin(w_rad) * math.cos(inc_rad)) * x_prime \
      + (-cos_d(node) * math.sin(w_rad) - sin_d(node) * math.cos(w_rad) * math.cos(inc_rad)) * y_prime
    y = (sin_d(node) * math.cos(w_rad) + cos_d(node) * math.sin(w_rad) * math.cos(inc_rad)) * x_prime \
      + (-sin_d(node) * math.sin(w_rad) + cos_d(node) * math.cos(w_rad) * math.cos(inc_rad)) * y_prime
    z = (math.sin(w_rad) * math.sin(inc_rad)) * x_prime + (math.cos(w_rad) * math.sin(inc_rad)) * y_prime
    return x, y, z

def get_earth_helio(T):
    return get_planet_helio(1.00000261 + 0.00000562 * T, 0.01671123 - 0.00004392 * T, -0.00001531, 100.46457166 + 35999.37244981 * T, 102.93768193 + 0.32327364 * T, 0.0)

def get_geocentric_long(pH, eH):
    dx = pH[0] - eH[0]
    dy = pH[1] - eH[1]
    return normalize_degrees(math.atan2(dy, dx) * RAD2DEG)

def calculate_planets(jd):
    T = (jd - 2451545.0) / 36525.0
    ayanamsa = get_lahiri_ayanamsa(jd)
    eH = get_earth_helio(T)

    # Sun
    L0 = normalize_degrees(280.46646 + 36000.76983 * T)
    M = normalize_degrees(357.52911 + 35999.05029 * T)
    C = (1.914602 - 0.004817 * T) * sin_d(M) + 0.019993 * sin_d(2 * M)
    sun_trop = normalize_degrees(L0 + C)

    # Moon
    L_prime = normalize_degrees(218.3164477 + 481267.88123421 * T)
    D = normalize_degrees(297.8501921 + 445267.1114034 * T)
    M_prime = normalize_degrees(134.9633964 + 477198.8675055 * T)
    sumL = 6.288774 * sin_d(M_prime) + 1.274027 * sin_d(2 * D - M_prime) + 0.658314 * sin_d(2 * D)
    moon_trop = normalize_degrees(L_prime + sumL)

    # Planets
    merc_trop = get_geocentric_long(get_planet_helio(0.38709843, 0.20563661, 7.00559432, 252.25166724 + 149472.67486623 * T, 77.45771895, 48.33961819), eH)
    ven_trop = get_geocentric_long(get_planet_helio(0.72332102, 0.00676399, 3.39777545, 181.97970850 + 58517.81560260 * T, 131.76755713, 76.67261496), eH)
    mars_trop = get_geocentric_long(get_planet_helio(1.52371243, 0.09336511, 1.85181869, -4.56813164 + 19140.29934243 * T, -23.99172202, 49.71320984), eH)
    jup_trop = get_geocentric_long(get_planet_helio(5.20248019, 0.04853590, 1.29861416, 34.33479152 + 3034.90371757 * T, 14.27495244, 100.29282654), eH)
    sat_trop = get_geocentric_long(get_planet_helio(9.54149883, 0.05550825, 2.49424102, 50.07571329 + 1222.11494724 * T, 92.86136063, 113.63998702), eH)
    uranus_trop = get_geocentric_long(get_planet_helio(19.18916464, 0.04685740, 0.77298127, 314.20272064 + 428.49512595 * T, 172.43281431, 73.96250215), eH)
    rahu_trop = normalize_degrees(125.0445550 - 1934.1361849 * T)
    ketu_trop = normalize_degrees(rahu_trop + 180.0)

    trop_map = {
        1: sun_trop, 2: moon_trop, 3: mars_trop, 4: merc_trop, 5: jup_trop,
        6: ven_trop, 7: sat_trop, 8: rahu_trop, 9: ketu_trop, 0: uranus_trop
    }

    result = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
        sid_deg = normalize_degrees(trop_map[pid] - ayanamsa)
        detail = degree_to_sign_detail(sid_deg)
        meta = PLANETS_META[pid]
        sign_info = ZODIAC_SIGNS[detail["signId"]]
        result.append({
            "id": pid,
            "symbol": meta["symbol"],
            "name": meta["name"],
            "keyword": meta["keyword"],
            "degree": sid_deg,
            "signId": detail["signId"],
            "signName": sign_info["thaiName"],
            "signDegree": detail["signDegree"],
            "arcMinutes": detail["arcMinutes"]
        })
    return result

# 1. การคำนวณลัคนาแบบอันโตนาทีสามัญ (สุริยยาตร์ สมผุสอาทิตย์อุทัย + ตัดเวลาท้องถิ่น LMT) -> มาตรฐานโหราศาสตร์ไทย
def calculate_ascendant_antona(year, month, day, hour, minute, lng):
    # LMT offset from standard meridian 105E (1 deg = 4 minutes)
    lmt_offset = (105.0 - lng) * 4.0
    total_min = hour * 60.0 + minute - lmt_offset
    if total_min < 0:
        total_min += 1440.0

    # Sun position at sunrise (06:00 LMT)
    jd_sun = date_to_julian_day(year, month, day, 6 - 7, 0)
    planets = calculate_planets(jd_sun)
    sun = next(p for p in planets if p['id'] == 1)

    sun_sign = sun['signId']
    sun_deg = sun['signDegree'] + sun['arcMinutes'] / 60.0

    elapsed = (total_min - 360.0) % 1440.0
    time_rem_sun = ((30.0 - sun_deg) / 30.0) * ANTONA_TI_SAMANYA[sun_sign]

    if elapsed < time_rem_sun:
        asc_sign = sun_sign
        asc_deg = sun_deg + (elapsed / ANTONA_TI_SAMANYA[sun_sign]) * 30.0
    else:
        elapsed -= time_rem_sun
        curr_sign = (sun_sign + 1) % 12
        while elapsed >= ANTONA_TI_SAMANYA[curr_sign]:
            elapsed -= ANTONA_TI_SAMANYA[curr_sign]
            curr_sign = (curr_sign + 1) % 12
        asc_sign = curr_sign
        asc_deg = (elapsed / ANTONA_TI_SAMANYA[curr_sign]) * 30.0

    sign_info = ZODIAC_SIGNS[asc_sign]
    sign_deg_int = int(asc_deg)
    arc_min_int = int((asc_deg - sign_deg_int) * 60.0)

    nakshatras = [
        "อัศวินี (ทลิทโทฤกษ์)", "ภรณี (มหัทธโนฤกษ์)", "กฤติกา (โจโรฤกษ์)", "โรหิณี (ภูมิปาโลฤกษ์)",
        "มฤคศิระ (เทศาตรีฤกษ์)", "อารทรา (เทวีฤกษ์)", "ปุนัพสุ (เพชฌฆาตฤกษ์)", "ปุษยะ (ราชาฤกษ์)", "อาศเลษา (สมโณฤกษ์)"
    ]
    nak_idx = int((asc_sign * 30 + asc_deg) // (360.0 / 27.0)) % len(nakshatras)

    return {
        "degree": asc_sign * 30.0 + asc_deg,
        "signId": asc_sign,
        "signName": sign_info["thaiName"],
        "signDegree": sign_deg_int,
        "arcMinutes": arc_min_int,
        "nakshatra": nakshatras[nak_idx],
        "method": "สุริยยาตร์ (อันโตนาทีสามัญ สมผุสอาทิตย์อุทัย)",
        "lmtOffset": lmt_offset,
        "lmtTime": f"{int(total_min // 60):02d}:{int(total_min % 60):02d}"
    }

# 2. การคำนวณลัคนาแบบนิรายนะวิธี ลาหิรี (Local Sidereal Time / RAMC)
def calculate_ascendant_nirayana(jd, lat, lng):
    T = (jd - 2451545.0) / 36525.0
    gmst = normalize_degrees(280.46061837 + 360.98564736629 * (jd - 2451545.0))
    lmst = normalize_degrees(gmst + lng)
    eps = (23.4392911 - 0.0130042 * T) * DEG2RAD
    phi = lat * DEG2RAD
    ramc = lmst * DEG2RAD

    y = math.cos(ramc)
    x = -math.sin(ramc) * math.cos(eps) - math.tan(phi) * math.sin(eps)
    asc_trop = normalize_degrees(math.atan2(y, x) * RAD2DEG)
    ayanamsa = get_lahiri_ayanamsa(jd)
    asc_sid = normalize_degrees(asc_trop - ayanamsa)
    detail = degree_to_sign_detail(asc_sid)
    sign_info = ZODIAC_SIGNS[detail["signId"]]

    nakshatras = [
        "อัศวินี (ทลิทโทฤกษ์)", "ภรณี (มหัทธโนฤกษ์)", "กฤติกา (โจโรฤกษ์)", "โรหิณี (ภูมิปาโลฤกษ์)",
        "มฤคศิระ (เทศาตรีฤกษ์)", "อารทรา (เทวีฤกษ์)", "ปุนัพสุ (เพชฌฆาตฤกษ์)", "ปุษยะ (ราชาฤกษ์)", "อาศเลษา (สมโณฤกษ์)"
    ]
    nak_idx = int(asc_sid // (360.0 / 27.0)) % len(nakshatras)

    return {
        "degree": asc_sid,
        "signId": detail["signId"],
        "signName": sign_info["thaiName"],
        "signDegree": detail["signDegree"],
        "arcMinutes": detail["arcMinutes"],
        "nakshatra": nakshatras[nak_idx],
        "method": "นิรายนะวิธี (ลาหิรี Ayanamsa / เวลานักษัตร RAMC)"
    }

def resolve_coordinates(prov_name, district_name=""):
    prov_data = PROVINCES_DICT.get(prov_name, PROVINCES_DICT["กรุงเทพมหานคร"])
    districts = prov_data.get("districts", {})
    if district_name and district_name in districts:
        coords = districts[district_name]
    else:
        coords = {"lat": prov_data["lat"], "lng": prov_data["lng"]}
    return coords, prov_data

def calculate_local_solar_times(year, month, day, lat, lng):
    """
    Calculates precise local sunrise, sunset, and solar noon in Thai Standard Time (UTC+7).
    """
    dt = datetime.date(year, month, day)
    day_of_year = dt.timetuple().tm_yday
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
    
    lat_rad = math.radians(lat)
    zenith = math.radians(90.8333) # Official sunrise zenith
    cos_ha = math.cos(zenith) / (math.cos(lat_rad) * math.cos(decl)) - math.tan(lat_rad) * math.tan(decl)
    cos_ha = max(-1.0, min(1.0, cos_ha))
    ha_deg = math.degrees(math.acos(cos_ha))
    
    solar_noon_min = 720.0 + 4.0 * (105.0 - lng) - eqtime
    sunrise_min = solar_noon_min - ha_deg * 4.0
    sunset_min = solar_noon_min + ha_deg * 4.0
    
    def min_to_str(m):
        m = (m + 1440.0) % 1440.0
        hh = int(m // 60)
        mm = int(round(m % 60))
        if mm == 60:
            hh = (hh + 1) % 24
            mm = 0
        return f"{hh:02d}:{mm:02d}"
        
    return {
        "sunriseMinutes": sunrise_min,
        "sunsetMinutes": sunset_min,
        "solarNoonMinutes": solar_noon_min,
        "sunriseStr": min_to_str(sunrise_min),
        "sunsetStr": min_to_str(sunset_min),
        "solarNoonStr": min_to_str(solar_noon_min),
        "minToStr": min_to_str
    }

def calculate_transit_horizon(ty, tm, td, transit_coords, natal_asc_sign):
    """
    Calculates rising sign at local transit location and its astrological relationship with natal ascendant.
    """
    transit_asc = calculate_ascendant_antona(ty, tm, td, 6, 0, transit_coords["lng"])
    diff = (transit_asc["signId"] - natal_asc_sign + 12) % 12
    house_relation = BHAVAS_LIST[diff]
    
    aspect_notes = {
        0: "กุมลัคน์เดิม (ตนุ) — พลังแห่งตัวตนเข้มข้น มีความมั่นใจและริเริ่มสิ่งใหม่ได้ดีเยี่ยม",
        1: "กดุมภะ (ภพ 2) — ส่องผลต่อเรื่องการเงิน ทรัพย์สิน และการหารายได้เป็นหลัก",
        2: "สหัชชะ (ภพ 3) โยคหน้า — มิตรสหายและการติดต่อสื่อสารเกื้อหนุน การเดินทางราบรื่น",
        3: "พันธุ (ภพ 4) จตุโกณ — เน้นเรื่องหลักทรัพย์ บ้าน ครอบครัว และความมั่นคง",
        4: "ปุตตะ (ภพ 5) ตรีโกณธาตุ — จุดประกายความคิดสร้างสรรค์ เสี่ยงโชค และความรักสดชื่น",
        5: "อริ (ภพ 6) — ควรระวังเรื่องข้อขัดแย้ง บริวาร หรือการจัดการหนี้สิน",
        6: "ปัตนิ (ภพ 7) เล็งลัคน์ — เน้นปฏิสัมพันธ์กับหุ้นส่วน คู่สัญญา หรือคนรักอย่างใกล้ชิด",
        7: "มรณะ (ภพ 8) — เหมาะกับการเคลียร์งานเก่า การศึกษาค้นคว้า และปรับปรุงสิ่งเดิม",
        8: "ศุภะ (ภพ 9) ตรีโกณธาตุ — ผู้ใหญ่เมตตา มีโชคดีเรื่องการเรียน การทำงาน และความสำเร็จ",
        9: "กัมมะ (ภพ 10) จตุโกณ — หน้าที่การงานเด่นชัด ผลงานเป็นที่ประจักษ์ มีภาระหน้าที่สำคัญ",
        10: "ลาภะ (ภพ 11) โยคหลัง — ได้รับผลประโยชน์ โชคลาภ และความสำเร็จเกินคาดหมาย",
        11: "วินาศ (ภพ 12) — เหมาะแก่การทำงานเบื้องหลัง การวางแผนลับ และการทำสมาธิบำเพ็ญบุญ"
    }
    
    return {
        "signId": transit_asc["signId"],
        "signName": transit_asc["signName"],
        "signDegree": transit_asc["signDegree"],
        "arcMinutes": transit_asc["arcMinutes"],
        "houseName": house_relation["name"],
        "relationshipNote": aspect_notes.get(diff, "เกื้อหนุนดวงชะตา")
    }

def _parse_birth_date(date_val):
    if not date_val or not isinstance(date_val, str):
        return 1995, 8, 12
    s = date_val.strip()
    if s.lower() in ("none", "undefined", "null", ""):
        return 1995, 8, 12
    parts = s.split("-")
    if len(parts) != 3:
        return 1995, 8, 12
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        if y > 2400:
            y -= 543
        if not (1 <= m <= 12 and 1 <= d <= 31 and 1800 <= y <= 2650):
            return 1995, 8, 12
        return y, m, d
    except Exception:
        return 1995, 8, 12

def _parse_birth_time(time_val):
    if not time_val or not isinstance(time_val, str):
        return 8, 30
    s = time_val.strip()
    if s.lower() in ("none", "undefined", "null", ""):
        return 8, 30
    parts = s.split(":")
    if len(parts) < 2:
        return 8, 30
    try:
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            return 8, 30
        return h, m
    except Exception:
        return 8, 30

def _parse_target_date(target_val):
    now_th = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
    if not target_val or not isinstance(target_val, str):
        return now_th.year, now_th.month, now_th.day, now_th.strftime("%Y-%m-%d")
    s = target_val.strip()
    if s.lower() in ("none", "undefined", "null", ""):
        return now_th.year, now_th.month, now_th.day, now_th.strftime("%Y-%m-%d")
    parts = s.split("-")
    if len(parts) != 3:
        return now_th.year, now_th.month, now_th.day, now_th.strftime("%Y-%m-%d")
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        if y > 2400:
            y -= 543
        if not (1 <= m <= 12 and 1 <= d <= 31):
            return now_th.year, now_th.month, now_th.day, now_th.strftime("%Y-%m-%d")
        return y, m, d, f"{y:04d}-{m:02d}-{d:02d}"
    except Exception:
        return now_th.year, now_th.month, now_th.day, now_th.strftime("%Y-%m-%d")

def get_horoscope(birth_dict, target_date_str=""):
    ty, tm, td, target_date_str = _parse_target_date(target_date_str)

    # Parse birth info safely (supports camelCase and snake_case)
    b_date_raw = birth_dict.get("birthDate") or birth_dict.get("birth_date")
    b_time_raw = birth_dict.get("birthTime") or birth_dict.get("birth_time")
    by, bm, bd = _parse_birth_date(b_date_raw)
    bh, bmin = _parse_birth_time(b_time_raw)
    prov_name = birth_dict.get("province") or birth_dict.get("birth_province") or "กรุงเทพมหานคร"
    if str(prov_name).lower() in ("none", "undefined", "null", ""):
        prov_name = "กรุงเทพมหานคร"
    district_name = birth_dict.get("district") or birth_dict.get("birth_district") or "พระนคร"
    if str(district_name).lower() in ("none", "undefined", "null", ""):
        district_name = "พระนคร"
    calc_method = birth_dict.get("calcMethod") or birth_dict.get("calc_method") or "suriyayatra" # default suriyayatra
    if str(calc_method).lower() in ("none", "undefined", "null", ""):
        calc_method = "suriyayatra"

    # Resolve birth coordinates
    coords, prov_data = resolve_coordinates(prov_name, district_name)
    birth_lmt_offset = (105.0 - coords["lng"]) * 4.0

    # UTC+7 to UTC for planets calculation
    birth_dt = datetime.datetime(by, bm, bd, bh, bmin) - datetime.timedelta(hours=7)
    jd_birth = date_to_julian_day(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour, birth_dt.minute)

    # Natal planets
    natal_planets = calculate_planets(jd_birth)

    # Calculate Ascendant based on chosen method
    if calc_method == "suriyayatra":
        ascendant = calculate_ascendant_antona(by, bm, bd, bh, bmin, coords["lng"])
    else:
        ascendant = calculate_ascendant_nirayana(jd_birth, coords["lat"], coords["lng"])

    asc_sign = ascendant["signId"]

    # Natal houses
    natal_houses = []
    for h in BHAVAS_LIST:
        hid = h["id"]
        sign_id = (asc_sign + hid - 1) % 12
        planets_in_h = [p for p in natal_planets if p["signId"] == sign_id]
        for p in planets_in_h:
            p["houseId"] = hid
            p["houseName"] = h["name"]
        natal_houses.append({
            "id": hid,
            "name": h["name"],
            "signId": sign_id,
            "signName": ZODIAC_SIGNS[sign_id]["thaiName"],
            "meaning": h["meaning"]
        })

    # Transit chart
    transit_dt = datetime.datetime(ty, tm, td, 6, 0) - datetime.timedelta(hours=7)
    jd_transit = date_to_julian_day(transit_dt.year, transit_dt.month, transit_dt.day, transit_dt.hour, transit_dt.minute)
    transit_planets = calculate_planets(jd_transit)

    # Map transit planets to natal houses
    transit_by_house = {i: [] for i in range(1, 13)}
    for tp in transit_planets:
        diff = (tp["signId"] - asc_sign + 12) % 12
        hid = diff + 1
        tp["houseId"] = hid
        tp["houseName"] = BHAVAS_LIST[hid - 1]["name"]
        transit_by_house[hid].append(tp)

    moon_tp = next(p for p in transit_planets if p["id"] == 2)
    moon_house_id = moon_tp.get("houseId", 1)
    moon_house_name = moon_tp.get("houseName", "ตนุ")

    # Transit location resolution & solar times
    is_same_location = birth_dict.get("isSameLocation", True)
    if isinstance(is_same_location, str):
        is_same_location = is_same_location.lower() in ("true", "1", "yes")

    if is_same_location:
        transit_prov_name = prov_name
        transit_district_name = district_name
    else:
        transit_prov_name = birth_dict.get("transitProvince", prov_name)
        transit_district_name = birth_dict.get("transitDistrict", "")

    transit_coords, _ = resolve_coordinates(transit_prov_name, transit_district_name)
    transit_lmt_offset = (105.0 - transit_coords["lng"]) * 4.0

    # Local solar times (sunrise, sunset, solar noon) at transit location
    solar_times = calculate_local_solar_times(ty, tm, td, transit_coords["lat"], transit_coords["lng"])
    
    # Calculate Transit Horizon (Rising sign at transit location and aspect to natal ascendant)
    transit_horizon = calculate_transit_horizon(ty, tm, td, transit_coords, asc_sign)
    weekday_idx = datetime.datetime(ty, tm, td).weekday() # 0=Mon, 6=Sun

    # Synthesize rich, detailed daily forecasts across all categories
    categories = synthesize_detailed_categories(
        asc_sign, ascendant["signName"], moon_house_id, moon_house_name,
        transit_by_house, transit_horizon, weekday_idx, ty, tm, td
    )

    # Synthesize detailed lucky boosters, thaksa, chants & auspicious windows
    lucky_info = synthesize_detailed_lucky(
        weekday_idx, ty, tm, td, solar_times, transit_prov_name
    )

    # Add transit location specific highlight to overall category
    if not is_same_location:
        categories["overall"]["highlights"].append(
            f"สถานที่จร (ปัจจุบัน): {transit_prov_name} ({transit_district_name or 'อำเภอเมือง'}) อาทิตย์อุทัย {solar_times['sunriseStr']} น. (LMT ปัจจุบัน: ตัด {transit_lmt_offset:.1f} นาที)"
        )
    else:
        categories["overall"]["highlights"].append(
            f"สถานที่จร: สถิต ณ ภูมิลำเนาเกิด (อาทิตย์อุทัย {solar_times['sunriseStr']} น. / อัสดง {solar_times['sunsetStr']} น.)"
        )

    return {
        "date": target_date_str,
        "natalChart": {
            "birthInfo": {
                **birth_dict,
                "district": district_name,
                "calcMethod": calc_method,
                "latitude": coords["lat"],
                "longitude": coords["lng"],
                "lmtOffset": round(birth_lmt_offset, 2)
            },
            "ascendant": ascendant,
            "planets": natal_planets,
            "houses": natal_houses,
            "ayanamsa": get_lahiri_ayanamsa(jd_birth)
        },
        "transitLocation": {
            "isSameLocation": is_same_location,
            "province": transit_prov_name,
            "district": transit_district_name or ("พระนคร" if transit_prov_name == "กรุงเทพมหานคร" else f"อำเภอเมือง{transit_prov_name}"),
            "latitude": transit_coords["lat"],
            "longitude": transit_coords["lng"],
            "lmtOffsetMinutes": round(transit_lmt_offset, 2),
            "sunriseTime": solar_times["sunriseStr"],
            "sunsetTime": solar_times["sunsetStr"],
            "solarNoonTime": solar_times["solarNoonStr"],
            "transitHorizon": transit_horizon
        },
        "transitChart": {
            "targetDate": target_date_str,
            "planets": transit_planets
        },
        "categories": categories,
        "luckyInfo": lucky_info,
        "quickSummary": f"ดวงรายวันลัคนาราศี{ascendant['signName']}: {categories['overall']['theme']} (คะแนนรวม {categories['overall']['score']}%)"
    }

def compute_28day_forecast(birth_dict: dict, start_date_str: str = None) -> dict:
    """
    Compute a 28-day forward astrological forecast trend from start_date_str.
    Identifies:
      - Daily score trend for 28 days
      - Top Golden Auspicious Days (วันมงคลทำการใหญ่ เช่น เซ็นสัญญา ออกรถ เปิดตัว ลงทุน)
      - Top Caution Days (วันควรระวัง ชะลอเรื่องสำคัญ มีสติรอบคอบ)
      - 4-week phase breakdown (Weeks 1 to 4)
    """
    now_th = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
    if start_date_str:
        try:
            start_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            start_dt = now_th.date()
    else:
        start_dt = now_th.date()

    thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    thai_months = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    thai_full_months = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

    days = []
    asc_name = ""
    for offset in range(28):
        cur_date = start_dt + datetime.timedelta(days=offset)
        d_str = cur_date.strftime("%Y-%m-%d")
        
        try:
            h = get_horoscope(birth_dict, d_str)
            cats = h.get("categories", {})
            ov = cats.get("overall", {})
            score = ov.get("score", 75)
            theme = ov.get("theme", "")
            career_sc = cats.get("career", {}).get("score", score)
            finance_sc = cats.get("finance", {}).get("score", score)
            love_sc = cats.get("love", {}).get("score", score)
            health_sc = cats.get("health", {}).get("score", score)
            if not asc_name:
                asc_name = h.get("natalChart", {}).get("ascendant", {}).get("signName", "")
        except Exception:
            score = 75
            theme = "ดวงชะตาราบรื่นปานกลาง"
            career_sc = finance_sc = love_sc = health_sc = 75

        day_name = thai_days[cur_date.weekday()]
        short_label = f"{day_name[:2]} {cur_date.day} {thai_months[cur_date.month]}"
        full_label = f"วัน{day_name}ที่ {cur_date.day} {thai_full_months[cur_date.month]}"

        cat_scores = [("การงาน", career_sc), ("การเงิน", finance_sc), ("ความรัก", love_sc), ("สุขภาพ", health_sc)]
        top_cat_name, top_cat_sc = max(cat_scores, key=lambda x: x[1])

        days.append({
            "offset": offset,
            "dayIndex": offset + 1,
            "date": d_str,
            "day": cur_date.day,
            "month": cur_date.month,
            "weekday": day_name,
            "shortLabel": short_label,
            "fullLabel": full_label,
            "score": score,
            "theme": theme,
            "topCategory": top_cat_name,
            "isToday": (offset == 0),
            "scores": {
                "overall": score,
                "career": career_sc,
                "finance": finance_sc,
                "love": love_sc,
                "health": health_sc
            }
        })

    sorted_days = sorted(days, key=lambda x: x["score"], reverse=True)
    highest_score = sorted_days[0]["score"]
    lowest_score = sorted_days[-1]["score"]
    avg_score = round(sum(d["score"] for d in days) / 28)

    golden_action_templates = [
        "เหมาะเซ็นสัญญา เจรจาธุรกิจ ปิดการขายสำคัญ",
        "เหมาะออกรถใหม่ ขึ้นบ้านใหม่ หรือเริ่มต้นโปรเจกต์ใหญ่",
        "เหมาะเจรจาขอความช่วยเหลือ ผู้ใหญ่อุปถัมภ์ สมัครงาน",
        "เหมาะลงทุน เสี่ยงโชคลาภ เจรจาเรื่องการเงิน"
    ]
    caution_templates = [
        "ควรระวังเอกสารสัญญาผิดพลาด ชะลอการตัดสินใจเรื่องใหญ่",
        "ระวังความใจร้อน ปากไว หลีกเลี่ยงข้อพิพาทและการปะทะ",
        "มีสติในการขับขี่เดินทาง และระวังค่าใช้จ่ายฉุกเฉิน",
        "งดเริ่มงานใหญ่ รักษาสุขภาพ และพักผ่อนให้เพียงพอ"
    ]

    golden_candidates = [d for d in sorted_days if d["score"] >= 80]
    if len(golden_candidates) < 3:
        golden_candidates = sorted_days[:3]
    golden_days = golden_candidates[:4]
    for idx, g in enumerate(golden_days):
        g["status"] = "golden"
        g["badge"] = "🌟 วันมงคลทำการใหญ่"
        g["actionAdvice"] = golden_action_templates[idx % len(golden_action_templates)]

    caution_candidates = [d for d in sorted_days[::-1] if d["score"] <= 68]
    if len(caution_candidates) < 2:
        caution_candidates = sorted_days[::-1][:2]
    caution_days = caution_candidates[:3]
    for idx, c in enumerate(caution_days):
        c["status"] = "caution"
        c["badge"] = "⚠️ วันควรระวังรอบคอบ"
        c["actionAdvice"] = caution_templates[idx % len(caution_templates)]

    golden_dates = {g["date"] for g in golden_days}
    caution_dates = {c["date"] for c in caution_days}
    for d in days:
        if d["date"] in golden_dates:
            d["status"] = "golden"
            d["badge"] = "🌟 วันมงคลทำการใหญ่"
        elif d["date"] in caution_dates:
            d["status"] = "caution"
            d["badge"] = "⚠️ วันควรระวังรอบคอบ"
        else:
            d["status"] = "steady"
            d["badge"] = "✨ ราบรื่นตามปกติ"
            d["actionAdvice"] = "ดำเนินงานตามแผน รักษาสมดุลชีวิตได้ดีเยี่ยม"

    weeks = []
    for w_idx in range(4):
        w_days = days[w_idx * 7 : (w_idx + 1) * 7]
        w_avg = round(sum(d["score"] for d in w_days) / 7)
        w_start = w_days[0]["shortLabel"]
        w_end = w_days[-1]["shortLabel"]
        
        if w_avg >= 80:
            w_theme = "สัปดาห์ทองแห่งความสำเร็จและโอกาสใหม่"
        elif w_avg >= 74:
            w_theme = "สัปดาห์แห่งความก้าวหน้าราบรื่นต่อเนื่อง"
        else:
            w_theme = "สัปดาห์เน้นความสุขุมรอบคอบและตั้งรับ"

        weeks.append({
            "weekNumber": w_idx + 1,
            "label": f"สัปดาห์ที่ {w_idx + 1} ({w_start} - {w_end})",
            "avgScore": w_avg,
            "theme": w_theme,
            "days": w_days
        })

    end_dt = start_dt + datetime.timedelta(days=27)
    date_range_label = f"{start_dt.day} {thai_months[start_dt.month]} - {end_dt.day} {thai_months[end_dt.month]} {start_dt.year + 543}"

    return {
        "startDate": start_dt.strftime("%Y-%m-%d"),
        "endDate": end_dt.strftime("%Y-%m-%d"),
        "dateRangeLabel": date_range_label,
        "ascendant": asc_name,
        "averageScore": avg_score,
        "highestScore": highest_score,
        "lowestScore": lowest_score,
        "peakDay": golden_days[0],
        "lowestDay": caution_days[0],
        "goldenDays": golden_days,
        "cautionDays": caution_days,
        "weeks": weeks,
        "days": days
    }

