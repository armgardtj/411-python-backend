import requests
import json
import nltk

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity, opinion_lexicon
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import treebank

# This code is shoving the positive and negative words list into a dictionary
# since we can get O(1) runtime on checking if an element exists in a dict.
# the 'in' keyword traverses things as linked lists has has O(n) runtime on checking
# if elements exist.
positive_words = {}
negative_words = {}
for word in opinion_lexicon.positive():
    positive_words[word] = 1
for word in opinion_lexicon.negative():
    negative_words[word] = 1
def getData(ticker, startDate, endDate):
    if ticker == None or startDate == None or endDate == None:
        raise Exception("One of the parameters to this function is None.")

    url = ('https://newsapi.org/v2/everything?'
    'q='+ticker+
    '&apiKey=9c5df86e319b4acba568a959e37fd639')
    response = requests.get(url)
    d = response.json()

    all_articles_from_api = d['articles']
    # print("-------------------------------------------------------------------")
    progress = 0.0
    all_articles = []
    for article in all_articles_from_api:
        publisher = article['source']['name']
        author = article['author']
        title = article['title']
        publishedAt = article['publishedAt']
        link = article['url']
        text = article['content']
        try:
            sentiment = evaluate_sentence(text)
        except Exception as e:
            print(e)
            print("You dont have the opinion_lexicon downloaded, so I'll just do that for you.")
            print(" -Danny")
            nltk.download('opinion_lexicon')
            sentiment = evaluate_sentence(text)

        to_table = {
                'title' : title,
                'link' : link,
                'text' : text,
                'articleDate' : publishedAt,
                'sentiment' : sentiment
        }
        all_articles.append(to_table)

        progress+= 1
        print(100*progress/len(all_articles_from_api))
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
        try:
            pos_words += positive_words[word]
        except:
            pass
        try:
            neg_words += negative_words[word]
        except:
            pass
        # if word in opinion_lexicon.positive():
        #     pos_words += 1
        # elif word in opinion_lexicon.negative():
        #     neg_words += 1

    if pos_words > neg_words:
        return "Positive"
    elif pos_words < neg_words:
        return "Negative"
    elif pos_words == neg_words:
        return "Neutral"



if __name__ == '__main__':
    ticker = "AAPL"
    startDate = "2020-10-05"
    endDate = "2020-10-15"
    data_return = getData(ticker, startDate, endDate)
    print(data_return)
    print('--------------------------------------------------------------------------------------------------------')
    print(data_return[0])
