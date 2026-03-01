import requests
import pandas as pd
import time

class RedditScraper:

    def __init__(self):
        # reddit requires a proper user-agent or it blocks you
        self.headers = {
            "User-Agent": "WikipediaAnalysis/1.0 (academic research project)"
        }
        self.base_url = "https://www.reddit.com"

    def search_subreddit(self, subreddit, query, limit=500, sort="relevance", time_filter="all"):
        """search a subreddit for posts matching a query.
        reddit caps at ~250 results per search, so we paginate."""
        posts = []
        after = None
        fetched = 0

        while fetched < limit:
            batch_size = min(100, limit - fetched)
            params = {
                "q": query,
                "sort": sort,
                "t": time_filter,
                "limit": batch_size,
                "restrict_sr": "on",
                "type": "link"
            }
            if after:
                params["after"] = after

            url = f"{self.base_url}/r/{subreddit}/search.json"

            try:
                response = requests.get(url, params=params, headers=self.headers, timeout=15)
                if response.status_code == 429:
                    # rate limited, wait and retry
                    print("  rate limited, waiting 10s...")
                    time.sleep(10)
                    continue
                if response.status_code != 200:
                    print(f"  error {response.status_code} searching r/{subreddit}")
                    break

                data = response.json()
                children = data.get("data", {}).get("children", [])
                if not children:
                    break

                for child in children:
                    post = child["data"]
                    posts.append({
                        "subreddit": subreddit,
                        "title": post.get("title", ""),
                        "text": post.get("selftext", ""),
                        "score": post.get("score", 0),
                        "date": pd.to_datetime(post.get("created_utc", 0), unit="s"),
                        "num_comments": post.get("num_comments", 0),
                        "url": post.get("url", ""),
                        "permalink": f"https://reddit.com{post.get('permalink', '')}",
                        "id": post.get("id", "")
                    })

                after = data.get("data", {}).get("after")
                fetched += len(children)

                if not after:
                    break

                # respect rate limits
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"  request failed: {e}")
                break

        print(f"  scraped {len(posts)} posts from r/{subreddit}")
        return pd.DataFrame(posts) if posts else pd.DataFrame()

    def scrape_multiple_subreddits(self, subreddits, query, limit_per_sub=300):
        """search multiple subreddits and combine results."""
        all_posts = []
        for sub in subreddits:
            print(f"searching r/{sub}...")
            df = self.search_subreddit(sub, query, limit=limit_per_sub)
            if not df.empty:
                all_posts.append(df)
            time.sleep(3)  # extra pause between subreddits

        if not all_posts:
            return pd.DataFrame()
        return pd.concat(all_posts, ignore_index=True)


if __name__ == "__main__":
    scraper = RedditScraper()
    df = scraper.search_subreddit("wikipedia", "ChatGPT OR AI", limit=10)
    if not df.empty:
        print(df[["title", "score", "date"]].to_string())
