#!/usr/bin/env python3
"""
Vedic Astrology (Jyotish) Ephemeris Calculator
Uses Swiss Ephemeris (pyswisseph) with Lahiri Ayanamsha (Chitrapaksha)
to calculate Sidereal (Nirayana) planetary longitudes, Rashi, Nakshatra,
Pada, Navamsha (D-9), and Lagna (Ascendant).
"""

import sys
import argparse
from datetime import datetime
import json

try:
    import swisseph as swe
except ImportError:
    print("Error: pyswisseph is not installed.", file=sys.stderr)
    sys.exit(1)

# Vedic Constellation and Sign definitions
RASHIS = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

PLANETS = [
    ("Surya (Sun)", swe.SUN),
    ("Chandra (Moon)", swe.MOON),
    ("Mangala (Mars)", swe.MARS),
    ("Budha (Mercury)", swe.MERCURY),
    ("Guru (Jupiter)", swe.JUPITER),
    ("Shukra (Venus)", swe.VENUS),
    ("Shani (Saturn)", swe.SATURN),
    ("Rahu (North Node)", swe.MEAN_NODE)
]

def deg_to_dms(deg_float):
    deg = int(deg_float)
    rem_min = (deg_float - deg) * 60
    minute = int(rem_min)
    second = int((rem_min - minute) * 60)
    return f"{deg:02d}°{minute:02d}'{second:02d}\""

def get_sign_and_deg(lon):
    lon = lon % 360
    sign_idx = int(lon // 30)
    sign_deg = lon % 30
    return sign_idx, sign_deg

def get_nakshatra_and_pada(lon):
    lon = lon % 360
    nak_span = 360.0 / 27.0  # 13° 20' = 13.333333°
    pada_span = nak_span / 4.0 # 3° 20' = 3.333333°
    nak_idx = int(lon // nak_span)
    rem_deg = lon % nak_span
    pada = int(rem_deg // pada_span) + 1
    return nak_idx, pada

def get_navamsha_sign(lon):
    lon = lon % 360
    nav_span = 30.0 / 9.0  # 3° 20'
    nav_idx = int(lon // nav_span) % 12
    return nav_idx

def calculate_chart(year, month, day, hour, minute, second, lat, lon_geo, tz_offset_hours=5.5):
    # Set Lahiri Ayanamsha
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Convert local time to UTC
    decimal_local_time = hour + (minute / 60.0) + (second / 3600.0)
    decimal_utc_time = decimal_local_time - tz_offset_hours

    # Handle day shift if needed
    utc_day = day
    if decimal_utc_time < 0:
        decimal_utc_time += 24.0
        utc_day -= 1
    elif decimal_utc_time >= 24.0:
        decimal_utc_time -= 24.0
        utc_day += 1

    jd_ut = swe.julday(year, month, utc_day, decimal_utc_time)
    ayanamsha = swe.get_ayanamsa_ut(jd_ut)

    # Calculate Ascendant (Lagna)
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon_geo, b'P', swe.FLG_SIDEREAL)
    lagna_lon = ascmc[0] % 360

    results = []

    # Lagna
    s_idx, s_deg = get_sign_and_deg(lagna_lon)
    n_idx, pada = get_nakshatra_and_pada(lagna_lon)
    nav_idx = get_navamsha_sign(lagna_lon)
    results.append({
        "body": "Lagna (Ascendant)",
        "longitude": lagna_lon,
        "sign": RASHIS[s_idx],
        "degree": deg_to_dms(s_deg),
        "nakshatra": NAKSHATRAS[n_idx],
        "pada": pada,
        "navamsha": RASHIS[nav_idx]
    })

    # Planets
    rahu_lon = 0
    for name, p_code in PLANETS:
        res, flag = swe.calc_ut(jd_ut, p_code, swe.FLG_SIDEREAL | swe.FLG_SPEED)
        p_lon = res[0] % 360
        speed = res[3]
        retro = " (R)" if speed < 0 and p_code not in (swe.SUN, swe.MOON, swe.MEAN_NODE) else ""

        if p_code == swe.MEAN_NODE:
            rahu_lon = p_lon

        s_idx, s_deg = get_sign_and_deg(p_lon)
        n_idx, pada = get_nakshatra_and_pada(p_lon)
        nav_idx = get_navamsha_sign(p_lon)

        results.append({
            "body": f"{name}{retro}",
            "longitude": p_lon,
            "sign": RASHIS[s_idx],
            "degree": deg_to_dms(s_deg),
            "nakshatra": NAKSHATRAS[n_idx],
            "pada": pada,
            "navamsha": RASHIS[nav_idx],
            "is_retrograde": speed < 0
        })

    # Ketu (exactly 180 degrees from Rahu)
    ketu_lon = (rahu_lon + 180.0) % 360
    s_idx, s_deg = get_sign_and_deg(ketu_lon)
    n_idx, pada = get_nakshatra_and_pada(ketu_lon)
    nav_idx = get_navamsha_sign(ketu_lon)
    results.append({
        "body": "Ketu (South Node)",
        "longitude": ketu_lon,
        "sign": RASHIS[s_idx],
        "degree": deg_to_dms(s_deg),
        "nakshatra": NAKSHATRAS[n_idx],
        "pada": pada,
        "navamsha": RASHIS[nav_idx],
        "is_retrograde": True
    })

    return {
        "datetime_local": f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}",
        "latitude": lat,
        "longitude": lon_geo,
        "ayanamsha": deg_to_dms(ayanamsha),
        "positions": results
    }

def main():
    parser = argparse.ArgumentParser(description="Vedic Astrology (Jyotish) Ephemeris Calculator")
    parser.add_argument("--date", help="Date in YYYY-MM-DD (defaults to today)")
    parser.add_argument("--time", help="Time in HH:MM:SS (defaults to 12:00:00)")
    parser.add_argument("--lat", type=float, default=22.5726, help="Latitude (default: 22.5726 N - Kolkata)")
    parser.add_argument("--lon", type=float, default=88.3639, help="Longitude (default: 88.3639 E - Kolkata)")
    parser.add_argument("--tz", type=float, default=5.5, help="Timezone offset hours (default: +5.5 for IST)")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    now = datetime.now()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
        year, month, day = d.year, d.month, d.day
    else:
        year, month, day = now.year, now.month, now.day

    if args.time:
        t = datetime.strptime(args.time, "%H:%M:%S")
        hour, minute, second = t.hour, t.minute, t.second
    else:
        hour, minute, second = 12, 0, 0

    chart = calculate_chart(year, month, day, hour, minute, second, args.lat, args.lon, args.tz)

    if args.json:
        print(json.dumps(chart, indent=2))
    else:
        print(f"🔯 Vedic Chart (Nirayana / Lahiri Ayanamsha: {chart['ayanamsha']})")
        print(f"📅 Date & Time: {chart['datetime_local']} | Lat: {chart['latitude']}, Lon: {chart['longitude']}")
        print("=" * 80)
        print(f"{'Body':<22} | {'Sign (Rashi)':<22} | {'Deg':<10} | {'Nakshatra (Pada)':<20} | {'Navamsha (D9)'}")
        print("-" * 80)
        for p in chart["positions"]:
            nak_info = f"{p['nakshatra']} ({p['pada']})"
            print(f"{p['body']:<22} | {p['sign']:<22} | {p['degree']:<10} | {nak_info:<20} | {p['navamsha']}")

if __name__ == '__main__':
    main()
