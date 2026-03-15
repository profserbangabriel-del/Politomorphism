import requests
import json
import time
import csv
import os
from datetime import datetime, date

# NYT API Key - stored as GitHub Secret NYT_API_KEY
API_KEY = os.environ.get('NYT_API_KEY', '')

def get_article_count(query, begin_date, end_date, api_key):
    """Get article count for a query in a date range."""
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        'q': query,
        'begin_date': begin_date,
        'end_date': end_date,
        'api-key': api_key
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()['response']['meta']['hits']
        elif r.status_code == 429:
            print("Rate limit hit - waiting 12 seconds...")
            time.sleep(12)
            return get_article_count(query, begin_date, end_date, api_key)
        else:
            print(f"Error {r.status_code}: {r.text[:100]}")
            return 0
    except Exception as e:
        print(f"Request error: {e}")
        return 0

def get_monthly_counts(query, start_year, start_month, end_year, end_month, api_key):
    """Get monthly article counts."""
    results = []
    year, month = start_year, start_month

    while (year, month) <= (end_year, end_month):
        # First and last day of month
        begin = f"{year}{month:02d}01"
        if month == 12:
            end = f"{year}{month:02d}31"
        else:
            import calendar
            last_day = calendar.monthrange(year, month)[1]
            end = f"{year}{month:02d}{last_day:02d}"

        count = get_article_count(query, begin, end, api_key)
        date_str = f"{year}-{month:02d}-01"
        results.append({'date': date_str, 'count': count, 'year': year, 'month': month})
        print(f"  {date_str}: {count} articles")

        # NYT API rate limit: 10 requests/minute
        time.sleep(6)

        month += 1
        if month > 12:
            month = 1
            year += 1

    return results

print("=== NYT API Data Collection for Mandela ===")
print(f"API Key: {'SET' if API_KEY else 'NOT SET'}")

if not API_KEY:
    print("ERROR: NYT_API_KEY environment variable not set")
    exit(1)

os.makedirs('data_mandela', exist_ok=True)

# BASELINE: 1988-01 to 1990-01 (pre-release)
print("\nCollecting BASELINE data (1988-1990)...")
baseline = get_monthly_counts('mandela', 1988, 1, 1990, 1, API_KEY)

with open('data_mandela/mandela_baseline.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'count', 'year', 'month'])
    writer.writeheader()
    writer.writerows(baseline)
print(f"Baseline saved: {len(baseline)} months")

# ANALYSIS: 1990-02 to 1991-12 (post-release)
print("\nCollecting ANALYSIS data (1990-1991)...")
analysis = get_monthly_counts('mandela', 1990, 2, 1991, 12, API_KEY)

with open('data_mandela/mandela_analysis.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'count', 'year', 'month'])
    writer.writeheader()
    writer.writerows(analysis)
print(f"Analysis saved: {len(analysis)} months")

# Also get titles for VADER (Feb-Apr 1990)
print("\nCollecting titles for VADER (Feb-Apr 1990)...")
titles = []
for begin, end in [('19900211', '19900228'), ('19900301', '19900331'), ('19900401', '19900430')]:
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    for page in range(5):
        params = {'q': 'mandela', 'begin_date': begin, 'end_date': end,
                  'page': page, 'api-key': API_KEY}
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            docs = r.json()['response']['docs']
            if not docs:
                break
            for d in docs:
                titles.append({
                    'publish_date': d['pub_date'][:10],
                    'title': d['headline']['main'],
                    'media_name': 'nytimes.com'
                })
        time.sleep(6)

with open('data_mandela/mandela_titles.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['publish_date', 'title', 'media_name'])
    writer.writeheader()
    writer.writerows(titles)
print(f"Titles saved: {len(titles)}")
print("\nDone! All Mandela data collected.")

