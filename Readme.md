[README.md](https://github.com/user-attachments/files/32817122/README.md)

# 💱 Currency Exchange Rate Tracker

A Python-based command-line currency tracker and analysis tool that provides **live exchange rates, historical data, technical indicators, risk analysis, currency comparison, news sentiment, watchlists, and rate targets**.

The project uses the **Frankfurter API**, backed by European Central Bank reference rates, for exchange-rate data and **Google News RSS** for currency-related headlines.

> **Note:** This project is for educational and informational purposes only. It is not financial advice and its analysis should not be treated as a prediction of future currency prices.

---

## ✨ Features

### 💵 Live Exchange Rates
- Fetches current exchange rates using the Frankfurter API.
- Supports currency pairs such as:
  - `USD/INR`
  - `EUR/USD`
  - `GBP/INR`
  - `USD/JPY`
- Displays the rate date provided by the API.

### 📈 Historical Exchange Rates
- Retrieves up to **180 days** of historical exchange-rate data by default.
- Uses ECB reference-rate data through Frankfurter.
- Displays historical rate charts directly in the terminal.

### 📊 Technical Analysis
The project calculates several commonly used technical indicators:

- **7-day Simple Moving Average (SMA)**
- **30-day Simple Moving Average (SMA)**
- **7-day Exponential Moving Average (EMA)**
- **14-period Relative Strength Index (RSI)**
- **MACD**
- MACD Signal Line
- Daily percentage change
- Weekly percentage change
- Monthly percentage change
- Six-month percentage change

### ⚠️ Risk Analysis
The tracker provides descriptive historical risk metrics including:

- Annualized historical volatility
- Maximum drawdown
- Correlation between currency pairs
- Daily percentage-return analysis

Historical volatility is annualized using **252 business days**.

### 📰 Currency News & Sentiment
- Retrieves recent currency-related headlines through Google News RSS.
- Performs lightweight sentiment analysis using **VADER Sentiment**.
- Includes a custom forex-focused sentiment lexicon.
- Classifies headlines as:
  - Positive
  - Neutral
  - Negative
- Provides an aggregate sentiment breakdown.

> Sentiment is a lexicon-based model output and is **not a currency-rate prediction**.

### 🔎 Currency Search
Search supported currencies by:

- Currency code
- Currency name
- Region

Example searches:

```text
USD
Indian Rupee
Asia
```

### 🔄 Currency Converter
Convert an amount from one supported currency to another using the latest available exchange rate.

Example:

```text
100 USD → INR
```

### 📋 Currency Comparison
Compare multiple target currencies against a selected base currency.

The comparison includes:

- Current exchange rate
- 1-month percentage change
- 6-month percentage change
- Correlation matrix based on daily rate changes
- Optional six-month comparison chart

### ⭐ Watchlist
Add currency pairs to a local watchlist and view their current rates later.

### 🎯 Rate Targets
Create rate targets for currency pairs and check whether the current rate has crossed the target.

Supported conditions:

```text
above
below
```

Example:

```text
USD/INR
Target: 90
Condition: above
```

### 💾 Local Caching & Storage
The project uses local JSON files for:

- API response caching
- Watchlists
- Rate targets

Caching helps reduce unnecessary API requests during repeated use.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Requests | HTTP/API requests |
| Pandas | Data processing and analysis |
| NumPy | Numerical calculations |
| VADER Sentiment | News sentiment analysis |
| Feedparser | Google News RSS parsing |
| Tabulate | Terminal tables |
| Frankfurter API | Exchange-rate data |
| Google News RSS | Currency-related news |

---

## 📁 Project Structure

```text
currency-tracker/
│
├── app.py
├── requirements.txt
│
├── analysis/
│   ├── __init__.py
│   ├── technical.py
│   ├── risk.py
│   └── targets.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── currency_mapping.csv
│   └── cache/
│
├── models/
│   ├── __init__.py
│   └── sentiment_model.py
│
├── services/
│   ├── __init__.py
│   ├── exchange_data.py
│   ├── currency_search.py
│   └── news_data.py
│
├── ui/
│   ├── __init__.py
│   └── terminal_charts.py
│
└── utils/
    ├── __init__.py
    └── storage.py
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hybrid-69/Currency-Tracker.git
```

Move into the project directory:

```bash
cd Currency-Tracker
```

---

### 2. Create a virtual environment

It is recommended to use a virtual environment.

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the application

```bash
python app.py
```

You should see the main menu:

```text
============================================================
             CURRENCY EXCHANGE RATE TRACKER
       Live rates via ECB (Frankfurter API)
============================================================

MAIN MENU
1. Search & Analyze a Currency Pair
2. Compare Currencies
3. Currency Converter
4. Watchlist & Rate Targets
5. Exit
```

---

## 🧭 How to Use

### 1. Search & Analyze a Currency Pair

Select:

```text
1. Search & Analyze a Currency Pair
```

You can search for a currency using its code, name, or region.

Example:

```text
Search base currency: usd
```

Then choose the target currency:

```text
Target currency code: INR
```

The application displays:

- Current exchange rate
- Technical indicators
- Rate changes
- Risk analysis
- Recent currency news
- Sentiment analysis

Optional terminal charts can also be displayed.

---

### 2. Compare Currencies

Select:

```text
2. Compare Currencies
```

Choose a base currency and enter multiple target currencies.

Example:

```text
Base currency: USD
Targets: INR, EUR, GBP, JPY
```

The application calculates current rates, percentage changes, and correlations.

---

### 3. Currency Converter

Select:

```text
3. Currency Converter
```

Example:

```text
Convert from: USD
Convert to: INR
Amount in USD: 100
```

The application returns the converted amount using the latest available rate.

---

### 4. Watchlist & Rate Targets

Select:

```text
4. Watchlist & Rate Targets
```

Available options:

```text
1. View watchlist
2. Add a rate target/alert
3. Check all targets
4. Clear all targets
5. Back to main menu
```

Rate targets are stored locally and can be checked against the latest available exchange rate.

---

## 📐 Analysis Methodology

### Moving Averages

The project calculates:

```text
SMA 7
SMA 30
EMA 7
```

These are calculated from the historical exchange-rate series.

### RSI

A 14-period RSI is calculated from rate changes.

The terminal chart includes reference levels:

```text
70 → Overbought reference
30 → Oversold reference
```

These levels are analytical references only and should not be interpreted as guaranteed buy/sell signals.

### MACD

The project calculates:

```text
MACD = EMA(12) - EMA(26)
Signal = EMA(9) of MACD
```

### Historical Volatility

Historical volatility is calculated from daily percentage changes and annualized using:

```text
Standard Deviation × √252
```

### Maximum Drawdown

Maximum drawdown measures the largest percentage decline from a previous running maximum in the historical rate series.

### Currency Correlation

Correlation is calculated using daily percentage changes between two currency-rate series.

---

## 🌐 Data Sources

### Exchange Rates

Exchange-rate data is retrieved from **Frankfurter**, a free API backed by European Central Bank reference rates.

No API key is required.

### News

Currency-related headlines are retrieved through **Google News RSS**.

The application searches for currency-pair-related news and then analyzes the returned headlines using VADER with a forex-specific lexicon.

---

## ⚙️ Configuration

Project configuration is located in:

```text
config/settings.py
```

Important settings include:

```python
DEFAULT_HISTORY_DAYS = 180
MAX_HEADLINES = 10
CACHE_TTL_SECONDS = 900
```

The project also defines local paths for:

- Currency mapping
- Cached API responses
- User data

---

## 📦 Dependencies

The project uses the following Python packages:

```text
requests
pandas
numpy
feedparser
vaderSentiment
tabulate
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔐 API Keys

No API key is required for the exchange-rate functionality.

The project uses:

- Frankfurter API for exchange-rate data
- Google News RSS for news headlines

---

## 🗃️ Local Data

The application can create local files for user-specific data and cached API responses.

These may include:

```text
data/cache/
data/user_data.json
```

`user_data.json` stores information such as:

- Watchlist pairs
- Rate targets

---

## 🧪 Example Workflow

A typical session can look like:

```text
1. Search & Analyze a Currency Pair
        ↓
Search for USD
        ↓
Select INR
        ↓
Fetch current + historical rates
        ↓
Calculate technical indicators
        ↓
Calculate risk metrics
        ↓
Fetch recent news
        ↓
Analyze sentiment
        ↓
Display terminal charts
        ↓
Optionally add USD/INR to watchlist
```

---

## ⚠️ Limitations

- Exchange-rate data depends on the availability of the external API.
- Frankfurter provides ECB reference-rate data, which may not represent real-time market trading prices.
- Historical data follows the available reference-rate publishing schedule.
- News sentiment is based on a lightweight lexicon-based model.
- Sentiment results can be affected by headline wording and context.
- Technical indicators describe historical data and do not guarantee future performance.
- Rate targets are checked when the user manually checks them; they are not a background notification system.

---

## 🔮 Future Improvements

Possible future improvements include:

- [ ] Web-based dashboard
- [ ] Interactive charts
- [ ] More technical indicators
- [ ] Better NLP/transformer-based sentiment analysis
- [ ] Automatic scheduled rate alerts
- [ ] Email or Telegram notifications
- [ ] More currency and historical-data providers
- [ ] Portfolio tracking
- [ ] Export analysis to CSV/PDF
- [ ] Unit tests and automated CI
- [ ] Docker support
- [ ] REST API
- [ ] Database-backed storage

---

## 👨‍💻 Author

**Vansh Choudhary**

GitHub:  
https://github.com/hybrid-69

Project Repository:  
https://github.com/hybrid-69/Currency-Tracker

---

## 📄 License

This project currently does not specify a license.

If you want other people to legally reuse, modify, and distribute the project, consider adding an appropriate open-source license such as the MIT License.

---

## ⭐ Contributing

Contributions and suggestions are welcome.

A typical contribution workflow:

```bash
# Fork the repository

# Create a feature branch
git checkout -b feature/your-feature

# Make your changes

# Commit your changes
git add .
git commit -m "Add your feature"

# Push the branch
git push origin feature/your-feature

# Open a Pull Request on GitHub
```

---

## 📌 Disclaimer

This project is intended for **learning, experimentation, and informational purposes**.

The exchange rates, historical analysis, technical indicators, risk metrics, and news sentiment provided by this application should not be considered financial advice or a recommendation to buy, sell, or trade any currency or financial instrument.
