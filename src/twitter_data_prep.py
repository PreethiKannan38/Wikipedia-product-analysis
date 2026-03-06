"""
twitter_data_prep.py
---------------------
Cleaning, feature engineering, and aggregation utilities for Twitter data.
Mirrors data_prep.py's style for consistent project structure.
"""

import re
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def _remove_urls(text: str) -> str:
    return re.sub(r"http\S+|www\.\S+", "", text)

def _remove_mentions(text: str) -> str:
    return re.sub(r"@\w+", "", text)

def _remove_hashtags_text(text: str) -> str:
    """Remove the # symbol but keep the word."""
    return re.sub(r"#(\w+)", r"\1", text)

def _remove_rt(text: str) -> str:
    return re.sub(r"^RT\s+", "", text)

def clean_tweet_text(text: str) -> str:
    """Full cleaning pipeline for ML/sentiment use (keeps words, removes noise)."""
    if not isinstance(text, str):
        return ""
    text = _remove_rt(text)
    text = _remove_urls(text)
    text = _remove_mentions(text)
    text = _remove_hashtags_text(text)
    text = re.sub(r"[^\w\s'!?.,]", " ", text)   # keep basic punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_hashtags(text: str) -> list:
    """Return list of hashtags found in raw tweet text."""
    if not isinstance(text, str):
        return []
    return [h.lower() for h in re.findall(r"#(\w+)", text)]

def extract_mentions(text: str) -> list:
    if not isinstance(text, str):
        return []
    return [m.lower() for m in re.findall(r"@(\w+)", text)]


# ---------------------------------------------------------------------------
# Main cleaning function
# ---------------------------------------------------------------------------

def clean_twitter_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline for raw Twitter DataFrame.

    Steps:
    1. Parse & filter dates (>= 2020-01-01)
    2. Drop duplicates by tweet id
    3. Drop empty / RT-only tweets
    4. Add cleaned_text column (for ML/sentiment)
    5. Add hashtags and mentions lists
    6. Add word_count and char_count
    7. Add is_retweet flag
    8. Coerce engagement columns to int

    Returns a clean pd.DataFrame.
    """
    if df is None or df.empty:
        return df
    df = df.copy()

    # --- dates ---
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.tz_localize(None)          # remove tz for easier handling
    df = df[df["date"] >= "2020-01-01"].reset_index(drop=True)

    # --- dedup ---
    before = len(df)
    df = df.drop_duplicates(subset="id").reset_index(drop=True)
    print(f"  dedup: {before} → {len(df)} tweets")

    # --- engagement coercion ---
    for col in ["likes", "retweets", "replies"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        else:
            df[col] = 0

    # --- retweet flag ---
    df["is_retweet"] = df["text"].str.startswith("RT ", na=False)

    # --- cleaned text ---
    df["cleaned_text"] = df["text"].apply(clean_tweet_text)

    # --- drop tweets with no usable text ---
    df = df[df["cleaned_text"].str.len() > 5].reset_index(drop=True)

    # --- feature extraction ---
    df["hashtags"]   = df["text"].apply(extract_hashtags)
    df["mentions"]   = df["text"].apply(extract_mentions)
    df["word_count"] = df["cleaned_text"].apply(lambda x: len(str(x).split()))
    df["char_count"] = df["cleaned_text"].apply(len)

    print(f"  final clean shape: {df.shape}")
    return df


# ---------------------------------------------------------------------------
# Engagement features
# ---------------------------------------------------------------------------

def add_engagement_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived engagement columns:
    - total_engagement = likes + retweets + replies
    - engagement_tier: 'viral' / 'high' / 'medium' / 'low'
    """
    df = df.copy()
    # Ensure columns exist
    for col in ["likes", "retweets", "replies"]:
        if col not in df.columns:
            df[col] = 0
    df["total_engagement"] = df["likes"] + df["retweets"] + df["replies"]

    q75 = df["total_engagement"].quantile(0.75)
    q90 = df["total_engagement"].quantile(0.90)
    q99 = df["total_engagement"].quantile(0.99)

    def _tier(v):
        if v >= q99:
            return "viral"
        elif v >= q90:
            return "high"
        elif v >= q75:
            return "medium"
        return "low"

    df["engagement_tier"] = df["total_engagement"].apply(_tier)
    return df


# ---------------------------------------------------------------------------
# Time features
# ---------------------------------------------------------------------------

def add_time_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Add year, month, day_of_week, hour, is_weekend columns."""
    df = df.copy()
    col = pd.to_datetime(df[date_col])
    df["year"]        = col.dt.year
    df["month"]       = col.dt.month
    df["month_name"]  = col.dt.month_name()
    df["day_of_week"] = col.dt.day_name()
    df["hour"]        = col.dt.hour
    df["is_weekend"]  = col.dt.dayofweek >= 5
    return df


# ---------------------------------------------------------------------------
# Pre/post ChatGPT period (mirrors reddit data_prep.py)
# ---------------------------------------------------------------------------

def add_pre_post_chatgpt(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Flag tweets as 'pre-ChatGPT' or 'post-ChatGPT' (launch: 2022-11-30)."""
    df = df.copy()
    launch = pd.Timestamp("2022-11-30")
    df["period"] = pd.to_datetime(df[date_col]).apply(
        lambda x: "post-ChatGPT" if pd.notnull(x) and x >= launch else "pre-ChatGPT"
    )
    return df


# ---------------------------------------------------------------------------
# Monthly aggregation
# ---------------------------------------------------------------------------

def aggregate_by_month(df: pd.DataFrame, date_col: str = "date",
                       min_tweets: int = 10) -> pd.DataFrame:
    """
    Aggregate tweet-level data to monthly level.
    Returns: month, tweet_count, avg_likes, avg_retweets,
             avg_engagement, reliable (bool)
    """
    df = df.copy()
    df["month"] = pd.to_datetime(df[date_col]).dt.to_period("M")
    agg = df.groupby("month").agg(
        tweet_count    =("id",              "count"),
        avg_likes      =("likes",           "mean"),
        avg_retweets   =("retweets",        "mean"),
        avg_replies    =("replies",         "mean"),
        avg_engagement =("total_engagement","mean"),
    ).reset_index()
    agg["month"] = agg["month"].dt.to_timestamp()
    agg["reliable"] = agg["tweet_count"] >= min_tweets
    return agg
