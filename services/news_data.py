"""Macroeconomic news retrieval for a currency pair, via free Google News RSS."""

import re
from urllib.parse import quote

import feedparser

from config.settings import NEWS_RSS_TEMPLATE, MAX_HEADLINES


def _clean_headline(title: str) -> str:
    return re.sub(r"\s*-\s*[^-]+$", "", title).strip()


def get_currency_news(base: str, target: str, max_headlines: int = MAX_HEADLINES) -> list:
    query = quote(f"{base} {target} exchange rate")
    url = NEWS_RSS_TEMPLATE.format(query=query)

    feed = feedparser.parse(url)
    headlines = []
    seen_titles = set()

    for entry in feed.entries:
        title = _clean_headline(entry.get("title", ""))
        if not title or title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())
        headlines.append({
            "title": title,
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
        })
        if len(headlines) >= max_headlines:
            break

    return headlines
