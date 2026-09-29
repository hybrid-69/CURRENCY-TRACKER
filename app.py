"""
Currency Exchange Rate Tracker - CLI version
Run with: python app.py
Data: Frankfurter API (ECB reference rates) - free, no API key needed.
"""

from tabulate import tabulate

from services.currency_search import CurrencySearch
from services.exchange_data import get_latest_rate, get_historical_rates, convert_amount, \
    ExchangeDataError
from services.news_data import get_currency_news
from models.sentiment_model import analyze_headlines, aggregate_sentiment
from analysis.technical import rates_to_dataframe, compute_all_indicators, compute_changes
from analysis.risk import risk_summary, correlation_between
from analysis.targets import check_targets
from utils.storage import add_to_watchlist, get_watchlist, add_target, get_targets, clear_targets
from ui.terminal_charts import plot_rate_history, plot_rsi, plot_sentiment_bar, plot_comparison_bar

search_engine = CurrencySearch()


def header(title: str):
    print()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def prompt_currency_code(label: str) -> str:
    while True:
        raw = input(f"{label} (e.g. USD, INR, EUR): ").strip().upper()
        if search_engine.is_valid_code(raw):
            return raw
        print(f"'{raw}' isn't in the supported currency list. Try again "
              "(type a 3-letter code like USD, INR, GBP).")


def show_pair_detail(base: str, target: str):
    header(f"{base} / {target}")

    try:
        quote = get_latest_rate(base, target)
    except ExchangeDataError as e:
        print(f"[ERROR] {e}")
        return
    print(f"As of {quote['date']}: 1 {base} = {quote['rate']} {target}")

    try:
        history = get_historical_rates(base, target)
    except ExchangeDataError as e:
        print(f"[ERROR] {e}")
        return

    df = rates_to_dataframe(history)
    df = compute_all_indicators(df)
    latest = df.iloc[-1]

    print("\n--- Technical Indicators (latest) ---")
    tech_rows = [
        ["SMA 7", round(latest["SMA_7"], 4) if latest["SMA_7"] == latest["SMA_7"] else "N/A"],
        ["SMA 30", round(latest["SMA_30"], 4) if latest["SMA_30"] == latest["SMA_30"] else "N/A"],
        ["RSI (14)", round(latest["RSI_14"], 2) if latest["RSI_14"] == latest["RSI_14"] else "N/A"],
        ["MACD", round(latest["MACD"], 4) if latest["MACD"] == latest["MACD"] else "N/A"],
    ]
    print(tabulate(tech_rows, headers=["Indicator", "Value"], tablefmt="simple"))

    if input("\nShow rate history chart? (y/n): ").strip().lower() == "y":
        plot_rate_history(df, base, target)
    if input("Show RSI chart? (y/n): ").strip().lower() == "y":
        plot_rsi(df, base, target)

    print("\n--- Rate Changes ---")
    changes = compute_changes(df)
    change_rows = [[k.replace("_pct", "").replace("_", " ").title(),
                     f"{v}%" if v is not None else "N/A"] for k, v in changes.items()]
    print(tabulate(change_rows, tablefmt="simple"))

    print("\n--- Risk Analysis ---")
    risk = risk_summary(df)
    for k, v in risk.items():
        print(f"{k.replace('_', ' ').title()}: {v}")

    print("\n--- Recent News & Sentiment ---")
    headlines = get_currency_news(base, target)
    if not headlines:
        print("No recent headlines found.")
    else:
        analyzed = analyze_headlines(headlines)
        agg = aggregate_sentiment(analyzed)
        for h, a in zip(headlines, analyzed):
            tag = {"positive": "[+]", "neutral": "[ ]", "negative": "[-]"}[a["label"]]
            print(f"{tag} {h['title']}  ({a['label']}, {a['compound']:+.2f})")
        print(f"\nAggregate: {agg['positive_pct']}% positive | {agg['neutral_pct']}% neutral | "
              f"{agg['negative_pct']}% negative -> overall: {agg['overall_label'].upper()}")
        print("Note: sentiment is model output (lexicon-based), not a rate prediction.")
        if input("\nShow sentiment chart? (y/n): ").strip().lower() == "y":
            plot_sentiment_bar(agg)

    print()
    if input("Add this pair to your watchlist? (y/n): ").strip().lower() == "y":
        add_to_watchlist(base, target)
        print(f"Added {base}/{target} to watchlist.")


def menu_search():
    header("SEARCH & ANALYZE A CURRENCY PAIR")
    print("Search a currency by code, name, or region (e.g. 'usd', 'rupee', 'asia').")
    query = input("Search base currency: ").strip()
    results = search_engine.search(query) if query else search_engine.df.iloc[0:0]

    if results.empty:
        print("No matches. You can still type an exact 3-letter code directly below.")
        base = prompt_currency_code("Base currency code")
    else:
        print(f"\n{len(results)} match(es):\n")
        rows = [[i + 1, r["code"], r["name"], r["region"]] for i, r in results.iterrows()]
        print(tabulate(rows, headers=["#", "Code", "Name", "Region"], tablefmt="simple"))
        choice = input("\nEnter number to select, or type a code directly: ").strip()
        try:
            base = results.iloc[int(choice) - 1]["code"]
        except (ValueError, IndexError):
            base = choice.upper() if search_engine.is_valid_code(choice.upper()) else \
                prompt_currency_code("Base currency code")

    target = prompt_currency_code("Target currency code")
    if base == target:
        print("Base and target can't be the same currency.")
        return

    show_pair_detail(base, target)


