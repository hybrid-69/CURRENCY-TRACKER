"""
Live and historical exchange rate data via Frankfurter (api.frankfurter.app) -
a free API backed by European Central Bank reference rates. No API key needed.
"""

from datetime import date, timedelta

import requests

from config.settings import FRANKFURTER_BASE, DEFAULT_HISTORY_DAYS
from utils.storage import cached


class ExchangeDataError(Exception):
    pass


@cached(namespace="latest_rate")
def get_latest_rate(base: str, target: str) -> dict:
    url = f"{FRANKFURTER_BASE}/latest"
    try:
        resp = requests.get(url, params={"from": base, "to": target}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        raise ExchangeDataError(f"Could not fetch rate for {base}->{target}: {exc}") from exc

    if "rates" not in data or target not in data["rates"]:
        raise ExchangeDataError(
            f"No rate data returned for {base}->{target}. "
            "Check both currency codes are valid (e.g. USD, INR, EUR)."
        )

    return {
        "base": base,
        "target": target,
        "rate": data["rates"][target],
        "date": data["date"],
    }


@cached(namespace="history")
def get_historical_rates(base: str, target: str, days: int = DEFAULT_HISTORY_DAYS) -> list:
    end = date.today()
    start = end - timedelta(days=days)
    url = f"{FRANKFURTER_BASE}/{start.isoformat()}..{end.isoformat()}"

    try:
        resp = requests.get(url, params={"from": base, "to": target}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        raise ExchangeDataError(f"Could not fetch history for {base}->{target}: {exc}") from exc

    rates_by_date = data.get("rates", {})
    if not rates_by_date:
        raise ExchangeDataError(f"No historical data returned for {base}->{target}.")

    series = []
    for d in sorted(rates_by_date.keys()):
        rate = rates_by_date[d].get(target)
        if rate is not None:
            series.append({"date": d, "rate": rate})
    return series


def convert_amount(amount: float, base: str, target: str) -> dict:
    quote = get_latest_rate(base, target)
    converted = round(amount * quote["rate"], 2)
    return {
        "amount": amount,
        "base": base,
        "target": target,
        "rate": quote["rate"],
        "converted": converted,
        "date": quote["date"],
    }
