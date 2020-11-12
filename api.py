import requests
import json

def getData(ticker, startDate, endDate):
    url = ('https://newsapi.org/v2/everything?'
    'q='+ticker+
    '&apiKey=9c5df86e319b4acba568a959e37fd639')
    response = requests.get(url)
    d = response.json()
    print(d)
    post = {}
    article = d['articles'][1]
    #for article in d['articles']:
    post[article['url']] = {'title': article['title'], 'text': article['content'], 'articleDate': article['publishedAt'], 'positivity': 0}

    #p_url = "http://localhost:8080/article"
    #header = {"content-type": "application/json"}
    #p_response = requests.post(p_url,data=json.dumps(post), headers=header, verify=False)
    #return p_response

ticker = "AAPL"
startDate = "2020-10-05"
endDate = "2020-11-04"
print(getData(ticker, startDate, endDate))