import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add src to path
sys.path.append(os.path.abspath('c:/Users/preet/Documents/BA/Wikipedia-product-analysis'))
from src.data_prep import clean_pageview_data, add_time_features

# Configuration
DATA_PATH = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/data/raw/en_wiki_pageviews_daily.csv'
REPORT_DIR = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/reports/'
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")
PURPLE_COLOR = '#800080'

# 1. Load and Prepare Data
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = clean_pageview_data(df)
df = add_time_features(df)

# Ensure correct weekday ordering
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)

# 2. Weekly Usage Profile
weekly_profile = df.groupby('day_of_week')['views'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=weekly_profile, x='day_of_week', y='views', palette='viridis')
plt.title('Wikipedia Weekly Usage Profile: Mean Views by Day', fontsize=15)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Average Pageviews', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, 'section_2_weekly_profile_bars.png'))
print("Weekly profile bar chart saved.")

# 3. Annual Weekend vs Weekday Analysis
annual_ratios = df.groupby(['year', 'is_weekend'])['views'].mean().unstack()
annual_ratios.columns = ['weekday_mean', 'weekend_mean']
annual_ratios['ratio'] = annual_ratios['weekend_mean'] / annual_ratios['weekday_mean']

print("Yearly Weekend vs Weekday Ratio Table:")
print(annual_ratios[['weekday_mean', 'weekend_mean', 'ratio']])

# 4. Main Visualization: Weekend-to-Weekday Ratio Trend
plt.figure(figsize=(14, 8))
plt.plot(annual_ratios.index, annual_ratios['ratio'], marker='o', linestyle='-', color=PURPLE_COLOR, linewidth=2.5, markersize=8)
plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.6, label='Equal Weekend/Weekday Traffic')
plt.title('Ratio of Weekend to Weekday Pageviews (2015-2025)', fontsize=18, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Weekend / Weekday Mean Ratio', fontsize=14)
plt.ylim(0.94, 1.04)
plt.grid(True, which='both', linestyle='-', alpha=0.3)
plt.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, 'section_2_weekend_weekday_ratio.png'), dpi=300)
print("Weekend-to-Weekday ratio plot saved.")

# 5. Stability Check
stability = df.groupby('day_of_week')['views'].agg(['mean', 'std']).reset_index()
stability['cv'] = stability['std'] / stability['mean']
print("Stability Check:")
print(stability)
