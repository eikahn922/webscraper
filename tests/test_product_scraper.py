import argparse
import csv
import tempfile
import unittest
from pathlib import Path

import product_scraper


class ProductScraperTests(unittest.TestCase):
    def test_no_web_enrichment_preserves_existing_products(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "vendors.csv"
            input_path.write_text(
                "Vendor,Product,Email\n"
                "MavenIT,,ops@mavenit.com\n"
                "Already Known,existing product,known@example.com\n",
                encoding="utf-8",
            )

            args = make_args(input_path, no_web=True)
            rows, headers = product_scraper.enrich_rows(args)

        self.assertEqual(
            headers[:6],
            [
                "Vendor",
                "Product",
                "Product Source URL",
                "Product Confidence",
                "Scrape Status",
                "Scrape Notes",
            ],
        )
        self.assertEqual(rows[0]["Product"], "IT support services")
        self.assertEqual(rows[0]["Product Confidence"], "low")
        self.assertEqual(rows[0]["Scrape Status"], "filled_from_company_name")
        self.assertEqual(rows[1]["Product"], "existing product")
        self.assertEqual(rows[1]["Scrape Status"], "already_had_product")

    def test_overwrite_replaces_existing_product(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "vendors.csv"
            input_path.write_text(
                "Vendor,Product\nMavenIT,old value\n",
                encoding="utf-8",
            )

            rows, _headers = product_scraper.enrich_rows(
                make_args(input_path, no_web=True, overwrite=True)
            )

        self.assertEqual(rows[0]["Product"], "IT support services")
        self.assertEqual(rows[0]["Scrape Status"], "filled_from_company_name")

    def test_page_summary_prefers_specific_service_copy(self) -> None:
        parser = product_scraper.parse_page(
            "<html><head><meta name='description' "
            "content='We provide commercial plumbing installation and repair.'>"
            "</head><body><h1>Acme Plumbing</h1></body></html>"
        )

        summary = product_scraper.products_from_page("Acme Plumbing", parser)

        self.assertEqual(summary, "commercial plumbing installation and repair")

    def test_write_csv_keeps_header_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "result.csv"
            product_scraper.write_csv(
                [{"Vendor": "MavenIT", "Product": "IT support services"}],
                ["Vendor", "Product"],
                output_path,
            )
            with output_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))

        self.assertEqual(rows, [["Vendor", "Product"], ["MavenIT", "IT support services"]])


def make_args(input_path: Path, **overrides: object) -> argparse.Namespace:
    args = product_scraper.parse_args([str(input_path), "--cache", ""])
    for name, value in overrides.items():
        setattr(args, name, value)
    return args


if __name__ == "__main__":
    unittest.main()
