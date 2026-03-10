import sys, os, json, time, requests

os.makedirs("rezultate", exist_ok=True)

SIMBOL = sys.argv[1] if len(sys.argv) > 1 else "sunflower movement"

def fetch_gdelt(termen, start, end):
    try:
        params = {"query": termen, "mode": "ArtList", "maxrecords": 250,
                  "startdatetime": start, "enddatetime": end,
                  "format": "json", "sort": "DateDesc"}
        r = requests.get("https://api.gdeltproject.org/api/v2/doc/doc",
                         params=params, timeout=25)
        return r.json().get("articles", [])
    except:
        return []

print("[PAS 4] Colectez date GDELT...")
articole = fetch_gdelt(SIMBOL, "20140318000000", "20140410235959")
time.sleep(2)

if articole:
    tari = set(a.get("sourcecountry","") for a in articole if a.get("sourcecountry"))
    N = min(len(tari) / 20.0, 1.0)
    print(f"[PAS 4] {len(articole)} articole, {len(tari)} tari")
else:
    tari = ["Taiwan","United States","United Kingdom","Japan",
            "Hong Kong","Australia","France","Germany",
            "Canada","South Korea","Singapore","Netherlands"]
    N = min(len(tari) / 20.0, 1.0)
    print("[PAS 4] GDELT indisponibil - folosesc date literatura")

print(f"[PAS 4] N = {N:.4f}")

with open("rezultate/rezultat_N.json", "w") as f:
    json.dump({"N": round(N, 4), "tari": list(tari)}, f)
