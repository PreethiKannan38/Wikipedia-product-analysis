# Wikipedia Product Health Analysis (2015-2025)

## Overview
This project evaluates the "product health" of Wikipedia between 2015 and 2025. It focuses on analyzing user engagement through time-series data and assessing the impact of various Wikimedia initiatives (campaigns) on editor activity and pageview growth. By integrating data from Wikimedia's internal APIs with external social signals from Reddit and Twitter (X), the project provides a holistic view of Wikipedia's ecosystem and public perception.

---

## Project Structure
```text
wikipedia-analysis/
├── config/              # Configuration files (e.g., campaign dates, API settings)
├── data/                # Data storage (ignored by git except for structure)
│   ├── raw/             # Original, immutable data from APIs and scrapers
│   └── processed/       # Cleaned and engineered datasets ready for analysis
├── notebooks/           # Jupyter notebooks for EDA and experimentation
│   ├── editor_analysis/ # Specific notebooks for editor behavior
│   ├── pageview_analysis/ # Specific notebooks for traffic patterns
│   ├── reddit_notebooks/ # Analysis of Reddit data
│   └── twitter_notebooks/ # Analysis of Twitter data
├── reports/             # Generated figures, visualizations, and final reports
├── src/                 # Modular Python source code
│   ├── api_client.py    # Wikimedia API wrapper
│   ├── reddit_scraper.py # Scraper for Reddit community data
│   ├── twitter_scraper.py # Scraper for Twitter (X) data
│   ├── data_prep.py     # General data cleaning utilities
│   ├── sentiment.py     # Sentiment analysis for social data
│   └── ...              # Other specialized processing scripts
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

---

## Datasets & APIs

### 1. Wikimedia API (Pageviews & Metrics)
We use the [Wikimedia Analytics Query Service (AQS)](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews) to retrieve core product metrics.
- **Endpoint**: `https://wikimedia.org/api/rest_v1/metrics/pageviews`
- **Data Collected**: Aggregate pageviews (by project, access method, and agent type) and per-article traffic.
- **Granularity**: Monthly and Daily data from 2015 to present.

### 2. Reddit Data
Public discussions related to Wikipedia are collected using a custom `RedditScraper`.
- **Source**: Reddit Search API (`reddit.com/r/{subreddit}/search.json`).
- **Subreddits**: Focuses on `r/wikipedia`, `r/technology`, and others where Wikipedia utility or controversies are discussed.
- **Features**: Post title, text, score, comment count, and timestamp (filtered from 2020 onwards).

### 3. Twitter (X) Data
Social sentiment and mentions are gathered using a guest-token-based `TwitterScraper`.
- **Mechanism**: Utilizes Twitter's adaptive search API with public guest tokens (no API key required).
- **Metrics**: Tweet content, engagement (likes, retweets, replies), and user metadata.
- **Purpose**: To gauge real-time public reaction to Wikipedia campaigns and service changes.

### 4. Internal Campaign Data
We track specific Wikimedia initiatives defined in `config/campaign_dates.json`:
- **Fundraising**: Annual donation drives.
- **Wiki Loves Monuments / Earth**: Photography and content competitions.
- **Wikipedia Asian Month**: Content creation marathons.
---

# Requirements

To run the project locally, install:

- Python **3.10+**
- pandas
- matplotlib
- seaborn
- requests
- jupyter (recommended)

Example installation:

```bash
pip install pandas matplotlib seaborn requests jupyter
```
