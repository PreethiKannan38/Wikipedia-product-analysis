import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def vader_sentiment(df, text_col="combined_text"):
    """run vader on combined_text. adds compound score, component scores, and label.
    vader is rule-based so it runs instantly and needs no GPU."""
    analyzer = SentimentIntensityAnalyzer()
    df = df.copy()

    if text_col not in df.columns:
        if "title" in df.columns and "text" in df.columns:
            df["combined_text"] = df["title"].fillna("") + " " + df["text"].fillna("")
            text_col = "combined_text"
        else:
            raise ValueError(f"column '{text_col}' not found and cannot build combined_text")

    scores = df[text_col].apply(lambda x: analyzer.polarity_scores(str(x)))
    df["vader_compound"] = scores.apply(lambda x: x["compound"])
    df["vader_pos"]      = scores.apply(lambda x: x["pos"])
    df["vader_neg"]      = scores.apply(lambda x: x["neg"])
    df["vader_neu"]      = scores.apply(lambda x: x["neu"])
    df["vader_label"]    = df["vader_compound"].apply(
        lambda x: "positive" if x >= 0.05 else ("negative" if x <= -0.05 else "neutral")
    )
    return df


def roberta_sentiment(df, text_col="combined_text", batch_size=32, max_chars=512):
    """run cardiffnlp/twitter-roberta-base-sentiment-latest on text.
    returns the top-1 label + confidence score + all 3 class probabilities.
    getting all 3 probabilities lets us compute a continuous sentiment score
    instead of just a 3-class label, which is much more useful for trend analysis."""
    from transformers import pipeline as hf_pipeline

    pipe = hf_pipeline(
        "text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
        max_length=512,
        truncation=True,
        top_k=None
    )

    df = df.copy()

    if text_col not in df.columns:
        if "title" in df.columns and "text" in df.columns:
            df["combined_text"] = df["title"].fillna("") + " " + df["text"].fillna("")
            text_col = "combined_text"
        else:
            raise ValueError(f"column '{text_col}' not found")

    texts = df[text_col].fillna("").tolist()
    texts = [str(t)[:max_chars] for t in texts]

    all_results = []
    n_batches = (len(texts) + batch_size - 1) // batch_size
    for i in range(0, len(texts), batch_size):
        batch_num = i // batch_size + 1
        print(f"  batch {batch_num}/{n_batches}...", end="\r")
        batch = texts[i:i + batch_size]
        results = pipe(batch)
        all_results.extend(results)
    print(f"  done. {len(all_results)} posts scored.          ")

    label_map = {"positive": 1, "neutral": 0, "negative": -1}

    rows = []
    for result in all_results:
        score_dict = {r["label"].lower(): r["score"] for r in result}
        top_label = max(score_dict, key=score_dict.get)
        rows.append({
            "roberta_label":      top_label,
            "roberta_score":      score_dict[top_label],
            "roberta_pos":        score_dict.get("positive", 0),
            "roberta_neu":        score_dict.get("neutral", 0),
            "roberta_neg":        score_dict.get("negative", 0),
            "roberta_numeric":    label_map[top_label],
            "roberta_continuous": (
                score_dict.get("positive", 0) * 1
                + score_dict.get("neutral",  0) * 0
                + score_dict.get("negative", 0) * -1
            ),
        })

    result_df = pd.DataFrame(rows)
    for col in result_df.columns:
        df[col] = result_df[col].values

    return df


def flag_sentiment_quality(df, confidence_threshold=0.65, min_chars=10):
    """adds two quality flags:
    - high_confidence: roberta_score >= threshold
    - has_body: post has a real body beyond just a title
    low-confidence predictions are more likely to be wrong and worth tracking separately."""
    df = df.copy()
    df["high_confidence"] = df["roberta_score"] >= confidence_threshold
    if "text" in df.columns:
        df["has_body"] = df["text"].notna() & (df["text"].str.len() >= min_chars)
    return df


def compute_agreement(df):
    """adds vader_roberta_agree and disagreement_type columns."""
    df = df.copy()
    df["vader_roberta_agree"] = df["vader_label"] == df["roberta_label"]
    df["disagreement_type"] = df.apply(
        lambda r: f"vader={r['vader_label']}, roberta={r['roberta_label']}"
        if not r["vader_roberta_agree"] else "agree",
        axis=1
    )
    return df


def get_disagreement_summary(df):
    """prints and returns a breakdown of where vader and roberta disagree."""
    total = len(df)
    agree = df["vader_roberta_agree"].sum()
    disagree_df = df[~df["vader_roberta_agree"]]
    breakdown = disagree_df.groupby(["vader_label", "roberta_label"]).size().reset_index(name="count")
    breakdown["pct_of_total"] = (breakdown["count"] / total * 100).round(1)
    breakdown = breakdown.sort_values("count", ascending=False)
    print(f"agreement rate: {agree}/{total} = {agree/total*100:.1f}%")
    print("disagreement breakdown:")
    print(breakdown.to_string(index=False))
    return breakdown


def aggregate_sentiment_by_month(df, date_col="date", min_posts=10):
    """aggregate to monthly level. months below min_posts are flagged unreliable.
    uses roberta_continuous mean as the primary trend metric because it captures
    more signal than averaging the 3-class numeric labels."""
    df = df.copy()
    df["month"] = pd.to_datetime(df[date_col]).dt.to_period("M")

    agg_cols = {
        "post_count":    ("roberta_label",    "count"),
        "roberta_mean":  ("roberta_numeric",  "mean"),
        "vader_mean":    ("vader_compound",   "mean"),
        "positive_pct":  ("roberta_label",    lambda x: (x == "positive").mean() * 100),
        "negative_pct":  ("roberta_label",    lambda x: (x == "negative").mean() * 100),
        "neutral_pct":   ("roberta_label",    lambda x: (x == "neutral").mean()   * 100),
    }

    if "roberta_continuous" in df.columns:
        agg_cols["roberta_continuous_mean"] = ("roberta_continuous", "mean")

    agg = df.groupby("month").agg(**agg_cols).reset_index()
    agg["month"]    = agg["month"].dt.to_timestamp()
    agg["reliable"] = agg["post_count"] >= min_posts
    return agg
