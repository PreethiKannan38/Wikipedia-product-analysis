import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from scipy.stats import pearsonr

# Add project root to path
sys.path.append(os.path.abspath('c:/Users/preet/Documents/BA/Wikipedia-product-analysis'))
from src.data_prep import add_time_features

# Configuration
DATA_PATH = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/data/raw/en_wiki_topic_pageviews_daily.csv'
REPORT_DIR = 'c:/Users/preet/Documents/BA/Wikipedia-product-analysis/reports/'
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Load Data
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = add_time_features(df)

# 2. Normalization
def normalize_series(group):
    min_v, max_v = group['views'].min(), group['views'].max()
    group['norm_views'] = (group['views'] - min_v) / (max_v - min_v) if max_v != min_v else 0
    return group

df = df.groupby('article', group_keys=False).apply(normalize_series)
cluster_ts = df.groupby(['cluster', 'timestamp'])[['views', 'norm_views']].mean().reset_index()
cluster_ts = add_time_features(cluster_ts)

# 3. Seasonal Shape
seasonal_profile = cluster_ts.groupby(['cluster', 'month'])['norm_views'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=seasonal_profile, x='month', y='norm_views', hue='cluster', marker='o')
plt.title('Topic Seasonal Shape')
plt.savefig(os.path.join(REPORT_DIR, 'section_4_topic_seasonal_shape.png'))
plt.close()

# 4. Amplitude
stats = cluster_ts.groupby('cluster')['views'].agg(['max', 'min', 'mean']).reset_index()
stats['amplitude'] = (stats['max'] - stats['min']) / stats['mean']
plt.figure(figsize=(8, 5))
sns.barplot(data=stats, x='cluster', y='amplitude')
plt.title('Seasonal Amplitude')
plt.savefig(os.path.join(REPORT_DIR, 'section_4_topic_amplitude.png'))
plt.close()

# 5. Stability
def calculate_stability(df):
    years = sorted(df['year'].unique())
    correlations = []
    for cluster in df['cluster'].unique():
        cluster_df = df[df['cluster'] == cluster]
        profiles = []
        for year in years:
            profile = cluster_df[cluster_df['year'] == year].groupby('month')['norm_views'].mean()
            if len(profile) == 12: profiles.append(profile.values)
        for i in range(len(profiles) - 1):
            corr, _ = pearsonr(profiles[i], profiles[i+1])
            correlations.append({'cluster': cluster, 'correlation': corr})
    return pd.DataFrame(correlations)

stability_df = calculate_stability(cluster_ts)
avg_stability = stability_df.groupby('cluster')['correlation'].mean().reset_index()

# 6. Volatility
vol_list = []
for c in cluster_ts['cluster'].unique():
    subset = cluster_ts[cluster_ts['cluster'] == c].copy().sort_values('timestamp')
    subset['rolling_std'] = subset['norm_views'].rolling(window=30).std()
    vol_list.append(subset)
vol_df = pd.concat(vol_list)
plt.figure(figsize=(12, 5))
sns.lineplot(data=vol_df, x='timestamp', y='rolling_std', hue='cluster', alpha=0.5)
plt.title('Traffic Volatility')
plt.savefig(os.path.join(REPORT_DIR, 'section_4_topic_volatility.png'))
plt.close()

# 7. Recovery (Simplified)
results = []
for c in cluster_ts['cluster'].unique():
    subset = cluster_ts[cluster_ts['cluster'] == c].sort_values('timestamp')
    baseline = subset[(subset['timestamp'] >= '2019-08-01') & (subset['timestamp'] < '2020-02-01')]['views'].mean()
    post_shock = subset[subset['timestamp'] >= '2020-03-01'].copy()
    post_shock['monthly_mean'] = post_shock['views'].rolling(window=30).mean()
    recovery = post_shock[post_shock['monthly_mean'] <= baseline]
    if not recovery.empty:
        rec_date = recovery.iloc[0]['timestamp']
        months = (rec_date.year - 2020) * 12 + (rec_date.month - 3)
    else:
        months = "> 60"
    results.append({'cluster': c, 'recovery_months': months})

print("Verification Summary:")
print(f"Shapes and Amplitudes saved to {REPORT_DIR}")
print("\nStability (YoY Correlation):")
print(avg_stability)
print("\nPandemic Recovery (Months):")
print(pd.DataFrame(results))
