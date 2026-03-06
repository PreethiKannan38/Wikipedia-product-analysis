import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add src to path
sys.path.append(os.path.abspath('c:/Users/preet/Documents/BA/Wikipedia-product-analysis'))
from src.data_prep import clean_pageview_data, add_time_features

# Configuration
DATA_PATH = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/data/raw/en_wiki_pageviews_monthly.csv'
REPORT_DIR = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/reports/'
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="rocket")

# 1. Load and Clean Data
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = clean_pageview_data(df)
df = add_time_features(df)

print(f"Data loaded from {DATA_PATH}")

# 2. Long-Term Trend
df['moving_avg'] = df['views'].rolling(window=12, center=True).mean()

plt.figure(figsize=(14, 7))
plt.plot(df['timestamp'], df['views'], label='Monthly Pageviews', alpha=0.5, color='gray')
plt.plot(df['timestamp'], df['moving_avg'], label='12-Month Moving Average', color='red', linewidth=2)
plt.title('Wikipedia Monthly Pageviews and Long-Term Trend (2015-2025)', fontsize=15)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Pageviews', fontsize=12)
plt.legend()
plt.savefig(os.path.join(REPORT_DIR, 'section_1_long_term_trend.png'))
print("Long-term trend plot saved.")

# 3. YoY Overlay
plt.figure(figsize=(14, 8))
# Note: seaborn sns.lineplot can handle the grouping by year automatically
sns.lineplot(data=df, x='month', y='views', hue='year', palette='viridis', marker='o')
plt.xticks(rotation=45)
plt.title('Wikipedia Seasonality: Year-over-Year Overlay (2015-2025)', fontsize=15)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Pageviews', fontsize=12)
plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, 'section_1_yoy_overlay.png'))
print("YoY overlay plot saved.")
