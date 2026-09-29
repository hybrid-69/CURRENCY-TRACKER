"""
Rate target tracking - lets the user set a target rate for a currency pair
and check whether the live rate has crossed it.
"""

from services.exchange_data import get_latest_rate, ExchangeDataError


def check_targets(targets: list) -> list:
    results = []
    for t in targets:
        try:
            quote = get_latest_rate(t["base"], t["target"])
            current = quote["rate"]
            if t["direction"] == "above":
                met = current >= t["target_rate"]
            else:
                met = current <= t["target_rate"]
            results.append({**t, "current_rate": current, "status": "MET" if met else "NOT MET"})
        except ExchangeDataError as e:
            results.append({**t, "current_rate": None, "status": f"ERROR: {e}"})
    return results
