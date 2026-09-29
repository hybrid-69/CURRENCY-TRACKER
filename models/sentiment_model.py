"""
Lightweight sentiment model for macroeconomic/currency news, using VADER
extended with a forex-specific lexicon.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

_FOREX_LEXICON = {
    "rate hike": -1.0,
    "rate cut": -0.5,
    "interest rate hike": 1.5,
    "interest rate cut": -1.5,
    "inflation surge": -2.5,
    "inflation cools": 1.8,
    "inflation eases": 1.8,
    "depreciation": -2.3,
    "depreciates": -2.0,
    "appreciation": 2.3,
    "appreciates": 2.0,
    "weakens": -1.8,
    "strengthens": 1.8,
    "record low": -2.3,
    "record high": 2.0,
    "intervention": -0.8,
    "recession": -2.5,
    "trade deficit": -1.5,
    "trade surplus": 1.5,
    "current account deficit": -1.3,
    "forex reserves rise": 1.5,
    "forex reserves fall": -1.5,
    "devaluation": -2.8,
    "quantitative easing": -1.0,
    "capital outflow": -1.8,
    "capital inflow": 1.8,
    "downgrade": -2.0,
    "upgrade": 2.0,
}
_analyzer.lexicon.update(_FOREX_LEXICON)


def analyze_headline(text: str) -> dict:
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.15:
        label = "positive"
    elif compound <= -0.15:
        label = "negative"
    else:
        label = "neutral"

    return {
        "text": text,
        "positive": scores["pos"],
        "neutral": scores["neu"],
        "negative": scores["neg"],
        "compound": compound,
        "label": label,
    }


def analyze_headlines(headlines: list) -> list:
    return [analyze_headline(h["title"]) for h in headlines]


def aggregate_sentiment(analyzed: list) -> dict:
    if not analyzed:
        return {"positive_pct": 0.0, "neutral_pct": 0.0, "negative_pct": 0.0,
                "n_headlines": 0, "overall_label": "no_data"}

    counts = {"positive": 0, "neutral": 0, "negative": 0}
    for item in analyzed:
        counts[item["label"]] += 1

    n = len(analyzed)
    positive_pct = round(100 * counts["positive"] / n, 1)
    neutral_pct = round(100 * counts["neutral"] / n, 1)
    negative_pct = round(100 * counts["negative"] / n, 1)

    if positive_pct >= negative_pct and positive_pct >= neutral_pct:
        overall = "positive"
    elif negative_pct >= positive_pct and negative_pct >= neutral_pct:
        overall = "negative"
    else:
        overall = "neutral"

    return {
        "positive_pct": positive_pct,
        "neutral_pct": neutral_pct,
        "negative_pct": negative_pct,
        "n_headlines": n,
        "overall_label": overall,
    }
