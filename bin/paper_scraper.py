# Import modules that are needed
import requests
import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from Bio import Entrez
from bs4 import BeautifulSoup

# ── CONFIG ──────────────────────────────────────────────
QUERY      = "pQTL AND (IP-10 OR IL-2 OR IL-13) AND tuberculosis"
MAX_PAPERS = 50
OUTPUT     = "results/thesis_literature.csv"
KW_OUTPUT  = "results/thesis_keywords.csv"
# ────────────────────────────────────────────────────────

def fetch_papers(query, n):
    print(f"Searching Europe PMC: '{query}'")
    r = requests.get(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        params={"query": query, "format": "json",
                "pageSize": n, "resultType": "core"}
    )
    r.raise_for_status()
    results = r.json()["resultList"]["result"]
    print(f"Retrieved {len(results)} papers")
    return [{
        "id":       a.get("id"),
        "title":    a.get("title", ""),
        "abstract": a.get("abstractText", ""),
        "year":     a.get("pubYear"),
        "journal":  a.get("journalTitle", ""),
        "doi":      a.get("doi", ""),
        "cited_by": a.get("citedByCount", 0)
    } for a in results]

def extract_keywords(abstracts, top_n=30):
    vec = TfidfVectorizer(
        stop_words="english",
        max_features=200,
        ngram_range=(1, 2)
    )
    mat = vec.fit_transform(abstracts)
    scores = np.asarray(mat.mean(axis=0)).flatten()
    terms  = vec.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return pd.DataFrame(ranked[:top_n], columns=["term", "tfidf_score"])

# ── MAIN ────────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Fetch
    papers = fetch_papers(QUERY, MAX_PAPERS)
    df = pd.DataFrame(papers)

    # 2. Filter to papers with abstracts
    df_abs = df[df["abstract"].str.len() > 50].reset_index(drop=True)
    print(f"{len(df_abs)} papers have usable abstracts")

    # 3. Export papers
    df_abs.to_csv(OUTPUT, index=False)
    print(f"Papers saved → {OUTPUT}")

    # 4. Extract keywords
    kw_df = extract_keywords(df_abs["abstract"].tolist())
    kw_df.to_csv(KW_OUTPUT, index=False)
    print(f"Keywords saved → {KW_OUTPUT}")

    print("\nTop 15 keywords:")
    print(kw_df.head(15).to_string(index=False))