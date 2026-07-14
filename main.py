import pandas as pd
import yfinance as yf
import os
import sqlite3
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt


# We are pulling S&P 500 Data from Yfinance API
df_sp500 = yf.download(["^GSPC"], start="2013-06-01", end="2026-01-01")

# These are all the dates FED meetings took place between 2014-2026
fomc_dates_list = [
    # 2014
    "2014-01-29", "2014-03-19", "2014-04-30", "2014-06-18",
    "2014-07-30", "2014-09-17", "2014-10-29", "2014-12-17",
    # 2015
    "2015-01-28", "2015-03-18", "2015-04-29", "2015-06-17",
    "2015-07-29", "2015-09-17", "2015-10-28", "2015-12-16",
    # 2016
    "2016-01-27", "2016-03-16", "2016-04-27", "2016-06-15",
    "2016-07-27", "2016-09-21", "2016-11-02", "2016-12-14",
    # 2017
    "2017-02-01", "2017-03-15", "2017-05-03", "2017-06-14",
    "2017-07-26", "2017-09-20", "2017-11-01", "2017-12-13",
    # 2018
    "2018-01-31", "2018-03-21", "2018-05-02", "2018-06-13",
    "2018-08-01", "2018-09-26", "2018-11-08", "2018-12-19",
    # 2019
    "2019-01-30", "2019-03-20", "2019-05-01", "2019-06-19",
    "2019-07-31", "2019-09-18", "2019-10-30", "2019-12-11",
    # 2020
    "2020-01-29", "2020-03-15", "2020-04-29", "2020-06-10",
    "2020-07-29", "2020-09-16", "2020-11-05", "2020-12-16",
    # 2021
    "2021-01-27", "2021-03-17", "2021-04-28", "2021-06-16",
    "2021-07-28", "2021-09-22", "2021-11-03", "2021-12-15",
    # 2022
    "2022-01-26", "2022-03-16", "2022-05-04", "2022-06-15",
    "2022-07-27", "2022-09-21", "2022-11-02", "2022-12-14",
    # 2023
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14",
    "2023-07-26", "2023-09-20", "2023-11-01", "2023-12-13",
    # 2024
    "2024-01-31", "2024-03-20", "2024-05-01", "2024-06-12",
    "2024-07-31", "2024-09-18", "2024-11-07", "2024-12-18",
    # 2025
    "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18",
    "2025-07-30", "2025-09-17", "2025-10-29", "2025-12-10",
]

# We are turning "fomc_dates_list" list to dataframe
df_fomc_dates = pd.DataFrame(fomc_dates_list, columns=["FOMC_dates"])

# We are first turning S&P 500 Close data to series, and then make index a separate column
df_sp500 = df_sp500["Close"].squeeze().reset_index()

# Renaming Column
df_sp500.rename(columns={"^GSPC": "sp500_close"}, inplace=True)

# making sure that fomc_sp500.db is created in the same folder with our main.py file
folder_name = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder_name, "fomc_sp500.db")
connection = sqlite3.connect(db_path)

# Uploading data to sql for both dataframes
df_fomc_dates.to_sql('fomc_dates', connection,
                     if_exists="replace", index=False)
df_sp500.to_sql('sp500_close', connection, if_exists="replace", index=False)

# getting data back from sql
sp500_from_db = pd.read_sql("SELECT * FROM sp500_close", connection)
fomc_from_db = pd.read_sql("SELECT * FROM fomc_dates", connection)

# Changing Date colum data type into datetime
sp500_from_db["Date"] = pd.to_datetime(sp500_from_db["Date"])
fomc_from_db["FOMC_dates"] = pd.to_datetime(fomc_from_db["FOMC_dates"])

# We are first setting Date column to Index and calculating daily yield for S&P 500
sp500_from_db.set_index("Date", inplace=True)
sp500_from_db_daily_yield = sp500_from_db["sp500_close"].pct_change()
sp500_from_db_daily_yield = sp500_from_db_daily_yield.dropna()

# Statistical Calculations
pre_vol = []
post_vol = []

for date in fomc_from_db["FOMC_dates"]:
    pos = sp500_from_db_daily_yield.index.get_indexer(
        [date], method='nearest')[0]
    pre = sp500_from_db_daily_yield.iloc[pos-5: pos]
    post = sp500_from_db_daily_yield.iloc[pos+1: pos+6]
    pre_vol.append(pre.std())
    post_vol.append(post.std())

pre_vol_avg = np.mean(pre_vol)
post_vol_avg = np.mean(post_vol)
t_test = ttest_ind(pre_vol, post_vol, equal_var=False)
print(f"Pre Average Volatility: {pre_vol_avg}")
print(f"Post Average Volatility: {post_vol_avg}")
print(f"Welch T-test P-value: {t_test.pvalue}")

# Graphic
folder_name = os.path.dirname(os.path.abspath(__file__))
# Bar Graphic
plt.figure()
plt.bar(["Pre-Meeting", "Post-Meeting"], [pre_vol_avg, post_vol_avg])
plt.title("Average S&P 500 Volatility: Pre vs Post FOMC Meetings")
plt.ylabel("Volatility (Std. Dev. of Daily Returns)")
plt.savefig(os.path.join(folder_name, "bar_chart.png"))

# Box Plot
plt.figure()
plt.boxplot([pre_vol, post_vol], tick_labels=["Pre-Meeting", "Post-Meeting"])
plt.title("Distribution of S&P 500 Volatility: Pre vs Post FOMC Meetings")
plt.ylabel("Volatility (Std. Dev. of Daily Returns)")
plt.savefig(os.path.join(folder_name, "box_plot.png"))

plt.show()
