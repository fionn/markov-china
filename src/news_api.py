#!/usr/bin/env python3
"""News API wrapper"""

import os
from typing import Union

import requests

# pylint: disable=too-few-public-methods
class NewsAPI:
    """Wrapper for querying News API"""

    def __init__(self) -> None:
        api_key = os.environ["NEWS_API_KEY"]
        self.url = "https://newsapi.org"
        self.session = requests.Session()
        headers = {"Authorization": api_key}
        self.session.headers.update(headers)

    def headlines(self, query: str) -> list:
        """GET headlines"""
        payload: dict[str, Union[str, int]] = {"language": "en",
                                               "pagesize": 100,
                                               "q": query}
        response = self.session.get(self.url + "/v2/everything", params=payload)
        articles = response.json()["articles"]
        return [article["title"].split("- Reuters")[0] for article in articles]

def main() -> None:
    """Entry point"""
    news_api = NewsAPI()
    for headline in news_api.headlines("china"):
        print(headline)

if __name__ == "__main__":
    main()
