#!/usr/bin/env python3
"""Tweet Markov chain sentences of China headlines"""

import os
import re
import sys
from typing import List

import tweepy
import markovify
import nltk

from ft import FT

class NLPText(markovify.NewlineText):
    """Extend markovify.NewlineText with NLP"""

    def word_split(self, sentence: str) -> List[str]:
        """Splits a sentence into a list of words"""
        words = re.split(self.word_split_pattern, sentence)
        return ["::".join(tag) for tag in nltk.pos_tag(words)]

    def word_join(self, words: List[str]) -> str:
        """Re-joins a list of words into a sentence"""
        return " ".join(word.split("::")[0] for word in words)

# pylint: disable=too-few-public-methods
class Twitter:
    """Wrapper for the Twitter API"""

    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(os.environ["API_KEY"],
                                   os.environ["API_SECRET"])
        auth.set_access_token(os.environ["ACCESS_TOKEN"],
                              os.environ["ACCESS_TOKEN_SECRET"])
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

    @staticmethod
    def _compose(model: NLPText) -> dict:
        """Compose a status dictionary compatible with api.status_update"""
        text = model.make_short_sentence(280, state_size=1)
        place_id = "4797714c95971ac1" # PRC
        return {"status": text, "place_id": place_id}

    def update(self, model: NLPText,
               dry_run: bool = False) -> tweepy.Status:
        """Post tweet for constituency"""
        composition = self._compose(model)
        print(composition["status"], file=sys.stderr)

        if dry_run:
            return tweepy.Status

        return self.api.update_status(**composition)

# pylint: disable=invalid-name
def generate_corpus(ft: FT) -> str:
    """Gets headlines from FT"""
    query = "regions:China"

    corpus = ""
    max_results = 100
    for offset in range(0, 400, max_results):
        response = ft.search(query, max_results, offset)
        corpus += "\n".join(title for title in \
                            ft.titles(response))

    return corpus

def main() -> None:
    """Entry point"""
    ft = FT()
    corpus = generate_corpus(ft)
    model = NLPText(corpus)
    twitter = Twitter()
    twitter.update(model)

if __name__ == "__main__":
    main()
