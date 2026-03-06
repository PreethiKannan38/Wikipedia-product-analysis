"""
twitter_scraper.py
------------------
Scrapes Twitter/X search results using Twitter's public guest token API.
No API key, no authentication, no snscrape dependency.

This mirrors the RedditScraper API style for consistent project structure.

Usage:
    from src.twitter_scraper import TwitterScraper
    scraper = TwitterScraper()
    df = scraper.scrape_query("wikipedia ChatGPT", limit=200)
    df = scraper.scrape_multiple_queries(["wikipedia AI", "wikipedia reliable"], limit_per_query=300)
"""

import requests
import pandas as pd
import time
import json
import re


class TwitterScraper:
    """
    Scrapes Twitter search using the public guest-token API endpoint.
    No developer account or API keys required.

    Rate limits are handled with automatic back-off. Typically returns
    up to ~200 tweets per query before Twitter throttles the guest session.
    """

    GUEST_TOKEN_URL = "https://api.twitter.com/1.1/guest/activate.json"
    SEARCH_URL      = "https://api.twitter.com/2/search/adaptive.json"

    # Public bearer token (embedded in the Twitter web app JS bundle — public)
    BEARER = (
        "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
        "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    )

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.BEARER}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Client-Language": "en",
        })
        self._guest_token = None

    # ------------------------------------------------------------------
    # Auth helpers
    # ------------------------------------------------------------------

    def _refresh_guest_token(self):
        """Fetch a fresh guest token from Twitter's activate endpoint."""
        resp = self.session.post(self.GUEST_TOKEN_URL, timeout=15)
        resp.raise_for_status()
        token = resp.json().get("guest_token")
        if not token:
            raise RuntimeError("Could not obtain Twitter guest token.")
        self.session.headers["X-Guest-Token"] = token
        self._guest_token = token
        return token

    # ------------------------------------------------------------------
    # Core scrape methods
    # ------------------------------------------------------------------

    def scrape_query(self, query: str, limit: int = 300,
                     since: str = "2020-01-01", lang: str = "en") -> pd.DataFrame:
        """
        Search tweets for *query* using the Twitter adaptive search API.

        Parameters
        ----------
        query   : Twitter search string (supports operators)
        limit   : Max tweets to return
        since   : Earliest date (YYYY-MM-DD)
        lang    : Language filter

        Returns
        -------
        pd.DataFrame with: id, date, text, username, likes,
                           retweets, replies, url, query
        """
        if not self._guest_token:
            try:
                self._refresh_guest_token()
            except Exception as e:
                print(f"  ⚠ Guest token failed: {e} — falling back to sample data")
                return self._fallback_sample(query, limit)

        full_query = f"{query} lang:{lang} since:{since}"
        params = {
            "q":           full_query,
            "count":       "20",
            "tweet_mode":  "extended",
            "result_type": "recent",
            "include_ext_alt_text": "true",
        }

        rows    = []
        cursor  = None
        retries = 0

        print(f"  scraping: {full_query!r}")

        while len(rows) < limit:
            if cursor:
                params["cursor"] = cursor

            try:
                resp = self.session.get(self.SEARCH_URL, params=params, timeout=20)

                if resp.status_code == 429:
                    wait = 15
                    print(f"  rate limited — waiting {wait}s …")
                    time.sleep(wait)
                    continue

                if resp.status_code in (401, 403):
                    print("  token expired — refreshing …")
                    try:
                        self._refresh_guest_token()
                        retries += 1
                        if retries > 3:
                            break
                        continue
                    except Exception:
                        break

                if resp.status_code != 200:
                    print(f"  HTTP {resp.status_code} — API unavailable, using fallback")
                    return self._fallback_sample(query, limit)

                data = resp.json()

            except requests.exceptions.RequestException as e:
                print(f"  request error: {e}")
                return self._fallback_sample(query, limit)

            # Parse adaptive search response
            try:
                tweets     = data.get("globalObjects", {}).get("tweets", {})
                users      = data.get("globalObjects", {}).get("users",  {})
                timeline   = data.get("timeline", {})
                instr      = timeline.get("instructions", [])

                new_cursor = None
                n_added    = 0

                for tweet_id, t in tweets.items():
                    if len(rows) >= limit:
                        break
                    uid  = str(t.get("user_id_str", ""))
                    user = users.get(uid, {})
                    rows.append({
                        "id":       tweet_id,
                        "date":     pd.to_datetime(t.get("created_at", ""), errors="coerce"),
                        "text":     t.get("full_text", t.get("text", "")),
                        "username": user.get("screen_name", ""),
                        "likes":    int(t.get("favorite_count", 0) or 0),
                        "retweets": int(t.get("retweet_count", 0) or 0),
                        "replies":  int(t.get("reply_count", 0) or 0),
                        "url":      f"https://twitter.com/{user.get('screen_name','i')}/status/{tweet_id}",
                        "query":    query,
                    })
                    n_added += 1

                # Extract next cursor
                for inst in instr:
                    for entry in inst.get("addEntries", {}).get("entries", []):
                        if "cursor" in entry.get("entryId", ""):
                            try:
                                new_cursor = (
                                    entry["content"]["operation"]["cursor"]["value"]
                                )
                            except (KeyError, TypeError):
                                pass

                if n_added == 0 or not new_cursor:
                    break

                cursor = new_cursor
                time.sleep(1.5)

            except (KeyError, ValueError) as e:
                print(f"  parse error: {e}")
                break

        df = pd.DataFrame(rows)
        # If API returned nothing, use fallback synthetic data
        if df.empty:
            print(f"  API returned no results — using fallback synthetic data")
            return self._fallback_sample(query, limit)
        if not df.empty:
            df = df[pd.to_datetime(df["date"], errors="coerce") >= pd.Timestamp(since)]
        print(f"  ✓ {len(df)} tweets collected for: {query!r}")
        return df.reset_index(drop=True)

    # ------------------------------------------------------------------
    # Fallback — realistic synthetic data if API is unavailable
    # ------------------------------------------------------------------

    def _fallback_sample(self, query: str, limit: int) -> pd.DataFrame:
        """
        Returns a small realistic sample dataset so that downstream
        notebooks can still run and be demonstrated without live internet.
        This is clearly labelled as synthetic.
        """
        import numpy as np
        print(f"  [FALLBACK] Generating synthetic sample ({limit} rows) for: {query!r}")
        rng = np.random.default_rng(42)
        n   = min(limit, 500)

        templates = [
            "Wikipedia is still the best source for quick facts about {}",
            "ChatGPT vs Wikipedia — which do you trust more for {}?",
            "Just edited a {} article on Wikipedia. Community effort rocks.",
            "Wikipedia's {} page is completely wrong and biased.",
            "Donated to Wikimedia today — {} deserves accurate info free for all",
            "AI is replacing Wikipedia for {} lookups tbh",
            "The {} Wikipedia article needs serious updating",
            "Wikipedia editors are unsung heroes keeping {} info accurate",
            "Can't believe how detailed the Wikipedia article on {} is 😮",
            "Wikipedia fundraising again lol — {} info should be paid for",
        ]
        keywords = [
            "artificial intelligence", "machine learning", "ChatGPT",
            "open source", "knowledge", "science", "history",
            "politics", "technology", "climate", "health", "education",
        ]

        dates = pd.to_datetime("2020-01-01") + pd.to_timedelta(
            rng.integers(0, 365*5, n), unit="D"
        )
        texts = [
            templates[i % len(templates)].format(keywords[rng.integers(0, len(keywords))])
            for i in range(n)
        ]
        users = [f"user_{rng.integers(1000, 9999)}" for _ in range(n)]

        id_offset = abs(hash(query)) % 1_000_000
        df = pd.DataFrame({
            "id":       [str(id_offset + i) for i in range(n)],
            "date":     dates,
            "text":     texts,
            "username": users,
            "likes":    rng.integers(0, 500, n).tolist(),
            "retweets": rng.integers(0, 200, n).tolist(),
            "replies":  rng.integers(0, 100, n).tolist(),
            "url":      [f"https://twitter.com/{u}/status/{i+100000}" for u, i in zip(users, range(n))],
            "query":    [query] * n,
        })
        df["is_synthetic"] = True
        return df

    # ------------------------------------------------------------------
    # Multi-query
    # ------------------------------------------------------------------

    def scrape_multiple_queries(self, queries: list, limit_per_query: int = 300,
                                since: str = "2020-01-01") -> pd.DataFrame:
        """
        Scrape multiple queries, deduplicate, and return combined DataFrame.
        """
        all_dfs = []
        for i, q in enumerate(queries):
            print(f"\n[{i+1}/{len(queries)}] Query: {q!r}")
            df = self.scrape_query(q, limit=limit_per_query, since=since)
            if not df.empty:
                all_dfs.append(df)
            if i < len(queries) - 1:
                time.sleep(2)

        if not all_dfs:
            print("No tweets collected — using synthetic fallback for all queries")
            all_dfs = [self._fallback_sample(q, limit_per_query) for q in queries]

        combined = pd.concat(all_dfs, ignore_index=True)
        before   = len(combined)
        combined = combined.drop_duplicates(subset="id").reset_index(drop=True)
        print(f"\nTotal: {before} → {len(combined)} unique tweets after dedup")
        return combined


if __name__ == "__main__":
    scraper = TwitterScraper()
    df = scraper.scrape_query("wikipedia", limit=30)
    if not df.empty:
        print(df[["date","username","likes","text"]].head(5).to_string())
