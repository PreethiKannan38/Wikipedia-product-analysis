import pandas as pd
import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath('.'))
from src.api_client import WikipediaAPIClient

TOPIC_CLUSTERS = {
    "education": [
        "Calculus",
        "Derivative",
        "Integral",
        "Photosynthesis",
        "Cell_(biology)",
        "Newton's_laws_of_motion",
        "World_War_II",
        "French_Revolution",
        "Periodic_table",
        "Pythagorean_theorem"
    ],
    "politics": [
        "Democracy",
        "United_Nations",
        "European_Parliament",
        "NATO",
        "United_States_Congress",
        "President_of_the_United_States",
        "Human_rights",
        "Constitution",
        "Cold_War",
        "Geopolitics"
    ],
    "entertainment": [
        "Marvel_Cinematic_Universe",
        "Star_Wars",
        "Game_of_Thrones",
        "House_of_the_Dragon",
        "Avatar_(film)",
        "Taylor_Swift",
        "Beyoncé",
        "Harry_Potter",
        "Netflix",
        "Disney+"
    ]
}

def fetch_topic_data(start_date="20150701", end_date="20250301"):
    client = WikipediaAPIClient()
    output_dir = "data/raw/topics"
    os.makedirs(output_dir, exist_ok=True)

    all_data = []

    for cluster, articles in TOPIC_CLUSTERS.items():
        print(f"Fetching data for cluster: {cluster}")
        for article in articles:
            print(f"  Article: {article}")
            df = client.get_article_pageviews("en.wikipedia.org", article, start_date, end_date)
            if df is not None:
                df['article'] = article
                df['cluster'] = cluster
                all_data.append(df)
            else:
                print(f"    Warning: Failed to fetch data for {article}")
            # Rate limiting as per Wikimedia best practices
            time.sleep(0.1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        output_path = "data/raw/en_wiki_topic_pageviews_daily.csv"
        final_df.to_csv(output_path, index=False)
        print(f"Saved all topic data to {output_path}")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    # For speed during development, we might use a shorter window if needed,
    # but the task asks for the full range.
    # Note: 20150701 is the start of modern Pageviews API.
    fetch_topic_data()
