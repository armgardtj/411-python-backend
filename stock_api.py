import requests
import csv
from datetime import datetime
from polygon import RESTClient


def ts_to_datetime(ts):
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d')


def getStockData(from_, to, ticker):
    key = "PKR2KQ0NLBO5RJ22KV0U"
    client = RESTClient(key)
    last_resp = ""
    resp = client.stocks_equities_aggregates(ticker, 1, "day", from_, to, unadjusted=False)
    hist_data = []
    for result in resp.results:
        dt = ts_to_datetime(result["t"])
        #print(dt)
        sub_data = {}
        sub_data["date"] = dt
        sub_data["close"] = result['c']
        sub_data["open"] = result['o']
        sub_data["low"] = result['l']
        sub_data["high"] = result['h']
        hist_data.append(sub_data)
        last_resp =datetime.fromtimestamp(result["t"] / 1000.0).date()
    return hist_data

def getStockInfo(ticker):

    Info = {}
    resp = requests.get("https://api.polygon.io/v1/meta/symbols/"+ticker+"/company?apiKey=PKR2KQ0NLBO5RJ22KV0U")
    try:
        Info['Ticker'] = ticker
        Info['MarketCap'] = resp.json()['marketcap']
        Info['Name'] = resp.json()['name'] 
    except:
        print(ticker+ " cannot be found")
        temp = {}
        return temp
    return Info
    

#print(getStockInfo("NOOO"))