def menu_compare():
    header("COMPARE CURRENCIES AGAINST A BASE")
    base = prompt_currency_code("Base currency")
    print("Enter 2-5 target currency codes, separated by commas (e.g. INR, EUR, GBP, JPY).")
    raw = input("Targets: ").strip().upper()
    targets = [t.strip() for t in raw.split(",") if t.strip()]
    targets = [t for t in targets if search_engine.is_valid_code(t) and t != base]

    if len(targets) < 2:
        print("Need at least 2 valid target currencies.")
        return

    rows = []
    dataframes = {}
    six_month_changes = []
    for target in targets:
        try:
            quote = get_latest_rate(base, target)
            history = get_historical_rates(base, target)
            df = rates_to_dataframe(history)
            dataframes[target] = df
            changes = compute_changes(df)
            rows.append([target, quote["rate"], changes.get("monthly_change_pct"),
                         changes.get("six_month_change_pct")])
            six_month_changes.append(changes.get("six_month_change_pct") or 0)
        except ExchangeDataError as e:
            rows.append([target, "ERROR", str(e), ""])
            six_month_changes.append(0)

    print()
    print(tabulate(rows, headers=[f"1 {base} =", "Rate", "1M Change %", "6M Change %"],
                    tablefmt="simple"))

    if len(dataframes) >= 2:
        print("\n--- Correlation Matrix (daily rate changes) ---")
        pairs = list(dataframes.keys())
        corr_rows = []
        for p1 in pairs:
            row = [p1]
            for p2 in pairs:
                row.append(correlation_between(dataframes[p1], dataframes[p2]))
            corr_rows.append(row)
        print(tabulate(corr_rows, headers=["", *pairs], tablefmt="simple"))

    if input("\nShow 6-month change comparison chart? (y/n): ").strip().lower() == "y":
        plot_comparison_bar(targets, six_month_changes, f"6-Month Change vs {base} (%)")


def menu_converter():
    header("CURRENCY CONVERTER")
    base = prompt_currency_code("Convert from")
    target = prompt_currency_code("Convert to")
    try:
        amount = float(input(f"Amount in {base}: ").strip())
    except ValueError:
        print("Invalid amount.")
        return

    try:
        result = convert_amount(amount, base, target)
    except ExchangeDataError as e:
        print(f"[ERROR] {e}")
        return

    print(f"\n{result['amount']} {base} = {result['converted']} {target} "
          f"(rate: 1 {base} = {result['rate']} {target}, as of {result['date']})")


def menu_watchlist():
    while True:
        header("WATCHLIST & RATE TARGETS")
        print("1. View watchlist (current rates)")
        print("2. Add a rate target/alert")
        print("3. Check all targets")
        print("4. Clear all targets")
        print("5. Back to main menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            watchlist = get_watchlist()
            if not watchlist:
                print("Nothing on your watchlist yet - add pairs from Search & Analyze.")
                continue
            rows = []
            for pair in watchlist:
                base, target = pair.split("/")
                try:
                    quote = get_latest_rate(base, target)
                    rows.append([pair, quote["rate"], quote["date"]])
                except ExchangeDataError as e:
                    rows.append([pair, "ERROR", str(e)])
            print(tabulate(rows, headers=["Pair", "Rate", "Date"], tablefmt="simple"))

        elif choice == "2":
            base = prompt_currency_code("Base currency")
            target = prompt_currency_code("Target currency")
            try:
                target_rate = float(input(f"Target rate (1 {base} = ? {target}): ").strip())
            except ValueError:
                print("Invalid rate.")
                continue
            direction = input("Alert when rate goes (above/below) this value: ").strip().lower()
            if direction not in ("above", "below"):
                print("Must be 'above' or 'below'.")
                continue
            add_target(base, target, target_rate, direction)
            print(f"Target added: alert when {base}/{target} goes {direction} {target_rate}.")

        elif choice == "3":
            targets = get_targets()
            if not targets:
                print("No targets set.")
                continue
            results = check_targets(targets)
            rows = [[f"{r['base']}/{r['target']}", r['direction'], r['target_rate'],
                     r['current_rate'], r['status']] for r in results]
            print(tabulate(rows, headers=["Pair", "Direction", "Target", "Current", "Status"],
                            tablefmt="simple"))

        elif choice == "4":
            if input("Clear all targets? (y/n): ").strip().lower() == "y":
                clear_targets()
                print("Targets cleared.")

        elif choice == "5":
            break
        else:
            print("Invalid option.")


def main():
    print("=" * 60)
    print("CURRENCY EXCHANGE RATE TRACKER".center(60))
    print("Live rates via ECB (Frankfurter API) - not financial advice".center(60))
    print("=" * 60)

    while True:
        print("\nMAIN MENU")
        print("1. Search & Analyze a Currency Pair")
        print("2. Compare Currencies")
        print("3. Currency Converter")
        print("4. Watchlist & Rate Targets")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            menu_search()
        elif choice == "2":
            menu_compare()
        elif choice == "3":
            menu_converter()
        elif choice == "4":
            menu_watchlist()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
