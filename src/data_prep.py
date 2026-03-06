import pandas as pd

def clean_pageview_data(df):
    if df is None or df.empty:
        return None
    df = df.copy()
    df = df.dropna()
    df["views"] = df["views"].astype(int)
    return df

def aggregate_data(df, frequency="M"):
    df = df.set_index("timestamp")
    agg_df = df.resample(frequency).sum()
    return agg_df.reset_index()

def add_time_features(df, date_col="timestamp"):
    df = df.copy()
    col = pd.to_datetime(df[date_col])
    df["day_of_week"] = col.dt.day_name()
    df["month_name"] = col.dt.month_name()
    df["year"] = col.dt.year
    df["is_weekend"] = col.dt.dayofweek >= 5
    return df

def clean_reddit_data(df):
    """deduplicate, filter out deleted/removed posts, add basic text features."""
    if df is None or df.empty:
        return df
    df = df.copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    # deduplicate by post id
    if "id" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset="id")
        removed = before - len(df)
        if removed > 0:
            print(f"  removed {removed} duplicate posts")

    # drop deleted/removed posts
    if "text" in df.columns:
        mask = df["text"].isin(["[deleted]", "[removed]", ""])
        df.loc[mask, "text"] = None

    # add title word count as a feature
    if "title" in df.columns:
        df["title_word_count"] = df["title"].fillna("").apply(lambda x: len(str(x).split()))

    # combined text for sentiment (title + body)
    if "title" in df.columns and "text" in df.columns:
        df["combined_text"] = df["title"].fillna("") + " " + df["text"].fillna("")
        df["combined_text"] = df["combined_text"].str.strip()

    return df

def add_pre_post_chatgpt(df, date_col="date"):
    df = df.copy()
    chatgpt_launch = pd.Timestamp("2022-11-30")
    if date_col in df.columns:
        df["period"] = (
            pd.to_datetime(df[date_col])
            .apply(lambda x: "post-ChatGPT" if pd.notnull(x) and x >= chatgpt_launch else "pre-ChatGPT")
        )
    return df

def flag_low_count_months(df, count_col="post_count", threshold=10):
    """adds a reliable column so low-sample months can be filtered out in plots."""
    df = df.copy()
    df["reliable"] = df[count_col] >= threshold
    return df
