import sys
import os
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath('.'))
from src.api_client import WikipediaAPIClient

def fetch_daily_data():
    client = WikipediaAPIClient()
    project = "en.wikipedia.org"
    start_date = "20150701"
    end_date = "20251201"
    
    print(f"Fetching daily pageview data for {project} from {start_date} to {end_date}...")
    
    df = client.get_aggregate_pageviews(project, start_date, end_date, granularity="daily")
    
    if df is not None:
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)
        output_file = os.path.join(raw_dir, "en_wiki_pageviews_daily.csv")
        df.to_csv(output_file, index=False)
        print(f"Successfully saved {len(df)} rows to {output_file}")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    fetch_daily_data()
