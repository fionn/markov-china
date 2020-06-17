#!/usr/bin/env python3
"""FT wrapper module"""

import os
from typing import Generator

import requests

class FT:
    """FT wrapper"""

    def __init__(self) -> None:
        api_key = os.environ["FT_API_KEY"]
        self.url = "https://api.ft.com"
        self.session = requests.Session()
        headers = {"X-Api-Key": api_key}
        self.session.headers.update(headers)

    def search(self, query: str, max_results: int = 100,
               offset: int = 0) -> dict:
        """Send query payload"""
        payload = {
            "queryString": query,
            "queryContext": {
                "curations": ["ARTICLES"]
            },
            "resultContext": {
                "maxResults": max_results,
                "offset": offset,
                "aspects": ["title"],
                #"facets": {"names": ["subjects", "topics"]}
            }
        }

        search_url = self.url + "/content/search/v1"
        response = self.session.post(search_url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def titles(response: dict) -> Generator[str, None, None]:
        """Parse response for titles"""
        for result in response["results"][0]["results"]:
            try:
                yield result["title"]["title"]
            except KeyError:
                if response["results"][0]["indexCount"] == 0:
                    return
                continue

def main() -> None:
    """Entry point"""
    ft = FT() # pylint: disable=invalid-name

    query = "regions:China"

    max_results = 100
    for offset in range(0, 400, max_results):
        response = ft.search(query, max_results, offset)
        titles = ft.titles(response)
        for title in titles:
            print(title)

if __name__ == "__main__":
    main()
