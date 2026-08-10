# Dogwood vendor product lookup

Fill blank product or service cells in the Dogwood vendor list from vendors’ public web pages. The source file stays untouched; the script writes a new review file with the source and confidence for every guess.

## Review columns

| Column | What it records |
| --- | --- |
| `Products` | Extracted or inferred product/service description |
| `Product Source URL` | Public page used for the description |
| `Product Confidence` | `medium`, `low`, or `none` |
| `Scrape Status` | Whether the value came from the web, the company name, or was skipped |
| `Scrape Notes` | Fetch errors or the reason a row was not filled |

Existing product values are left alone unless `--overwrite` is supplied. Treat every new value as a draft: the scraper uses text heuristics, not a vendor catalog API.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the Dogwood list

Keep the source PDF outside this repository because it contains private contact details.

```bash
python product_scraper.py \
  "/Users/ezrakahn/Downloads/Master Product List.xlsx - Vendor Contact Numbers.pdf" \
  --output output/dogwood_enriched.csv \
  --xlsx-output output/dogwood_enriched.xlsx
```

Inputs may be PDF tables, `.xlsx`/`.xlsm` workbooks, or CSV files. CSV output is always written; `--xlsx-output` adds a formatted workbook.

## Common passes

Check five missing rows before running the whole file:

```bash
python product_scraper.py path/to/vendors.pdf --limit 5
```

Avoid all network requests and infer only from company/contact names:

```bash
python product_scraper.py path/to/vendors.pdf --no-web
```

Name the columns when automatic header detection picks the wrong fields:

```bash
python product_scraper.py path/to/vendors.xlsx \
  --company-column "Vendor" \
  --product-column "Product"
```

Replace existing product values instead of filling blanks only:

```bash
python product_scraper.py path/to/vendors.xlsx --overwrite
```

HTTP results are cached in `.scrape_cache.json`. Pass `--cache ''` for a run that should neither read nor write the cache.

## Tests

The test suite uses local HTML and CSV fixtures; it does not make web requests.

```bash
python -m unittest discover -s tests -v
```
