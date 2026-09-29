"""
Terminal-based chart rendering - pure Python, zero external dependencies.
"""


def _is_missing(v):
    """True for None or NaN (pandas rolling calculations produce NaN for early rows)."""
    return v is None or v != v


def _scale(values, height):
    clean = [v for v in values if not _is_missing(v)]
    if not clean:
        return [None] * len(values), 0, 0
    lo, hi = min(clean), max(clean)
    if hi == lo:
        hi = lo + 1
    rows = []
    for v in values:
        if _is_missing(v):
            rows.append(None)
        else:
            rows.append(int(round((v - lo) / (hi - lo) * (height - 1))))
    return rows, lo, hi


def _downsample(values, max_points):
    if len(values) <= max_points:
        return values
    step = len(values) / max_points
    return [values[int(i * step)] for i in range(max_points)]


def plot_line(values, title: str, y_label: str = "", width: int = 90, height: int = 18,
              reference_lines: dict = None):
    values = _downsample(values, width)
    rows, lo, hi = _scale(values, height)

    print()
    print(f"=== {title} ===")

    grid = [[" " for _ in range(len(values))] for _ in range(height)]
    for col, row in enumerate(rows):
        if row is not None:
            grid[row][col] = "*"

    if reference_lines:
        for ref_value, label in reference_lines.items():
            if hi != lo:
                ref_row = int(round((ref_value - lo) / (hi - lo) * (height - 1)))
                if 0 <= ref_row < height:
                    for col in range(len(values)):
                        if grid[ref_row][col] == " ":
                            grid[ref_row][col] = "."

    for row_idx in range(height - 1, -1, -1):
        row_value = lo + (row_idx / (height - 1)) * (hi - lo) if height > 1 else lo
        print(f"{row_value:>10.4f} | " + "".join(grid[row_idx]))

    print(" " * 11 + "+" + "-" * len(values))
    print(f"{'':11} {'Oldest'.ljust(len(values) // 2)}{'Newest'}")
    if y_label:
        print(f"(Y-axis: {y_label})")
    if reference_lines:
        ref_desc = ", ".join(f"{v}={lbl}" for v, lbl in reference_lines.items())
        print(f"(dotted reference lines: {ref_desc})")
    print()


def plot_bar(labels: list, values: list, title: str, max_bar_width: int = 50):
    print()
    print(f"=== {title} ===")

    clean_values = [v if not _is_missing(v) else 0 for v in values]
    max_abs = max((abs(v) for v in clean_values), default=1) or 1
    label_width = max((len(str(l)) for l in labels), default=10)

    for label, value in zip(labels, clean_values):
        bar_len = int(round((abs(value) / max_abs) * max_bar_width))
        bar_char = "#" if value >= 0 else "-"
        bar = bar_char * bar_len
        print(f"{str(label).ljust(label_width)} | {bar} {value:.4f}")
    print()


def plot_rate_history(df, base: str, target: str):
    rates = df["Rate"].tolist()
    plot_line(rates, title=f"{base}/{target} - Rate History (last {len(rates)} business days)",
               y_label=f"1 {base} = ? {target}")


def plot_rsi(df, base: str, target: str):
    rsi = df["RSI_14"].tolist()
    plot_line(rsi, title=f"{base}/{target} - RSI (14)", y_label="RSI",
               reference_lines={70: "Overbought", 30: "Oversold"})


def plot_sentiment_bar(aggregate: dict):
    labels = ["Positive", "Neutral", "Negative"]
    values = [aggregate["positive_pct"], aggregate["neutral_pct"], aggregate["negative_pct"]]
    plot_bar(labels, values, title="Currency News Sentiment Breakdown (%)")


def plot_comparison_bar(names: list, values: list, metric_label: str):
    plot_bar(names, values, title=metric_label)
