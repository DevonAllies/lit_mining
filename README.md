# lit_mining

Academic literature mining pipeline for keyword extraction from biomedical abstracts. Queries the Europe PMC and PubMed APIs, extracts ranked keywords using TF-IDF, downloads open-access PDFs, and exports structured CSV outputs for downstream analysis in R or Python.

Built as part of an MSc Computational Biology thesis (Stellenbosch University) focused on cytokine phenotyping and pQTL mapping in tuberculosis cohorts.

---

## Project structure

```
lit_mining/
├── bin/                  # Executable scripts
│   └── paper_scraper.py
├── src/                  # Reusable modules (future refactoring)
├── data/                 # Raw/intermediate data
├── results/              # Generated outputs (gitignored)
│   ├── thesis_literature.csv
│   ├── thesis_keywords.csv
│   └── <top_keyword>/    # PDF folder named after top TF-IDF term
│       ├── *.pdf
│       └── download_report.csv
└── doc/                  # Notes and documentation
```

---

## Setup

```bash
python3 -m venv research_env
source research_env/bin/activate
pip install requests beautifulsoup4 biopython scikit-learn pandas
```

---

## Usage

Edit the config block at the top of `bin/paper_scraper.py`:

```python
QUERY           = "pQTL cytokine tuberculosis IP-10 IL-2 IL-13"
MAX_PAPERS      = 50
OUTPUT          = "results/thesis_literature.csv"
KW_OUTPUT       = "results/thesis_keywords.csv"
UNPAYWALL_EMAIL = "your@email.com"   # required for Unpaywall PDF fallback
```

Run from the project root:

```bash
python bin/paper_scraper.py
```

---

## Outputs

| File | Description |
|------|-------------|
| `results/thesis_literature.csv` | Papers with title, abstract, year, DOI, citation count |
| `results/thesis_keywords.csv` | Top 30 TF-IDF terms ranked by relevance score |
| `results/<top_keyword>/*.pdf` | Downloaded open-access PDFs, folder named after top keyword |
| `results/<top_keyword>/download_report.csv` | Per-paper download status (`downloaded`, `no_oa_pdf`, `not_found`) |

All files under `results/` are gitignored — regenerate by running the script.

---

## PDF downloads

PDFs are fetched via two sources in order:

1. **Europe PMC OA** — free, no key required, covers all PMC-indexed papers
2. **Unpaywall API** — fallback for non-PMC papers with a DOI; requires a valid email address set in the config

Expect 40–60% download success depending on open-access coverage of your query topic.

---

## APIs used

- [Europe PMC REST API](https://europepmc.org/RestfulWebService) — primary source, no key required
- [NCBI Entrez (PubMed)](https://www.ncbi.nlm.nih.gov/books/NBK25499/) — via Biopython
- [Unpaywall API](https://unpaywall.org/products/api) — open-access PDF lookup, no key required (email only)

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing fallback |
| `biopython` | PubMed/Entrez API wrapper |
| `scikit-learn` | TF-IDF keyword extraction |
| `pandas` | DataFrame and CSV export |