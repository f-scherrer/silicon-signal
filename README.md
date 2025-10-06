# silicon-signal

**AI-first, modular quant stack focused on the semiconductor sector.**
Baseline (fundamental & technical) features, sentiment, supply-chain graph, GNNs, meta-labeling, and a multimodal master model.

**License:** _Business Source License 1.1 (BUSL-1.1)_

- **No production/commercial use** without a separate commercial license.
- Non-production academic research use is permitted. ‘Production’ means use in or for the benefit of any third party or for revenue-generating services.
- On **2029-10-01**, the license will change to **GPL-3.0-or-later**.
  See [LICENSE](./LICENSE) for details.

> **Status:** Phase 1 — _Fundamental & Technical Features_ (Module 1)

---

## Table of Contents

- [Goals](#goals)
- [Architecture & Modules](#architecture--modules)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [Configuration & Environment](#configuration--environment)
- [Module 1: Baseline Features](#module-1-baseline-features)
- [Data & Artifacts](#data--artifacts)
- [Tests, Linting, Format](#tests-linting-format)
- [Docker & Compose](#docker--compose)
- [Roadmap](#roadmap)
- [License](#license)
- [Troubleshooting](#troubleshooting)
- [Contributing & Contact](#contributing--contact)

---

## Goals

- **Reliable ETL core** for prices/fundamentals/indicators as the foundation for ML.
- **Modularity:** each module has a clear `run()` entry point, data contracts, and reproducible outputs.
- **Reproducibility:** unified time indices, NaN policies, normalization, tests.
- **Scalability:** Docker-ready for easy server/cloud deployment.

---

## Architecture & Modules

1. **Fundamental & Technical Features** — _baseline cleanup_ (pandas, ta, scikit-learn)
2. **Sentiment Analysis** — _market mood_ (transformers, FinBERT)
3. **Supply-Chain Graph Data** — _network relationships_ (networkx)
4. **GNN Module** — _shock propagation_ (torch-geometric)
5. **Meta-Labeling** — _signal filtering_ (xgboost, scikit-learn)
6. **Multimodal Master Model** — _fusion_ (PyTorch, transformers)
7. **Online Learning** — _continual learning_ (river)
8. **Causal Inference** — _cause–effect checks_ (DoWhy, EconML)

> Implemented now: **Module 1**. Other modules are prepared as stubs.

---

## Project Structure

```
trading-algo/
├─ src/
│  ├─ core/                     # shared infra: config, logging, io, types, registry
│  ├─ modules/
│  │  ├─ 01_baseline_features/  # ← active: ETL + indicators
│  │  ├─ 02_sentiment/
│  │  ├─ 03_supply_graph/
│  │  ├─ 04_gnn/
│  │  ├─ 05_meta_labeling/
│  │  ├─ 06_master_multimodal/
│  │  ├─ 07_online_learning/
│  │  └─ 08_causal_inference/
│  ├─ main.py                   # CLI / orchestration
│  └─ pipelines.py              # DAG definitions
├─ config/                      # YAML config & logging
├─ data/                        # artifacts (raw/interim/features) — gitignored
├─ tests/
├─ Dockerfile / docker-compose.yml
├─ requirements*.txt / pyproject.toml
├─ .env.example / .gitignore
└─ LICENSE / README.md
```

---

## Quickstart

### Prereqs

- **Python 3.11+**
- **Git**
- **(Windows)** PowerShell, optionally WSL2
- **Docker Desktop** (for container runs)

### Setup (local)

```powershell
git clone git@github.com:f-scherrer/silicon-signal.git
cd silicon-signal
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env
```

First run (minimal pipeline = Module 1):

```powershell
python -m src.main --pipeline minimal
```

> Without raw data you’ll see warnings (no parquet files yet) — that’s expected.

---

## Configuration & Environment

- **`.env.example`** → template committed to the repo (no secrets).
- **`.env`** → your local/private values (gitignored).

Sample `.env.example`:

```dotenv
ENV=dev
DATA_DIR=./data
```

Excerpt `config/config.yaml`:

```yaml
market:
  universe: ["NVDA", "AMD", "ASML", "TSM", "AVGO", "INTC"]

baseline:
  price_source: "yfinance"
  tf: "1d"
  resample_to: "W"
  tech_indicators: ["EMA_20", "EMA_50", "RSI_14", "ATR_14", "MACD"]
```

---

## Module 1: Baseline Features

**Goal:** Load prices → compute technical indicators (EMA, RSI, MACD, …) → resample to weekly (W) → save as Parquet.

**Entrypoints:**

```powershell
# run module 1 directly
python -c "from src.modules.01_baseline_features.run import run; run()"

# or the minimal pipeline:
python -m src.main --pipeline minimal
```

**Generate dummy data (for quick testing):**

```powershell
@'
import pandas as pd, numpy as np, os
os.makedirs("data/raw/prices", exist_ok=True)
for t in ["NVDA","AMD"]:
    dt = pd.date_range("2023-01-01","2023-03-31", freq="D")
    px = 100 + np.cumsum(np.random.randn(len(dt)))
    df = pd.DataFrame({"ticker":t,"ts":dt,"open":px,"high":px+1,"low":px-1,"close":px,"volume":1000})
    df.to_parquet(f"data/raw/prices/{t}.parquet", index=False)
print("done")
'@ | Set-Content scripts_make_dummy.py

python .\scripts_make_dummy.py
python -c "from src.modules.01_baseline_features.run import run; run()"
```

**Output:** `data/features/tech/<TICKER>.parquet`

---

## Data & Artifacts

- Working dir for artifacts: `./data` (configurable via `.env`).
- **Not** versioned: `data/` is gitignored.
- Schemas/contracts: see `src/core/types.py` and path registry `src/core/registry.py`.

---

## Tests, Linting, Format

```powershell
# tests
pytest -q

# lint & format
ruff check src tests
black src tests
isort src tests
```

_(If you use a Makefile and Bash, you can also run `make test`, `make fmt`, `make lint`.)_

---

## Docker & Compose

**Build & run (minimal):**

```powershell
docker build -t silicon-signal .
docker run --rm -v ${PWD}\data:/app/data silicon-signal
# or:
docker compose up --build
```

---

## Roadmap

- [x] Project scaffold & core infra (config, logging, IO, registry)
- [x] Module 1: technical indicators + parquet outputs
- [ ] Module 1: weekly resample, normalization, NaN policy, tests
- [ ] Module 2: FinBERT sentiment (batch inference, Ticker×Time aggregation)
- [ ] Module 3: supply-chain graph (edge extraction & cleaning)
- [ ] Module 4: GNN embeddings (PyG)
- [ ] Module 5: meta-labeling (XGBoost)
- [ ] Module 6: multimodal fusion (Torch/Transformers)
- [ ] Module 7: online learning (river)
- [ ] Module 8: causal inference (DoWhy/EconML)

---

## License

This repository is **source-available** under the **Business Source License 1.1 (BUSL-1.1)**.

- **No production/commercial use** without a separate commercial license.
- (Optional, if set) _Additional Use Grant_ — e.g., “Non-production academic research use is permitted.”
- On the **Change Date** (e.g., `2029-10-01`), the license automatically changes to **GPL-3.0-or-later** (or your chosen OSI license).

See [LICENSE](./LICENSE) for details.

> _Note:_ BUSL is **not** OSI-approved; GitHub may not show a standard license badge.

---

## Troubleshooting

Coming soon!

---

## Contributing & Contact

- Issues & feature requests → **GitHub Issues**
- For commercial licensing inquiries: **[mail@fscherrer.ch](mailto:mail@fscherrer.ch)**
- Contributions welcome — please note the license terms (BUSL; no production use without a license).

---
