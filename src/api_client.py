import requests
import pandas as pd
import time

class WikipediaAPIClient:
    BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

    def __init__(self, user_agent="WikipediaAnalysisBot/1.0 (contact: your-email@example.com)"):
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json"
        }

    def get_aggregate_pageviews(self, project, start, end, access="all-access", agent="user", granularity="monthly"):
        """fetch total pageviews for a wikipedia project over a date range.
        start/end format is YYYYMMDD. granularity can be daily or monthly."""
        url = f"{self.BASE_URL}/aggregate/{project}/{access}/{agent}/{granularity}/{start}/{end}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"error {response.status_code}: {response.text}")
            return None
        data = response.json()
        df = pd.DataFrame(data["items"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H")
        return df[["timestamp", "views"]]

    def get_article_pageviews(self, article, start, end, project="en.wikipedia.org", access="all-access", granularity="monthly"):
        """fetch monthly pageviews for a specific wikipedia article.
        article should be URL-encoded, e.g. 'Artificial_intelligence'.
        returns a dataframe with timestamp, article, and views columns."""
        url = f"{self.BASE_URL}/per-article/{project}/{access}/user/{article}/{granularity}/{start}/{end}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"error fetching {article}: {response.status_code}")
            return None
        data = response.json()
        df = pd.DataFrame(data["items"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H")
        df["article"] = article
        return df[["timestamp", "article", "views"]]

    def get_multiple_articles(self, articles, start, end, granularity="monthly"):
        """fetch pageviews for a list of articles and combine into one dataframe."""
        all_dfs = []
        for article in articles:
            print(f"  fetching {article}...")
            df = self.get_article_pageviews(article, start, end, granularity=granularity)
            if df is not None:
                all_dfs.append(df)
            time.sleep(0.5)
        if not all_dfs:
            return pd.DataFrame()
        return pd.concat(all_dfs, ignore_index=True)


if __name__ == "__main__":
    client = WikipediaAPIClient()
    df = client.get_article_pageviews("Artificial_intelligence", "20220101", "20240101")
    if df is not None:
        print(df.head())
