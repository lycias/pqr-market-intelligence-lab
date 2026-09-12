# Global Fund PQR Market Intelligence Lab

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Colab](https://img.shields.io/badge/Open%20in-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/lycias/pqr-market-intelligence-lab/blob/main/notebooks/PQR_Market_Intelligence_Lab.ipynb)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](LICENSE)

An explainable machine-learning and market-shaping portfolio project built from the Global Fund's public Price & Quality Reporting (PQR) transaction data. The lab turns historical procurement records into transparent price-review signals, supplier-concentration indicators, and country–product monitoring tables for decision support.

> **Important:** Review signals are screening prompts—not findings of overpricing, misconduct, or automatically achievable savings. Every flagged transaction requires contextual procurement review.

## Why this matters

Global health procurement teams need to distinguish ordinary price variation from transactions that merit closer review, while also monitoring supply-market concentration. This project demonstrates how reproducible data engineering, temporal validation, interpretable machine learning, and careful domain safeguards can support that workflow.

## Analytical design

- **Time-aware evaluation:** training through 2022, model selection on 2023, and an untouched 2024–2025 test set.
- **Strong comparator:** machine-learning performance is assessed against a product–pack median benchmark.
- **Two-model agreement:** the primary context model and a manufacturer-adjusted sensitivity model must agree before a high-price review signal is issued.
- **Leakage controls:** post-purchase and target-derived fields are excluded from prediction.
- **Separate market lenses:** price-review signals and manufacturer-concentration indicators are reported independently.
- **Auditability:** fixed random seed, source register, extraction QA, data dictionary, and machine-readable run manifest.

## Verified run snapshot

The eligible analytical cohort contained **43,054 positive-price transactions**. On the untouched 2024–2025 test set:

| Model | Log-price MAE |
|---|---:|
| Product–pack median baseline | 0.471 |
| Context model | 0.399 |
| Manufacturer-adjusted sensitivity model | 0.372 |

These are predictive—not causal—results. They do not estimate savings or establish why a price differed.

## Repository map

```text
├── notebooks/
│   ├── PQR_Market_Intelligence_Lab.ipynb
│   └── PQR_Market_Intelligence_Lab_Code_Only.ipynb
├── reports/
│   └── PQR_Market_Intelligence_Lab.html
├── code/
│   └── build_ml_ready_pqr.py
├── outputs/
│   ├── model_test_metrics.csv
│   ├── permutation_importance.csv
│   ├── high_price_review_signals_2024_2025.csv
│   ├── country_product_monitoring_2024_2025.csv
│   ├── manufacturer_concentration_recent.csv
│   └── run_manifest.json
├── documentation/
│   ├── REPRODUCIBILITY_GUIDE.md
│   ├── pqr_data_dictionary.csv
│   ├── pqr_extraction_qa.json
│   └── source_register.csv
└── data/README.md
```

## Run in Google Colab

1. Open the [complete notebook in Colab](https://colab.research.google.com/github/lycias/pqr-market-intelligence-lab/blob/main/notebooks/PQR_Market_Intelligence_Lab.ipynb).
2. Place the source files in Google Drive following `documentation/REPRODUCIBILITY_GUIDE.md`.
3. Set `USE_GOOGLE_DRIVE = True` in the path-configuration cell.
4. Select **Runtime → Restart session and run all**.
5. Confirm the final green **Run completed successfully** message.

The project expects this Drive root:

```python
Path('/content/drive/MyDrive/global-health-market-access')
```

## Data access and provenance

Raw transaction files are not committed to this repository. See [`data/README.md`](data/README.md) for the authoritative Global Fund dashboards, the PQR caveats note, expected filenames, and Drive placement. The public source was extracted on 11 September 2026. Data for 2026 were incomplete at extraction and are excluded from full-year model evaluation.

## Responsible interpretation

Before investigating a signal, verify the underlying transaction and consider product specification, pack size, freight treatment, quality status, procurement channel, payment conditions, urgency, lead time, availability, and local regulatory constraints. Supplier concentration is a resilience indicator; it is not, by itself, evidence of insufficient competition.

## Skills demonstrated

Python · pandas · scikit-learn · temporal validation · explainable ML · feature engineering · leakage prevention · procurement analytics · market concentration · data-quality assurance · reproducible research · stakeholder communication

## License and attribution

Project code is released under the MIT License. Data remain subject to the terms, caveats, and attribution requirements of their original providers. This independent portfolio project is not an official Global Fund product and does not imply endorsement.
