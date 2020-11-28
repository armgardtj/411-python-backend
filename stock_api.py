import requests
import csv
from datetime import datetime
from polygon import RESTClient


def ts_to_datetime(ts):
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

hist_data = []
def getStockData(from_, to, ticker):
    key = "PKR2KQ0NLBO5RJ22KV0U"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        #from_ = "2019-01-01"
        #to = "2020-01-01"
        last_resp = ""
        old_resp = ""
        d1 = datetime.strptime(from_, "%Y-%m-%d").date()
        d2 = datetime.strptime(to, "%Y-%m-%d").date()
        while(d1 < d2):
            old_resp = last_resp
            resp = client.stocks_equities_aggregates("AAPL", 1, "day", from_, to, unadjusted=False)
            
            for result in resp.results:
                dt = ts_to_datetime(result["t"])
                sub_data = {}
                #print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
                sub_data["Date"] = dt
                sub_data["Close"] = result['c']
                sub_data["Open"] = result['o']
                sub_data["Low"] = result['l']
                sub_data["High"] = result['h']
                hist_data.append(sub_data)
                last_resp =datetime.fromtimestamp(result["t"] / 1000.0).date()
            d1 = last_resp
            from_ = last_resp
            if(old_resp == last_resp):
                break
        return hist_data

getStockData("2019-01-01","2020-01-01","AAPL")

