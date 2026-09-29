"""Central configuration for the Currency Exchange Rate Tracker."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CURRENCY_MAPPING_PATH = os.path.join(BASE_DIR, "data", "currency_mapping.csv")
CACHE_DIR = os.path.join(BASE_DIR, "data", "cache")
STORAGE_PATH = os.path.join(BASE_DIR, "data", "user_data.json")

FRANKFURTER_BASE = "https://api.frankfurter.app"

DEFAULT_HISTORY_DAYS = 180

NEWS_RSS_TEMPLATE = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
MAX_HEADLINES = 10

CACHE_TTL_SECONDS = 900
