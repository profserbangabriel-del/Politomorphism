import sys, os, json, re
import numpy as np
from collections import defaultdict

os.makedirs("rezultate", exist_ok=True)
SIMBOL = sys.argv[1] if len(sys.argv) > 1 else "Calin Georgescu"

# T0 = context PRE-electoral (oct 2024) - cine era Georgescu inainte
CORPUS_T0 = [
    "Georgescu unknown candidate minor politician Romania election campaign",
    "Romania presidential election candidates mainstream parties polling",
    "Romanian politics coalition government opposition parties election race",
    "Georgescu fringe candidate nationalist obscure low polling numbers",
    "Romania election campaign television debates mainstream candidates",
]

# T1 = context POST-24 noiembrie (dupa primul tur)
CORPUS_T1 = [
    "Georgescu winner first round shocked Europe democracy threat NATO",
    "Georgescu TikTok viral manipulation election interference Russia",
    "Georgescu antisemitic pro-Putin extremist far-right danger Romania",
    "Georgescu revolution supporters celebrate corrupt system defeated",
    "Georgescu annulled election constitutional court democratic crisis",
    "Georgescu phenomenon social media manipulation coordinated accounts",
    "Georgescu spiritual national sovereignty authentic voice people",
    "Georgescu symbol resistance Western elites globalism Romania identity",
]

def tokenize(text):
    return re.findall(r'\b[a-z]{3,}\b', text.lower())

def build_context(corpus, targets, window=5):
    ctx = defaultdict(float)
    for doc in corpus:
        tokens = tokenize(doc)
        for i, tok in enumerate(tokens):
            if tok in targets:
                for j in range(max(0,i-window), min(len(tokens),i+window+1)):
                    if j != i and tokens[j] not in targets:
                        ctx[tokens[j]] += 1.0
    return ctx

def cosine(v1, v2):
    common = set(v1) & set(v2)
    if not common: return 0.0
    num = sum(v1[k]*v2[k] for k in common)
    d1 = np.sqrt(sum(x**2 for x in v1.values()))
    d2 = np.sqrt(sum(x**2 for x in v2.values()))
    return num / (d1 * d2) if d1 and d2 else 0.0

TARGET = {"georgescu", "calin", "candidate", "politician", "romania"}
ctx0 = build_context(CORPUS_T0, TARGET)
ctx1 = build_context(CORPUS_T1, TARGET)
D = 1.0 - cosine(ctx0, ctx1)

print(f"[PAS 3] D = {D:.4f}")
with open("rezultate/rezultat_D.json", "w") as f:
    json.dump({"D": round(D, 4), "nota": "drift semantic oct vs dec 2024"}, f)
