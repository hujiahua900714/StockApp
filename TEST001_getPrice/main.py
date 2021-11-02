from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

def get_latest_closing_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        return data["Close"][0]
    except Exception as e:
        print("Failed to get required data.", e)

def get_closing_prices(symbol, period="1mo"):  # default value of 1 day.
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period)
        return data["Close"]
    except Exception as e:
        print("Failed to get required data.", e)
########################################################
ticker = "2330.TW"  # TSMC
print(f"Latest closing price for {ticker} is: ${get_latest_closing_price(ticker):.2f}")
period = "3y"

prices_data = get_closing_prices(ticker)
print(prices_data)
sns.lineplot(data=prices_data)
sns.set_theme()  # Default seaborn style
plt.xticks(rotation=30) #rotate the word in x-axis
plt.title(f"Closing Stock Prices for {ticker}")
plt.show()
#########################################################
ticker = "0050.TW"  # 0050
print(f"Latest closing price for {ticker} is: ${get_latest_closing_price(ticker):.3f}") 
#float number until the third num after point

prices_data = yf.download('0050.TW', start='2021-10-20', end='2021-11-1')
print(prices_data)

price_data = yf.Ticker("0050.TW").history(start='2021-10-29', end='2021-11-2', interval='1h')['Close']
price_data = yf.download('0050.TW', start='2021-10-29', end='2021-11-2', interval='1h')['Close']
sns.lineplot(data=price_data)
sns.set_theme()
plt.xticks(rotation=30)
plt.title("test01")
plt.show()

price_data = yf.download('0050.TW')['Close']
sns.lineplot(data=price_data)
sns.set_theme()
plt.xticks(rotation=30)
plt.title("test02")
plt.show()
########################################################



