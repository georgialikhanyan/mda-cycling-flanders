"""
download_data.py
AWV Fietstellingen — automatic data downloader for the MDA cycling project.
Downloads: sites.csv, richtingen.csv, and monthly count CSVs (2020–2025).
Usage: python download_data.py
"""

import os
import time
import requests
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_URL = "https://opendata.apps.mow.vlaanderen.be/fietstellingen"
DATA_DIR = Path("data/raw")
COUNTS_DIR = DATA_DIR / "counts"
START_YEAR = 2020
END_YEAR = 2025

METADATA_FILES = ["sites.csv", "richtingen.csv"]

# ── Helpers ────────────────────────────────────────────────────────────────────
def download_file(url: str, dest: Path, overwrite: bool = False) -> bool:
    """Download a file from url to dest. Returns True on success."""
    if dest.exists() and not overwrite:
        print(f"  [skip] {dest.name} already exists.")
        return True

    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        size_kb = dest.stat().st_size / 1024
        print(f"  [ok]   {dest.name}  ({size_kb:.1f} KB)")
        return True
    except requests.HTTPError as e:
        print(f"  [404]  {dest.name} not available ({e})")
        return False
    except Exception as e:
        print(f"  [err]  {dest.name} failed: {e}")
        return False


def generate_monthly_urls(start_year: int, end_year: int):
    """Yield (url, filename) tuples for every month from start to end (inclusive)."""
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            filename = f"data-{year}-{month:02d}.csv"
            url = f"{BASE_URL}/{filename}"
            yield url, filename


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  AWV Fietstellingen — Data Downloader")
    print("=" * 60)

    # 1. Metadata files
    print("\n[1/2] Downloading metadata files …")
    for fname in METADATA_FILES:
        url = f"{BASE_URL}/{fname}"
        download_file(url, DATA_DIR / fname)

    # 2. Monthly count files
    print(f"\n[2/2] Downloading monthly counts ({START_YEAR}–{END_YEAR}) …")
    success, skipped, failed = 0, 0, 0

    for url, filename in generate_monthly_urls(START_YEAR, END_YEAR):
        dest = COUNTS_DIR / filename
        if dest.exists():
            print(f"  [skip] {filename} already exists.")
            skipped += 1
            continue
        ok = download_file(url, dest)
        if ok:
            success += 1
        else:
            failed += 1
        time.sleep(0.3)  # be polite to the server

    # Summary
    print("\n" + "=" * 60)
    print(f"  Done!  Downloaded: {success}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"  Data saved to: {DATA_DIR.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
