"""
Fetch Hugo Chavez 2002 media data from GDELT Project
GDELT covers global news from 1979 — free, no API key required
Fetches attention/volume data for baseline and analysis periods
"""
import requests
import csv
import os
import time
from datetime import date, timedelta

OUTPUT_DIR = "data_chavez"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_gdelt_counts(start_date, end_date, query="hugo chavez", output_file="chavez_counts.csv"):
    """
    GDELT DOC 2.0 API — counts articles mentioning query per day
    endpoint: https://api.gdeltproject.org/api/v2/doc/doc
    """
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    # GDELT uses 15-minute intervals; we aggregate to daily
    # Format dates as YYYYMMDDHHMMSS
    start_str = start_date.strftime("%Y%m%d") + "000000"
    end_str   = end_date.strftime("%Y%m%d") + "235959"
    
    params = {
        "query":    f'"{query}"',
        "mode":     "timelinevol",
        "format":   "csv",
        "startdatetime": start_str,
        "enddatetime":   end_str,
        "smoothing": 0,
    }
    
    print(f"  Fetching GDELT: {query} | {start_date} → {end_date}")
    try:
        resp = requests.get(base_url, params=params, timeout=60)
        if resp.status_code == 200 and resp.text.strip():
            lines = resp.text.strip().split("\n")
            rows = []
            for line in lines[1:]:  # skip header
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    try:
                        dt_str = parts[0].strip()
                        count  = float(parts[1].strip())
                        # Parse GDELT datetime format YYYYMMDDHHMMSS
                        if len(dt_str) >= 8:
                            d = date(int(dt_str[:4]), int(dt_str[4:6]), int(dt_str[6:8]))
                            rows.append({"date": d, "count": count})
                    except:
                        pass
            
            # Aggregate to daily totals
            from collections import defaultdict
            daily = defaultdict(float)
            for r in rows:
                daily[r["date"]] += r["count"]
            
            # Compute ratio (normalize by total daily volume)
            total_vol = sum(daily.values()) or 1
            out_path = os.path.join(OUTPUT_DIR, output_file)
            with open(out_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["date","count","ratio"])
                writer.writeheader()
                for d in sorted(daily.keys()):
                    writer.writerow({
                        "date":  d.strftime("%Y-%m-%d"),
                        "count": round(daily[d], 4),
                        "ratio": round(daily[d] / total_vol, 8)
                    })
            
            print(f"  Saved {len(daily)} daily records to {out_path}")
            return True
        else:
            print(f"  GDELT response: {resp.status_code} — {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  GDELT fetch error: {e}")
        return False


def fetch_gdelt_titles(start_date, end_date, query="hugo chavez", output_file="chavez_titles.csv"):
    """
    Fetch article titles for VADER sentiment analysis
    Uses GDELT ArtList mode
    """
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
    start_str = start_date.strftime("%Y%m%d") + "000000"
    end_str   = end_date.strftime("%Y%m%d") + "235959"
    
    params = {
        "query":    f'"{query}" sourcelang:english',
        "mode":     "artlist",
        "format":   "csv",
        "maxrecords": 250,
        "startdatetime": start_str,
        "enddatetime":   end_str,
    }
    
    print(f"  Fetching GDELT titles: {query} | {start_date} → {end_date}")
    try:
        resp = requests.get(base_url, params=params, timeout=60)
        if resp.status_code == 200 and resp.text.strip():
            out_path = os.path.join(OUTPUT_DIR, output_file)
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                f.write(resp.text)
            lines = resp.text.strip().split("\n")
            print(f"  Saved {len(lines)-1} article records to {out_path}")
            return True
        else:
            print(f"  GDELT titles response: {resp.status_code}")
            return False
    except Exception as e:
        print(f"  GDELT titles error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("GDELT Data Fetch — Hugo Chavez 2002")
    print("=" * 60)

    # Baseline: Jan 2000 – Mar 2002
    print("\n[1] Baseline period (2000-01-01 to 2002-03-31)")
    fetch_gdelt_counts(
        date(2000, 1, 1), date(2002, 3, 31),
        query="hugo chavez",
        output_file="chavez_baseline.csv"
    )
    time.sleep(3)

    # Full analysis: Apr – Dec 2002
    print("\n[2] Analysis period — full year (2002-04-01 to 2002-12-31)")
    fetch_gdelt_counts(
        date(2002, 4, 1), date(2002, 12, 31),
        query="hugo chavez",
        output_file="chavez_analysis.csv"
    )
    time.sleep(3)

    # Acute window: Apr 11–20 2002 (coup + reversal)
    print("\n[3] ACUTE WINDOW (2002-04-11 to 2002-04-20) — coup + reversal")
    fetch_gdelt_counts(
        date(2002, 4, 11), date(2002, 4, 20),
        query="hugo chavez",
        output_file="chavez_acute_window.csv"
    )
    time.sleep(3)

    # Titles for VADER (analysis period, English only)
    print("\n[4] Article titles for VADER sentiment (2002-04-01 to 2002-12-31)")
    fetch_gdelt_titles(
        date(2002, 4, 1), date(2002, 12, 31),
        query="hugo chavez",
        output_file="chavez_titles.csv"
    )

    print("\nDone. Files in data_chavez/")
