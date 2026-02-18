# Wikipedia Product Health Analysis (2015-2025)

This project analyzes Wikipedia as a product by evaluating its health through time-series data (pageviews, active editors, edit volume) and assessing the impact of internal initiatives such as Wikipedia campaigns on user behavior.

## Project Structure

```text
wikipedia-analysis/
├── data/
│   ├── raw/            # Original, immutable data (e.g., raw API responses)
│   └── processed/      # Cleaned data ready for analysis
├── notebooks/          # Jupyter notebooks for EDA and experimentation
├── src/                # Shared Python package for reusable logic
│   ├── api_client.py   # Client for Wikimedia Pageviews API
│   └── data_prep.py    # Cleaning and aggregation utilities
├── reports/            # Generated figures and final documentation
└── README.md           # This file
```

## Core Components

### API Client (`src/api_client.py`)
The `WikipediaAPIClient` encapsulates the logic for interacting with the [Wikimedia REST API](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews).
```python
from src.api_client import WikipediaAPIClient
client = WikipediaAPIClient()
df = client.get_aggregate_pageviews("en.wikipedia.org", "20230101", "20230131")
```

### Data Preprocessing (`src/data_prep.py`)
Includes functions for:
*   `clean_pageview_data`: Removing nulls and ensuring type safety.
*   `aggregate_data`: Resampling time-series data (e.g., daily to weekly/monthly).
*   `add_time_features`: Adding helpful columns like `day_of_week` or `is_weekend`.

## Team Collaboration
*   **Source Truth**: Always store raw API exports in `data/raw/` to avoid redundant network calls.
*   **Modularity**: If you write a complex data transformation or plotting function in a notebook, move it to `src/` so others can use it.
