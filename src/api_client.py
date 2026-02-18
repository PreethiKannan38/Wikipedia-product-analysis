import requests
import pandas as pd
from datetime import datetime

class WikipediaAPIClient:
    """A client to interact with the Wikimedia Pageviews API."""
    BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

    def __init__(self, user_agent="WikipediaAnalysisBot/1.0 (contact: your-email@example.com)"):
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json"
        }


        """Fetch aggregate pageviews for a specific project.
        Args:
            project (str): Project name, e.g., 'en.wikipedia.org'
            start (str): Start date in YYYYMMDD format
            end (str): End date in YYYYMMDD format
            access (str): 'all-access', 'desktop', 'mobile-app', 'mobile-web'
            agent (str): 'all-agents', 'user', 'spider', 'bot'
            granularity (str): 'daily', 'monthly'
        Returns:
            pd.DataFrame: Dataframe containing timestamps and pageview counts."""
    def get_aggregate_pageviews(self, project, start, end, access="all-access", agent="user", granularity="daily"):
        url = f"{self.BASE_URL}/aggregate/{project}/{access}/{agent}/{granularity}/{start}/{end}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            print(response.text)
            return None
        data = response.json()
        df = pd.DataFrame(data["items"])
        # Convert timestamp to datetime
        # API format is YYYYMMDDHH, e.g., 2022010100
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H")
        return df[["timestamp", "views"]]

if __name__ == "__main__":
    client = WikipediaAPIClient()
    df = client.get_aggregate_pageviews("en.wikipedia.org", "20230101", "20230131")
    if df is not None:
        print(df.head())
