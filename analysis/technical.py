"""
Technical indicators computed on an exchange-rate time series.
"""

import numpy as np
import pandas as pd


def rates_to_dataframe(history: list) -> pd.DataFrame:
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date": "Date", "rate": "Rate"})
    return df


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["SMA_7"] = df["Rate"].rolling(window=7).mean()
    df["SMA_30"] = df["Rate"].rolling(window=30).mean()
    df["EMA_7"] = df["Rate"].ewm(span=7, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    delta = df["Rate"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI_14"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    df = df.copy()
    ema_fast = df["Rate"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Rate"].ewm(span=slow, adjust=False).mean()
    df["MACD"] = ema_fast - ema_slow
    df["MACD_signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    return df


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    return df


def compute_changes(df: pd.DataFrame) -> dict:
    rates = df["Rate"]
    if len(rates) < 2:
        return {}

    def pct_change_over(n_rows):
        if len(rates) <= n_rows:
            return None
        start = rates.iloc[-n_rows - 1]
        end = rates.iloc[-1]
        return round(100 * (end - start) / start, 2)

    return {
        "daily_change_pct": pct_change_over(1),
        "weekly_change_pct": pct_change_over(5),
        "monthly_change_pct": pct_change_over(21),
        "six_month_change_pct": pct_change_over(126),
    }
