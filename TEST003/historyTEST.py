import yfinance as yf
import csv
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

tsmc = yf.Ticker("2330.TW")
data = tsmc.history(start='2021-01-01', end='2021-10-31')
print(data)
with open('2330.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    """
    for row in reader:
        print(row)
    """
    dictReader = csv.DictReader(csvfile)
    for row in dictReader:
        print(row['Date'], row['Close'])
df = pd.read_csv ('2330.csv', usecols=['Date', 'Close'])
data = pd.DataFrame(df)
print(df)
print(data)
plt.plot(df['Close'])
plt.show()
with open('2330.csv', newline='') as csvfile:
    old = df = pd.read_csv ('2330.csv')
    fig = go.Figure(data=go.Ohlc(x=old['Date'],
                    open=old['Open'],
                    high=old['High'],
                    low=old['Low'],
                    close=old['Close']))
    fig.show()
    
# data.to_csv('2330.csv')