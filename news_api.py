import requests
import json
import nltk

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity, opinion_lexicon
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import treebank

def getData(ticker, startDate, endDate):
    url = ('https://newsapi.org/v2/everything?'
    'q='+ticker+
    '&apiKey=9c5df86e319b4acba568a959e37fd639')
    response = requests.get(url)
    d = response.json()

    all_articles_from_api = d['articles']
    # print("-------------------------------------------------------------------")
    all_articles = []
    for article in all_articles_from_api:
        publisher = article['source']['name']
        author = article['author']
        title = article['title']
        publishedAt = article['publishedAt']
        link = article['url']
        text = article['content']
        sentiment = evaluate_sentence(text)

        to_table = {
                'title' : title,
                'link' : link,
                'text' : text,
                'articleDate' : publishedAt,
                'sentiment' : sentiment
        }
        all_articles.append(to_table)
        # exit()
    return all_articles
    # Insert code that pushes all_articles out to the database

    # post[article['url']] = {'title': article['title'], 'text': article['content'], 'articleDate': article['publishedAt'], 'positivity': 0}

    #p_url = "http://localhost:8080/article"
    #header = {"content-type": "application/json"}
    #p_response = requests.post(p_url,data=json.dumps(post), headers=header, verify=False)
    #return p_response
tokenizer = treebank.TreebankWordTokenizer()
def evaluate_sentence(sentence):
    pos_words = 0
    neg_words = 0
    tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]

    for word in tokenized_sent:
        if word in opinion_lexicon.positive():
            pos_words += 1
        elif word in opinion_lexicon.negative():
            neg_words += 1

    if pos_words > neg_words:
        return "Positive"
    elif pos_words < neg_words:
        return "Negative"
    elif pos_words == neg_words:
        return "Neutral"

# nltk.download('opinion_lexicon')
ticker = "AAPL"
startDate = "2020-10-05"
endDate = "2020-11-04"
data_return = getData(ticker, startDate, endDate)
print(data_return)
print('--------------------------------------------------------------------------------------------------------')
print(data_return[0])
