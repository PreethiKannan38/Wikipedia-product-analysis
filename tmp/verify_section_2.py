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

# 1. Load and Prepare Data
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = clean_pageview_data(df)
df = add_time_features(df)

# 2. Calculate Annual Weekend-to-Weekday Ratio
# Step 1: Mean per year and per is_weekend
annual_means = df.groupby(['year', 'is_weekend'])['views'].mean().unstack()
annual_means.columns = ['weekday_mean', 'weekend_mean']

# Step 2: Calculate the Ratio
annual_means['ratio'] = annual_means['weekend_mean'] / annual_means['weekday_mean']

# 3. Visualize the Ratio Trend
plt.figure(figsize=(14, 8))

# Plot the ratio line (Purple marker line)
plt.plot(annual_means.index, annual_means['ratio'], marker='o', linestyle='-', color='purple', linewidth=2.5, markersize=8)

# Add horizontal reference line at 1.0
plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.6, label='Equal Weekend/Weekday Traffic')

# Formatting to match the provided image
plt.title('Ratio of Weekend to Weekday Pageviews (2015-2025)', fontsize=18, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Weekend / Weekday Mean Ratio', fontsize=14)
plt.ylim(0.94, 1.04)
plt.grid(True, which='both', linestyle='-', alpha=0.3)
plt.tick_params(labelsize=12)

# Saving the report
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, 'section_2_weekend_weekday_ratio.png'), dpi=300)
print("Weekend-to-Weekday ratio plot saved to reports/section_2_weekend_weekday_ratio.png")
