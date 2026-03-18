# compute_d_bertopic.py
# Script to calculate Semantic Drift (D) using BERTopic
# Created for Politomorphism SRM project

import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from scipy.stats import entropy
import os

# ================== CHANGE ONLY THIS LINE ==================
symbol_name = "Georgescu"          # Change to: Trump, Ciolacu, Zelensky, Simion, etc.
# ===========================================================

input_file = f"data/data_{symbol_name.lower()}.csv"

print(f"Computing D for: {symbol_name}")

if not os.path.exists(input_file):
    print(f"ERROR: File {input_file} not found!")
    print("Please upload your titles CSV to the data/ folder first.")
    exit()

df = pd.read_csv(input_file)
docs = df['title'].astype(str).tolist()

print(f"Loaded {len(docs)} titles.")

print("Generating embeddings...")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = embedding_model.encode(docs, show_progress_bar=True)

print("Running BERTopic...")
topic_model = BERTopic(
    embedding_model=embedding_model,
    min_topic_size=8,
    nr_topics=None,
    calculate_probabilities=True
)

topics, probs = topic_model.fit_transform(docs, embeddings)

topic_probs = np.mean(probs, axis=0)
valid_probs = topic_probs[topic_probs > 1e-8]

if len(valid_probs) > 1:
    D_raw = entropy(valid_probs, base=2)
    D = D_raw / np.log2(len(valid_probs))
else:
    D = 0.0

print("\n" + "="*50)
print(f"RESULTS for {symbol_name.upper()}")
print(f"Semantic Drift D = {D:.4f}")
print(f"Number of topics = {len(valid_probs)}")
print("="*50)

os.makedirs("results", exist_ok=True)
with open(f"results/D_{symbol_name.lower()}.txt", "w") as f:
    f.write(f"Symbol: {symbol_name}\nD = {D:.4f}\n")
