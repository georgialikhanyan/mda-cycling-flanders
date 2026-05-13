"""
data_loader.py
Reusable functions for loading and merging AWV fietstellingen data.
Used by notebooks to avoid code duplication.
"""
import pandas as pd
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

RAW_DIR    = Path("data/raw")
COUNTS_DIR = RAW_DIR / "counts"
PROC_DIR   = Path("data/processed")


def load_sites(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Load and clean sites.csv metadata."""
    df = pd.read_csv(raw_dir / "sites.csv", sep=";")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def load_richtingen(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Load and clean richtingen.csv metadata."""
    df = pd.read_csv(raw_dir / "richtingen.csv", sep=";")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def load_counts(counts_dir: Path = COUNTS_DIR,
                type_filter: str = "FIETSERS") -> pd.DataFrame:
    """
    Load all monthly count CSVs and return a concatenated DataFrame.
    Filters to type_filter (default: FIETSERS = cyclists).
    """
    files = sorted(counts_dir.glob("data-*.csv"))
    if not files:
        raise FileNotFoundError(
            f"No count files found in {counts_dir}. "
            "Run download_data.py first."
        )

    chunks = []
    for fp in files:
        try:
            df = pd.read_csv(fp, sep=";", low_memory=False)
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            if type_filter:
                df = df[df["type"].str.upper() == type_filter.upper()]
            chunks.append(df)
        except Exception as e:
            print(f"Warning: could not read {fp.name}: {e}")

    counts = pd.concat(chunks, ignore_index=True)
    counts["van"] = pd.to_datetime(counts["van"], errors="coerce")
    counts["tot"] = pd.to_datetime(counts["tot"], errors="coerce")
    counts["aantal"] = pd.to_numeric(counts["aantal"], errors="coerce")
    counts.dropna(subset=["van", "tot", "aantal"], inplace=True)
    counts = counts[counts["aantal"] >= 0]
    counts.drop_duplicates(subset=["site_id", "richting", "van"], inplace=True)
    return counts


def load_processed(proc_dir: Path = PROC_DIR,
                   filename: str = "cyclists_clean.parquet") -> pd.DataFrame:
    """Load the cleaned processed parquet file."""
    path = proc_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run 01_data_loading.ipynb first."
        )
    return pd.read_parquet(path)
