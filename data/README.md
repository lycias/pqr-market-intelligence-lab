# Data access

Large raw and derived transaction files are intentionally excluded from GitHub. This keeps the repository lightweight and avoids redistributing source data without its accompanying caveats.

## Authoritative Global Fund sources

- [PQR Price Reference Report](https://insights.theglobalfund.org/t/Public/views/PriceQualityReportingPriceReferenceReport/Countries?iframeSizedToWindow=true&%3Aembed=y&%3AshowAppBanner=false&%3Adisplay_count=no&%3AshowVizHome=no)
- [PQR Transaction Summary](https://insights.theglobalfund.org/t/Public/views/PriceQualityReportingTransactionSummary/TransactionSummary?iframeSizedToWindow=true&%3Aembed=y&%3AshowAppBanner=false&%3Adisplay_count=no&%3AshowVizHome=no)
- [Official PQR data caveats note](https://www.theglobalfund.org/media/5871/psm_pqrdatacaveats_note_en.pdf)

## Expected local/Drive structure

```text
global-health-market-access/
└── data/raw/
    ├── global_fund/
    │   ├── pqr_transactions_2003_2026_ml_ready.csv
    │   ├── pqr_current_medicines_by_country.csv
    │   └── pqr_current_diagnostics_by_country.csv
    ├── world_bank/
    │   └── world_bank_country_metadata.json
    └── who/
        └── who_prequalified_finished_products.csv
```

Only `pqr_transactions_2003_2026_ml_ready.csv` is required for the core analysis. The other assets support enrichment and provenance. Keep filenames unchanged because the notebook resolves them recursively.

## Data limitations

Read the official caveats note before interpretation. The 2026 extract was incomplete as of 11 September 2026 and is not used as a complete annual period. Review signals must be validated against source transactions and procurement context.
