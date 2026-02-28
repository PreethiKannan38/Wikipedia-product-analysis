import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def vader_sentiment(df, text_col="text"):
    """run vader sentiment on a text column, returns df with scores added."""
    analyzer = SentimentIntensityAnalyzer()
    df = df.copy()

    # combine title + text for better signal
    if "title" in df.columns:
        df["combined_text"] = df["title"].fillna("") + " " + df[text_col].fillna("")
    else:
        df["combined_text"] = df[text_col].fillna("")

    scores = df["combined_text"].apply(lambda x: analyzer.polarity_scores(str(x)))
    df["vader_compound"] = scores.apply(lambda x: x["compound"])
    df["vader_pos"] = scores.apply(lambda x: x["pos"])
    df["vader_neg"] = scores.apply(lambda x: x["neg"])
    df["vader_neu"] = scores.apply(lambda x: x["neu"])

    # classify as positive / negative / neutral
    df["vader_label"] = df["vader_compound"].apply(
        lambda x: "positive" if x >= 0.05 else ("negative" if x <= -0.05 else "neutral")
    )
    return df


def roberta_sentiment(df, text_col="text", batch_size=32):
    """run huggingface roberta sentiment model on text column.
    uses cardiffnlp twitter-roberta for social media text."""
    from transformers import pipeline

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
        max_length=512,
        truncation=True
    )

    df = df.copy()

    # combine title + text
    if "title" in df.columns:
        texts = (df["title"].fillna("") + " " + df[text_col].fillna("")).tolist()
    else:
        texts = df[text_col].fillna("").tolist()

    # truncate long texts to avoid tokenizer issues
    texts = [t[:500] if len(t) > 500 else t for t in texts]

    # run in batches
    all_results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        results = sentiment_pipeline(batch)
        all_results.extend(results)

    df["roberta_label"] = [r["label"].lower() for r in all_results]
    df["roberta_score"] = [r["score"] for r in all_results]

    # map labels to numeric for trend analysis
    label_map = {"positive": 1, "neutral": 0, "negative": -1}
    df["roberta_numeric"] = df["roberta_label"].map(label_map).fillna(0)

    return df


def aggregate_sentiment_by_month(df, date_col="date"):
    """group sentiment scores by month for time series plotting."""
    df = df.copy()
    df["month"] = pd.to_datetime(df[date_col]).dt.to_period("M")

    agg = df.groupby("month").agg(
        vader_mean=("vader_compound", "mean"),
        post_count=("vader_compound", "count"),
        positive_pct=("vader_label", lambda x: (x == "positive").mean() * 100),
        negative_pct=("vader_label", lambda x: (x == "negative").mean() * 100)
    ).reset_index()

    # add roberta if it exists
    if "roberta_numeric" in df.columns:
        roberta_agg = df.groupby("month").agg(
            roberta_mean=("roberta_numeric", "mean"),
            roberta_positive_pct=("roberta_label", lambda x: (x == "positive").mean() * 100),
            roberta_negative_pct=("roberta_label", lambda x: (x == "negative").mean() * 100)
        ).reset_index()
        agg = agg.merge(roberta_agg, on="month")

    agg["month"] = agg["month"].dt.to_timestamp()
    return agg
