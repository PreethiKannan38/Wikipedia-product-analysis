import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import json
from datetime import timedelta

# Add src to path
sys.path.append(os.path.abspath('c:/Users/preet/Documents/BA/Wikipedia-product-analysis'))
from src.data_prep import clean_pageview_data, add_time_features

# Configuration
DATA_PATH = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/data/raw/en_wiki_pageviews_daily.csv'
CONFIG_PATH = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/config/campaign_dates.json'
REPORT_DIR = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/reports/'
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

def analyze_campaign(df, start_date, campaign_name, year):
    start_date = pd.to_datetime(start_date)
    est_start = start_date - timedelta(days=60)
    est_end = start_date - timedelta(days=31)
    event_start = start_date - timedelta(days=30)
    event_end = start_date + timedelta(days=30)
    
    est_data = df[(df['timestamp'] >= est_start) & (df['timestamp'] <= est_end)]
    event_data = df[(df['timestamp'] >= event_start) & (df['timestamp'] <= event_end)].copy()
    
    if est_data.empty or event_data.empty: return None
    baseline = est_data.groupby('day_of_week')['views'].mean().to_dict()
    event_data['expected_views'] = event_data['day_of_week'].map(baseline)
    event_data['excess_views'] = event_data['views'] - event_data['expected_views']
    event_data['percent_lift'] = (event_data['excess_views'] / event_data['expected_views']) * 100
    event_data['relative_day'] = (event_data['timestamp'] - start_date).dt.days
    return event_data

# Load
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = clean_pageview_data(df)
df = add_time_features(df)
with open(CONFIG_PATH, 'r') as f: config = json.load(f)

# Run All
all_results = []
for campaign_type, dates in config.items():
    for year, date_str in dates.items():
        event_df = analyze_campaign(df, date_str, campaign_type, year)
        if event_df is not None:
            active_mask = (event_df['relative_day'] >= 0) & (event_df['relative_day'] <= 14)
            all_results.append({
                'Campaign': campaign_type, 'Year': year,
                'Avg Lift (%)': event_df.loc[active_mask, 'percent_lift'].mean()
            })

comparison_df = pd.DataFrame(all_results)
plt.figure(figsize=(12, 6))
sns.boxplot(data=comparison_df, x='Campaign', y='Avg Lift (%)', palette='Set2')
plt.title('Average Traffic Lift by Campaign Type (2015-2025)', fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, 'section_3_campaign_comparison.png'))
print("Campaign comparison plot saved.")
