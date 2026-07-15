# Webscraper for Dogwood

Python scraper for filling missing product/service fields in vendor lists.

It can read:

- PDF tables exported from Excel
- Excel workbooks (`.xlsx`, `.xlsm`)
- CSV files

It writes an enriched CSV, and optionally an Excel workbook, with these audit columns:

- `Products`
- `Product Source URL`
- `Product Confidence`
- `Scrape Status`
- `Scrape Notes`

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run on the Dogwood vendor PDF

Keep the PDF outside the git repo because it contains private contact details.

```bash
python product_scraper.py \
  "/Users/ezrakahn/Downloads/Master Product List.xlsx - Vendor Contact Numbers.pdf" \
  --output output/dogwood_enriched.csv \
  --xlsx-output output/dogwood_enriched.xlsx
```

## Useful options

Fill only a few rows while testing:

```bash
python product_scraper.py path/to/vendors.pdf --limit 5
```

Run without web requests and infer from company names only:

```bash
python product_scraper.py path/to/vendors.pdf --no-web
```

Use explicit column names when the script cannot detect them:

```bash
python product_scraper.py path/to/vendors.xlsx \
  --company-column "Vendor" \
  --product-column "Product"
```

Overwrite existing product values:

```bash
python product_scraper.py path/to/vendors.xlsx --overwrite
```

## Notes

This scraper uses public web pages and simple heuristics, so every result should be treated as a draft until reviewed. The `Product Source URL`, `Product Confidence`, and `Scrape Notes` columns are there to make that review fast.
