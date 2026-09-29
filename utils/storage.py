"""
Caching decorator + JSON storage for watchlist/rate targets.
Simpler than a price-tracker's version of this file since exchange rate
data is naturally JSON-serializable (plain dicts/lists), avoiding any
DataFrame-caching complexity entirely.
"""

import functools
import hashlib
import json
import os
import time

from config.settings import CACHE_DIR, CACHE_TTL_SECONDS, STORAGE_PATH


def _cache_key(namespace: str, args, kwargs) -> str:
    raw = namespace + str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(raw.encode()).hexdigest()


def cached(namespace: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            os.makedirs(CACHE_DIR, exist_ok=True)
            key = _cache_key(namespace, args, kwargs)
            path = os.path.join(CACHE_DIR, f"{key}.json")

            if os.path.exists(path):
                age = time.time() - os.path.getmtime(path)
                if age < CACHE_TTL_SECONDS:
                    try:
                        with open(path, "r") as f:
                            return json.load(f)
                    except Exception:
                        try:
                            os.remove(path)
                        except OSError:
                            pass

            result = func(*args, **kwargs)
            try:
                with open(path, "w") as f:
                    json.dump(result, f)
            except Exception:
                pass
            return result

        return wrapper

    return decorator


def _load_store() -> dict:
    if not os.path.exists(STORAGE_PATH):
        return {"watchlist": [], "targets": []}
    try:
        with open(STORAGE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"watchlist": [], "targets": []}


def _save_store(store: dict):
    os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)
    with open(STORAGE_PATH, "w") as f:
        json.dump(store, f, indent=2)


def add_to_watchlist(base: str, target: str):
    store = _load_store()
    pair = f"{base}/{target}"
    if pair not in store["watchlist"]:
        store["watchlist"].append(pair)
        _save_store(store)


def get_watchlist() -> list:
    return _load_store()["watchlist"]


def add_target(base: str, target: str, target_rate: float, direction: str):
    store = _load_store()
    store["targets"].append({
        "base": base, "target": target,
        "target_rate": target_rate, "direction": direction,
    })
    _save_store(store)


def get_targets() -> list:
    return _load_store()["targets"]


def clear_targets():
    store = _load_store()
    store["targets"] = []
    _save_store(store)
