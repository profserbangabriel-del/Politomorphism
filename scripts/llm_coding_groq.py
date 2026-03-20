"""
llm_coding_groq.py
------------------
Înlocuitor drop-in pentru llm_coding.py care folosește Groq API (gratuit).
Funcție: topic coding al articolelor după titlu + URL.

Setare rapidă:
  pip install groq
  export GROQ_API_KEY="gsk_..."   # sau pune direct în GROQ_API_KEY de mai jos
  python llm_coding_groq.py
"""

import os
import csv
import time
import json
import sys
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    print("Instalează SDK-ul Groq: pip install groq")
    sys.exit(1)

# ─── CONFIGURARE ──────────────────────────────────────────────────────────────

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

# Modele disponibile gratuit pe Groq (alege unul):
#   "llama-3.3-70b-versatile"   → cel mai capabil, recomandat
#   "llama3-8b-8192"            → cel mai rapid, limită mai mare
#   "mixtral-8x7b-32768"        → context lung
MODEL = "llama-3.3-70b-versatile"

INPUT_FILE  = "articles.csv"     # CSV cu coloanele: url, title (sau story_url, title)
OUTPUT_FILE = "llm_coded.csv"
CHECKPOINT_EVERY = 25            # salvează la fiecare N articole

# Rate limiting Groq free tier: ~30 req/min pentru 70b, mai mult pentru 8b
DELAY_BETWEEN_REQUESTS = 2.2     # secunde (ajustează dacă primești 429)

# ─── SCHEMA DE CODARE ─────────────────────────────────────────────────────────
# Adaptează categoriile la proiectul tău (acestea sunt exemple pentru datele Trump 2015-2016)

TOPIC_CATEGORIES = [
    "Immigration",
    "Foreign Policy",
    "Economy / Trade",
    "Campaign / Elections",
    "Republican Primary",
    "Democrat Primary",
    "Trump Character / Rhetoric",
    "Media Coverage",
    "National Security / Terrorism",
    "Race / Identity Politics",
    "Other / Irrelevant",
]

SYSTEM_PROMPT = f"""You are a political science research assistant performing systematic content analysis.
Your task: classify news article titles into exactly ONE topic category.

Categories:
{chr(10).join(f"- {c}" for c in TOPIC_CATEGORIES)}

Rules:
- Return ONLY a valid JSON object, nothing else.
- No explanation, no markdown, no extra text.
- JSON format: {{"topic": "<category>", "confidence": <0.0-1.0>, "reasoning": "<one sentence>"}}
- If the title is clearly off-topic or unrelated to politics, use "Other / Irrelevant".
"""

# ─── FUNCȚII ──────────────────────────────────────────────────────────────────

def load_input(filepath: str) -> list[dict]:
    """Încarcă CSV-ul de intrare. Detectează automat coloana cu URL și titlu."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"Fișierul {filepath} este gol.")

    # Detectează coloanele
    cols = rows[0].keys()
    url_col   = next((c for c in cols if "url" in c.lower()), None)
    title_col = next((c for c in cols if "title" in c.lower()), None)

    if not url_col or not title_col:
        raise ValueError(f"Nu găsesc coloanele url/title în: {list(cols)}")

    print(f"Coloane detectate → URL: '{url_col}' | Titlu: '{title_col}'")
    return rows, url_col, title_col


def load_already_coded(filepath: str) -> set[str]:
    """Returnează setul de URL-uri deja procesate (pentru resume)."""
    if not Path(filepath).exists():
        return set()
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["url"] for row in reader if "url" in row}


def code_article(client: Groq, title: str, url: str) -> dict:
    """Trimite un articol la Groq și returnează rezultatul de codare."""
    domain = url.split("/")[2] if "//" in url else url[:30]

    user_msg = f'Source: {domain}\nTitle: "{title}"'

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.1,
        max_tokens=150,
    )

    raw = response.choices[0].message.content.strip()

    # Parsează JSON
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: extrage JSON din text
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            result = {"topic": "Other / Irrelevant", "confidence": 0.0, "reasoning": f"Parse error: {raw[:100]}"}

    return result


def main():
    if not GROQ_API_KEY:
        print("EROARE: Setează GROQ_API_KEY ca variabilă de mediu sau direct în script.")
        print("  Obții cheia gratuit la: https://console.groq.com")
        sys.exit(1)

    client = Groq(api_key=GROQ_API_KEY)

    # Încarcă datele
    rows, url_col, title_col = load_input(INPUT_FILE)
    already_coded = load_already_coded(OUTPUT_FILE)

    total      = len(rows)
    remaining  = [r for r in rows if r[url_col] not in already_coded]
    skipped    = total - len(remaining)

    print(f"Articole totale: {total}")
    print(f"Deja codate:     {skipped}")
    print(f"De procesat:     {len(remaining)}")
    print(f"Model:           {MODEL}")
    print("-" * 50)

    if not remaining:
        print("Totul este deja codat!")
        return

    # Pregătește fișierul de output (append dacă există, creare dacă nu)
    output_exists = Path(OUTPUT_FILE).exists() and skipped > 0
    fieldnames = [url_col, title_col, "topic", "confidence", "reasoning", "model"]

    out_file = open(OUTPUT_FILE, "a" if output_exists else "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    if not output_exists:
        writer.writeheader()

    success = 0
    failed  = 0

    for i, row in enumerate(remaining, 1):
        url   = row[url_col]
        title = row[title_col]
        domain = url.split("/")[2] if "//" in url else url[:30]

        print(f"[{i+skipped}/{total}] {domain} | {title[:60]}...")

        retries = 0
        while retries < 3:
            try:
                result = code_article(client, title, url)

                writer.writerow({
                    url_col:    url,
                    title_col:  title,
                    "topic":       result.get("topic", "Other / Irrelevant"),
                    "confidence":  result.get("confidence", 0.0),
                    "reasoning":   result.get("reasoning", ""),
                    "model":       MODEL,
                })
                out_file.flush()

                print(f"    ✓ {result.get('topic')} (conf: {result.get('confidence', 0):.2f})")
                success += 1
                break

            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate" in err_str.lower():
                    wait = 30 * (retries + 1)
                    print(f"    Rate limit → attept în {wait}s...")
                    time.sleep(wait)
                    retries += 1
                else:
                    print(f"    EROARE: {err_str[:100]}")
                    failed += 1
                    break

        # Checkpoint
        if i % CHECKPOINT_EVERY == 0:
            print(f"\n  ── Checkpoint {i+skipped}/{total}: {success} ok, {failed} eșuate ──\n")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    out_file.close()

    print("\n" + "=" * 50)
    print(f"DONE → Total: {total} | Success: {success} | Failed: {failed}")
    print(f"Rezultate salvate în: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
