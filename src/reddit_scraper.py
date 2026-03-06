import requests
import pandas as pd
import time

class RedditScraper:

    def __init__(self):
        self.headers = {
            "User-Agent": "WikipediaAnalysis/1.0 (academic research project)"
        }
        self.base_url = "https://www.reddit.com"

    def search_subreddit(self, subreddit, query, limit=500, sort="relevance", time_filter="all"):
        """search a subreddit for posts matching a query. paginates to get up to limit posts."""
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
                    print("  rate limited, waiting 10s...")
                    time.sleep(10)
                    continue
                if response.status_code != 200:
                    print(f"  error {response.status_code} on r/{subreddit}")
                    break

                data = response.json()
                children = data.get("data", {}).get("children", [])
                if not children:
                    break

                for child in children:
                    post = child["data"]
                    # skip deleted/removed at scrape time
                    text = post.get("selftext", "")
                    if text in ["[deleted]", "[removed]"]:
                        text = None
                    posts.append({
                        "subreddit": subreddit,
                        "title": post.get("title", ""),
                        "text": text,
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

                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"  request failed: {e}")
                break

        if posts:
            df = pd.DataFrame(posts)
            df = df[df["date"] >= "2020-01-01"].reset_index(drop=True)
            print(f"  scraped {len(df)} posts from r/{subreddit} (after 2020 filter)")
            return df
        return pd.DataFrame()

    def search_subreddit_extended(self, subreddit, query, limit=300):
        """run 4 sort methods and deduplicate to maximize unique posts retrieved.
        reddit hard caps at ~250 per search so this is the best workaround."""
        all_posts = []

        for sort in ["relevance", "new", "top", "comments"]:
            print(f"  sort={sort}...")
            df = self.search_subreddit(subreddit, query, limit=limit, sort=sort)
            if not df.empty:
                all_posts.append(df)
            time.sleep(3)

        if not all_posts:
            return pd.DataFrame()

        combined = pd.concat(all_posts, ignore_index=True)
        before = len(combined)
        combined = combined.drop_duplicates(subset="id").reset_index(drop=True)
        print(f"  deduplicated: {before} -> {len(combined)} unique posts")
        return combined

    def scrape_multiple_subreddits(self, subreddit_queries, limit_per_sub=300):
        """takes a dict of {subreddit: query} and scrapes all of them."""
        all_posts = []
        for sub, query in subreddit_queries.items():
            print(f"\nsearching r/{sub}...")
            df = self.search_subreddit_extended(sub, query, limit=limit_per_sub)
            if not df.empty:
                all_posts.append(df)
            time.sleep(3)

        if not all_posts:
            return pd.DataFrame()
        combined = pd.concat(all_posts, ignore_index=True)
        combined = combined.drop_duplicates(subset="id").reset_index(drop=True)
        return combined


if __name__ == "__main__":
    scraper = RedditScraper()
    df = scraper.search_subreddit_extended("wikipedia", "ChatGPT OR AI", limit=10)
    if not df.empty:
        print(df[["title", "score", "date"]].to_string())
