# literatureMaining

Academic literature mining pipeline for keyword extraction from biomedical abstracts. Queries the Europe PMC and PubMed APIs, extracts ranked keywords using TF-IDF, and exports structured CSV outputs for downstream analysis in R or Excel.

Built as part of an MSc Computational Biology thesis (Stellenbosch University) focused on cytokine phenotyping and pQTL mapping in tuberculosis cohorts.

---

## Project structure

```
literatureMaining/
├── bin/                  # Executable scripts
│   └── research_scraper.py
├── src/                  # Reusable modules (future refactoring)
├── data/                 # Raw/intermediate data
├── results/              # Final outputs
│   ├── thesis_literature.csv
│   └── thesis_keywords.csv
└── doc/                  # Notes and documentation
```

---

## Setup

```bash
python3 -m venv research_env
source research_env/bin/activate
pip install requests beautifulsoup4 biopython scikit-learn pandas keybert
```

---

## Usage

Edit the config block at the top of `bin/research_scraper.py`:

```python
QUERY      = "pQTL cytokine tuberculosis IP-10 IL-2 IL-13"
MAX_PAPERS = 50
OUTPUT     = "results/thesis_literature.csv"
KW_OUTPUT  = "results/thesis_keywords.csv"
```

Run from the project root:

```bash
python bin/research_scraper.py
```

---

## Outputs

| File | Description |
|------|-------------|
| `results/thesis_literature.csv` | Papers with title, abstract, year, DOI, citation count |
| `results/thesis_keywords.csv` | Top 30 TF-IDF terms ranked by relevance score |

Both files are `.gitignore`d by default — regenerate them by running the script.

---

## APIs used

- [Europe PMC REST API](https://europepmc.org/RestfulWebService) — primary source, no key required
- [NCBI Entrez (PubMed)](https://www.ncbi.nlm.nih.gov/books/NBK25499/) — via Biopython

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing fallback |
| `biopython` | PubMed/Entrez API wrapper |
| `scikit-learn` | TF-IDF keyword extraction |
| `pandas` | DataFrame and CSV export |
| `keybert` | Semantic keyphrase extraction (optional) |
