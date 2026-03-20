"""
llm_coding_groq.py — drop-in replacement for llm_coding.py
Politomorphism Research Project | Serban Gabriel Florin
Uses Groq API (free) instead of Anthropic API.
"""

import pandas as pd
import json
import time
import os
import re
import sys

# ── Config ────────────────────────────────────────────────────────────────────

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
MODEL        = "llama-3.3-70b-versatile"
INPUT_CSV    = "trump_validation_sample.csv"
OUTPUT_CSV   = "llm_coded.csv"
DELAY        = 2.2

# ── Prompt (identic cu originalul) ────────────────────────────────────────────

SYSTEM_PROMPT = """You are a political communication researcher coding news articles.
You will receive a news article title and outlet.
Return ONLY valid JSON, no explanation, no markdown.

SCORE 1 — PE (Topical Diversity), scale 1-5:
1 = Single topic only
2 = One main topic + one secondary
3 = Two distinct topics balanced
4 = Three or more topics
5 = Highly diverse, unrelated topics

Topics: electoral campaign, immigration, economy, foreign policy,
media/Twitter, Republican Party, legal/judicial, race/religion,
Clinton/Democrats, personal/biography

SCORE 2 — FRAMING toward Trump, scale -2 to +2:
-2 = Strongly anti-Trump
-1 = Mildly anti-Trump
 0 = Neutral/descriptive
+1 = Mildly pro-Trump
+2 = Strongly pro-Trump

Return ONLY this JSON:
{"PE": <1-5>, "framing": <-2 to 2>, "confidence": "high"|"medium"|"low", "reasoning": "<one sentence>"}"""

# ── Single article coding ─────────────────────────────────────────────────────

def code_article(title, outlet, date, phase, max_retries=3):
    try:
        import requests
    except ImportError:
        os.system(f"{sys.executable} -m pip install requests -q")
        import requests

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 200,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Title: {title}\nOutlet: {outlet}\nDate: {date}\nPhase: {phase}"}
        ]
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"].strip()
                text = re.sub(r"```json\s*", "", text)
                text = re.sub(r"```\s*", "", text)
                result = json.loads(text)

                return {
                    "PE_llm":         int(result["PE"]),
                    "framing_llm":    int(result["framing"]),
                    "confidence_llm": result.get("confidence", "medium"),
                    "reasoning_llm":  result.get("reasoning", ""),
                    "error":          None
                }

            elif resp.status_code == 429:
                wait = (attempt + 1) * 30
                print(f"    Rate limit — waiting {wait}s...")
                time.sleep(wait)

            else:
                print(f"    HTTP {resp.status_code}: {resp.text[:200]}")
                break

        except json.JSONDecodeError as e:
            print(f"    JSON parse error: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)

        except Exception as e:
            print(f"    Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    return {
        "PE_llm": None, "framing_llm": None,
        "confidence_llm": None, "reasoning_llm": None,
        "error": "FAILED"
    }

# ── Main coding loop ──────────────────────────────────────────────────────────

def run_coding():
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set")
        sys.exit(1)
    print(f"Groq API key loaded: {GROQ_API_KEY[:12]}...")

    df = pd.read_csv(INPUT_CSV)
    df = df.drop_duplicates(subset=["id"]).head(300)
    print(f"Articles to code: {len(df)}")

    coded_ids     = set()
    existing_rows = []
    if os.path.exists(OUTPUT_CSV):
        existing  = pd.read_csv(OUTPUT_CSV)
        existing  = existing.drop_duplicates(subset=["id"])
        done      = existing[existing["PE_llm"].notna()]
        coded_ids = set(done["id"].tolist())
        existing_rows = done.to_dict("records")
        print(f"Already coded: {len(coded_ids)}")

    to_code = df[~df["id"].isin(coded_ids)]
    print(f"Remaining: {len(to_code)}")

    results = list(existing_rows)

    for i, (_, row) in enumerate(to_code.iterrows()):
        title  = str(row.get("title", ""))[:200]
        outlet = str(row.get("media_name", ""))
        date   = str(row.get("publish_date", ""))
        phase  = str(row.get("phase", ""))

        print(f"[{i+1}/{len(to_code)}] {outlet} | {title[:55]}...")

        result = code_article(title, outlet, date, phase)
        row_dict = row.to_dict()
        row_dict.update(result)
        results.append(row_dict)

        if (i + 1) % 25 == 0:
            pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
            n_ok = sum(1 for r in results if r.get("PE_llm") is not None)
            print(f"  Checkpoint: {n_ok}/{len(results)} ok")

        time.sleep(DELAY)

    final = pd.DataFrame(results)
    final.to_csv(OUTPUT_CSV, index=False)

    n_ok   = final["PE_llm"].notna().sum()
    n_fail = (final["error"] == "FAILED").sum()

    print(f"\n=== DONE ===")
    print(f"Total: {len(final)} | Success: {n_ok} | Failed: {n_fail}")
    print(f"Saved: {OUTPUT_CSV}")

    if n_ok > 0:
        print(f"\nPE distribution:")
        print(final["PE_llm"].value_counts().sort_index().to_string())
        print(f"\nFraming distribution:")
        print(final["framing_llm"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    run_coding()
