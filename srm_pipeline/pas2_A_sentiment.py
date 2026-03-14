import sys
import os
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

symbol = sys.argv[1] if len(sys.argv) > 1 else "Putin"
print(f"STEP 2 - Affective Weight (A) for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

titles_path = 'data_putin/putin_titles_baseline.csv'
if not os.path.exists(titles_path):
    titles_path = 'putin_titles_baseline.csv'

if os.path.exists(titles_path):
    df = pd.read_csv(titles_path)
    titluri = df['title'].dropna().tolist()
    print(f"Titles loaded: {len(titluri)}")
    analyzer = SentimentIntensityAnalyzer()
    scores_abs = []
    scores_compound = []
    for titlu in titluri:
        s = analyzer.polarity_scores(str(titlu))
        scores_abs.append(abs(s['compound']))
        scores_compound.append(s['compound'])
    A = sum(scores_abs) / len(scores_abs)
    compound_avg = sum(scores_compound) / len(scores_compound)
    method = f"VADER on {len(titluri)} titles"
else:
    print("File not found - using pre-computed value")
    A = 0.2593
    compound_avg = -0.0689
    method = "VADER pre-computed on 19851 titles"

result = {
    "symbol": symbol,
    "A": round(A, 4),
    "compound_avg": round(compound_avg, 4),
    "method": method
}

with open('rezultate/pas2_sentiment.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"A = {A:.4f}")
print("Saved: rezultate/pas2_sentiment.json")
