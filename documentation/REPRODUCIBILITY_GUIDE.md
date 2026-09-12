# Reproducibility Guide — PQR Market Intelligence Lab

## 1. Recommended Google Drive structure

Create the following folders under `MyDrive`:

```text
global-health-market-access/
├── data/
│   └── raw/
│       ├── global_fund/
│       │   ├── pqr_transactions_2003_2026_ml_ready.csv
│       │   ├── pqr_current_medicines_by_country.csv
│       │   └── pqr_current_diagnostics_by_country.csv
│       ├── world_bank/
│       │   └── world_bank_country_metadata.json
│       └── who/
│           └── who_prequalified_finished_products.csv
├── documentation/
│   └── psm_pqrdatacaveats_note_en.pdf
├── notebooks/
│   └── PQR_Market_Intelligence_Lab.ipynb
├── reports/
│   └── PQR_Market_Intelligence_Lab.html
└── outputs/
```

Only `pqr_transactions_2003_2026_ml_ready.csv` is required to run the core analysis. The other files provide enrichment and provenance.

## 2. Upload the files

Use the files from `Global_Fund_PQR_Project_1_Data_2003_2026.zip`:

- Move `global_fund/derived/pqr_transactions_2003_2026_ml_ready.csv` to `data/raw/global_fund/`.
- Move the two files under `global_fund/price_reference/` to `data/raw/global_fund/`.
- Move `documentation/psm_pqrdatacaveats_note_en.pdf` to `documentation/`.

Use the files from `Project_1_Market_Access_Source_Data_2026-09-11.zip`:

- Move `world_bank/world_bank_country_metadata.json` to `data/raw/world_bank/`.
- Move `who_prequalification/who_prequalified_finished_products.csv` to `data/raw/who/`.

The notebook searches recursively below the project root, so the analysis will still find files in deeper subfolders if filenames remain unchanged.

## 3. Run in Google Colab

1. Upload `PQR_Market_Intelligence_Lab.ipynb` to `notebooks/` in Google Drive.
2. Right-click the notebook and select **Open with → Google Colaboratory**.
3. In the path-configuration cell, set:

```python
USE_GOOGLE_DRIVE = True
DRIVE_PROJECT_ROOT = Path('/content/drive/MyDrive/global-health-market-access')
PROJECT_ROOT_OVERRIDE = None
```

4. Select **Runtime → Restart session and run all**.
5. Approve the standard Google Drive mount request.
6. Confirm that the asset table shows the required PQR file as resolved.
7. Confirm that the final green box says **Run completed successfully**.

## 4. Outputs created by the notebook

The notebook writes the following files to:

```text
outputs/pqr_market_intelligence/
```

- `high_price_review_signals_2024_2025.csv`
- `country_product_monitoring_2024_2025.csv`
- `manufacturer_concentration_recent.csv`
- `model_test_metrics.csv`
- `permutation_importance.csv`
- `run_manifest.json`

The review-signal file must be treated as a screening queue. It is not evidence of overpricing, misconduct or achievable savings.

## 5. Recreate the HTML report

After running every cell in Colab:

1. Select **File → Download → Download .ipynb** to retain the executed notebook.
2. Select **File → Print** and save as PDF if a fixed report is needed.
3. For HTML, run this final optional Colab command:

```python
!jupyter nbconvert --to html "/content/drive/MyDrive/global-health-market-access/notebooks/PQR_Market_Intelligence_Lab.ipynb" \
  --output "/content/drive/MyDrive/global-health-market-access/reports/PQR_Market_Intelligence_Lab.html" \
  --HTMLExporter.exclude_input_prompt=True \
  --HTMLExporter.exclude_output_prompt=True
```

If the notebook was opened from Drive, save the completed notebook back to Drive before conversion so the HTML contains the latest outputs.

## 6. Reproducibility controls

- Random seed is fixed at 42.
- Training ends in 2022.
- Model selection uses 2023 only.
- 2024–2025 remains untouched until final evaluation.
- 2026 is excluded because it is incomplete as of 11 September 2026.
- Validation residuals determine review thresholds.
- Identifiers, invoices, delivery dates and total product cost are excluded from prediction.
- `run_manifest.json` records source location, sample sizes, chosen parameters, thresholds and software versions.

## 7. Recommended GitHub handling

Do not commit large raw datasets directly unless their licensing and GitHub size limits permit it. Commit:

- Notebook and HTML report
- Documentation
- Data dictionary and source register
- Small derived summary files
- A `data/README.md` containing download instructions and checksums

Add raw files to `.gitignore` and provide authoritative Global Fund source URLs in the repository README.

## 8. Interpretation safeguards

Before investigating any review signal, verify the source transaction and compare product specification, pack, freight treatment, quality status, procurement channel, payment conditions, urgency, lead time, market availability and local regulatory constraints. Never present the model output as proof of inefficient purchasing or supplier conduct.
