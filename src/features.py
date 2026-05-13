"""
features.py
Temporal and site-level feature engineering utilities.
"""
import pandas as pd
import numpy as np
import holidays


def add_temporal_features(df: pd.DataFrame,
                           dt_col: str = "van") -> pd.DataFrame:
    """Add hour, day_of_week, month, year, season, is_weekend, is_holiday."""
    be_holidays = holidays.Belgium(years=range(
        df[dt_col].dt.year.min(), df[dt_col].dt.year.max() + 1
    ))

    df = df.copy()
    df["hour"]        = df[dt_col].dt.hour
    df["day_of_week"] = df[dt_col].dt.dayofweek
    df["day_name"]    = df[dt_col].dt.day_name()
    df["month"]       = df[dt_col].dt.month
    df["year"]        = df[dt_col].dt.year
    df["date"]        = df[dt_col].dt.date
    df["is_weekend"]  = df["day_of_week"].isin([5, 6]).astype(int)
    df["is_holiday"]  = df["date"].astype(str).map(
        lambda d: 1 if d in be_holidays else 0
    )

    season_map = {12:"Winter", 1:"Winter", 2:"Winter",
                  3:"Spring",  4:"Spring",  5:"Spring",
                  6:"Summer",  7:"Summer",  8:"Summer",
                  9:"Autumn",  10:"Autumn", 11:"Autumn"}
    df["season"] = df["month"].map(season_map)
    return df


def add_rolling_average(df: pd.DataFrame,
                         group_col: str = "site_id",
                         value_col: str = "aantal",
                         window: int = 7 * 24) -> pd.DataFrame:
    """Add a rolling average column per group."""
    df = df.sort_values([group_col, "van"]).copy()
    df["rolling_7d_avg"] = (
        df.groupby(group_col)[value_col]
        .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
    )
    return df


def build_site_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a 168-dimensional traffic profile per site
    (average count per hour-of-week: 24h x 7 days).
    Returns a DataFrame indexed by site_id with 168 feature columns.
    """
    df = df.copy()
    df["hour_of_week"] = df["day_of_week"] * 24 + df["hour"]
    pivot = (
        df.groupby(["site_id", "hour_of_week"])["aantal"]
        .mean()
        .unstack("hour_of_week")
        .fillna(0)
    )
    pivot.columns = [f"h{c:03d}" for c in pivot.columns]
    return pivot
