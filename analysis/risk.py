"""
Descriptive risk metrics for a currency pair's rate history.
"""

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def daily_changes(df: pd.DataFrame) -> pd.Series:
    return df["Rate"].pct_change().dropna()


def historical_volatility(df: pd.DataFrame) -> float:
    r = daily_changes(df)
    if r.empty:
        return None
    return round(float(r.std() * np.sqrt(TRADING_DAYS_PER_YEAR) * 100), 2)


def max_drawdown(df: pd.DataFrame) -> float:
    rates = df["Rate"]
    if rates.empty:
        return None
    running_max = rates.cummax()
    drawdown = (rates - running_max) / running_max
    return round(float(drawdown.min() * 100), 2)


def correlation_between(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
    r1 = daily_changes(df1).reset_index(drop=True)
    r2 = daily_changes(df2).reset_index(drop=True)
    n = min(len(r1), len(r2))
    if n < 2:
        return None
    return round(float(np.corrcoef(r1.iloc[-n:], r2.iloc[-n:])[0][1]), 2)


def risk_summary(df: pd.DataFrame) -> dict:
    return {
        "historical_volatility_pct": historical_volatility(df),
        "max_drawdown_pct": max_drawdown(df),
        "methodology": f"Annualized over {TRADING_DAYS_PER_YEAR} business days "
                        "(weekends/holidays excluded, matching ECB publishing schedule).",
    }
