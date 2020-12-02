import requests
import csv
import datetime as dt
from polygon import RESTClient


def getStockData(from_, to, ticker):
    key = "PKR2KQ0NLBO5RJ22KV0U"
    client = RESTClient(key)
    resp = client.stocks_equities_aggregates(ticker, 1, "day", from_, to, unadjusted=False)
    hist_data = []
    for result in resp.results:
        date = (dt.datetime.fromtimestamp(result["t"] / 1000.0).date() + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        sub_data = {}
        sub_data["date"] = date
        sub_data["close"] = result['c']
        sub_data["open"] = result['o']
        sub_data["low"] = result['l']
        sub_data["high"] = result['h']
        hist_data.append(sub_data)
    return hist_data


def getStockInfo(ticker):
    Info = {}
    resp = requests.get("https://api.polygon.io/v1/meta/symbols/" + ticker + "/company?apiKey=PKR2KQ0NLBO5RJ22KV0U")
    try:
        Info['Ticker'] = ticker
        Info['MarketCap'] = resp.json()['marketcap']
        Info['Name'] = resp.json()['name']
    except:
        print(ticker + " cannot be found")
        temp = {}
        return temp
    return Info

# print(getStockData("2019-01-01", "2020-01-01", "AAPL"))
