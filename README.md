# FOMC Meetings and S&P 500 Volatility — An Event Study

This project examines whether S&P 500 return volatility differs before and 
after FOMC (Federal Reserve) meetings, using an event study approach.

## Research Question
Do FOMC meetings affect short-term S&P 500 volatility? Specifically, is the 
volatility in the 5 trading days *before* a meeting different from the 5 
trading days *after*?

## Data & Tools
- **Data:** S&P 500 daily closing prices (Yahoo Finance) and FOMC meeting 
  dates (2014–2025, 96 meetings), stored in and queried from a local SQLite 
  database.
- **Tech stack:** Python, pandas, yfinance, sqlite3, scipy, numpy, matplotlib
- **Data pipeline:** Data is pulled from Yahoo Finance, written to a local 
  SQLite database, then queried back into pandas for analysis — mirroring a 
  realistic data workflow.

## Result (short version)
No statistically significant difference in volatility was found between 
pre- and post-meeting windows (p = 0.36).

📄 **[Read the full research report](report.md)** for methodology, findings, 
graphs, and interpretation.