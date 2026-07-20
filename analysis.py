import pandas as pd
import os
import sqlite3
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# making sure that fomc_sp500.db is created in the same folder with our main.py file
folder_name = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder_name, "fomc_sp500.db")
connection = sqlite3.connect(db_path)

# testing if we have the db, if we have it getting data from sql
try:
    sp500_from_db = pd.read_sql("SELECT * FROM sp500_close", connection)
    fomc_from_db = pd.read_sql("SELECT * FROM fomc_dates", connection)
except Exception:
    print("Could not fetch the data. Please run 'fetch_data.py'")
    exit()

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
