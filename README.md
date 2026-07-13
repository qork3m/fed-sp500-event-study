# FOMC Meetings and S&P 500 Volatility — An Event Study

This project examines whether S&P 500 return volatility differs before and 
after FOMC (Federal Reserve) meetings, using an event study approach.

## Research Question
Do FOMC meetings affect short-term S&P 500 volatility? Specifically, is the 
volatility in the 5 trading days *before* a meeting different from the 5 
trading days *after*?

## Method
- **Data:** S&P 500 daily closing prices (Yahoo Finance) and FOMC meeting 
  dates (2014–2025, 96 meetings), stored in and queried from a local SQLite 
  database.
- **Event windows:** For each FOMC decision date, I compared the standard 
  deviation of daily returns in the 5 trading days before versus the 5 
  trading days after, excluding the decision day itself. Trading-day windows 
  (not calendar days) were used to avoid weekends distorting the sample.
- **Test:** A two-tailed Welch's t-test (no equal-variance assumption).

## Findings
Average post-meeting volatility (0.0092) was slightly higher than 
pre-meeting volatility (0.0082) — the opposite direction one might expect if 
markets fully priced in decisions beforehand. However, the two-tailed 
Welch's t-test returned a p-value of 0.36, far above 0.05, so the difference 
is **not statistically significant**.

With 96 events, the sample is reasonably large, which strengthens confidence 
that this null result reflects a genuine absence of a measurable effect 
rather than insufficient statistical power. A likely interpretation is that 
markets absorb FOMC decisions efficiently, leaving no pronounced shift in 
short-term daily volatility. A limitation is that daily data may miss 
intraday reactions around the announcement itself.

## Tech Stack
Python, pandas, yfinance, sqlite3, scipy, numpy

## Data Pipeline
Data is pulled from Yahoo Finance, written to a local SQLite database, then 
queried back into pandas for the event study analysis — mirroring a realistic 
data workflow.