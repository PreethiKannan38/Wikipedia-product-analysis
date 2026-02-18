import pandas as pd

def clean_pageview_data(df):
    """basic cleaning on pageview dataframe."""
    if df is None or df.empty:
        return None
    df = df.copy()
    df = df.dropna()
    df["views"] = df["views"].astype(int)
    return df

def aggregate_data(df, frequency="W"):
    """
    Aggregates pageview data to a given frequency.
    Args:
        df (pd.DataFrame): Dataframe with 'timestamp' and 'views'
        frequency (str): Pandas offset alias (e.g., 'W' for weekly, 'M' for monthly)
    Returns:
        pd.DataFrame: Aggregated data.
    """
    df = df.set_index("timestamp")
    agg_df = df.resample(frequency).sum()
    return agg_df.reset_index()

def add_time_features(df):
    """Adds day of week, month, and year features for seasonality analysis."""
    df = df.copy()
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["month"] = df["timestamp"].dt.month_name()
    df["year"] = df["timestamp"].dt.year
    df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5
    return df
