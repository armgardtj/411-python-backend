from bottle import route, run, template, request, post, get, delete, put, response
import json
import sql
import random
import datetime

from news_api import getData as getNewsData

portfolioSet = set()
articleSet = set()
frontend_port = 8090
frontend_link = "http://localhost:" + str(frontend_port)


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/account')
def f():
    print('hmm')


@post("/account")
def create_account():
    email = request.forms.get('email')
    name = request.forms.get('name')
    password = request.forms.get('password')
    if not email or not name or not password:
        response.status = 400
        return response
    portfolio_id = random.randint(0, 255)
    while portfolio_id in portfolioSet:
        portfolio_id = random.randint(0, 255)
    portfolioSet.add(portfolio_id)
    sql.insert_userdata(email, name, password, portfolio_id)
    return response


@delete("/account")
def delete_account():
    email = request.forms.get('email')
    if not email:
        response.status = 400
        return
    accounts = sql.query_userdata(email)
    for account in accounts:
        portfolioId = account[3]
        portfolioSet.remove(portfolioId)
        sql.delete_portfolio(portfolioId)
    sql.delete_userdata(email)
    return response


@get("/portfolio/<id>")
def get_portfolio_data_by_date(id):
    date = request.params.get('date')
    if date is None:
        date = sql.query_stockprice_dates()[0][0].strftime("%Y-%m-%d")
    portfolio = sql.query_stockprice_by_portfolio_by_date(id, date)
    body = []
    for e in portfolio:
        body.append({
            'ticker': e[0],
            'company-name': e[1],
            'market-cap': e[2],
            'open': e[3],
            'close': e[4],
            'low': e[5],
            'high': e[6],
            'date': e[7].strftime("%Y-%m-%d"),
        })
    response.body = json.dumps(body)
    return response


@get("/portfolio/<id>/add")
def add_ticker_to_portfolio(id):
    ticker = request.params.get('ticker')
    sql.insert_portfolio(id, ticker)
    date = sql.query_stockprice_dates()[0][0].strftime("%Y-%m-%d")
    portfolio = sql.query_stockprice_by_portfolio_by_date(id, date)
    body = []
    for e in portfolio:
        body.append({
            'ticker': e[0],
            'company-name': e[1],
            'market-cap': e[2],
            'open': e[3],
            'close': e[4],
            'low': e[5],
            'high': e[6],
            'date': e[7].strftime("%Y-%m-%d"),
        })
    response.body = json.dumps(body)
    return response


@get("/portfolio/<id>/delete")
def remove_ticker_from_portfolio(id):
    ticker = request.params.get('ticker')
    sql.delete_ticker_from_portfolio(id, ticker)
    date = sql.query_stockprice_dates()[0][0].strftime("%Y-%m-%d")
    portfolio = sql.query_stockprice_by_portfolio_by_date(id, date)
    body = []
    for e in portfolio:
        body.append({
            'ticker': e[0],
            'company-name': e[1],
            'market-cap': e[2],
            'open': e[3],
            'close': e[4],
            'low': e[5],
            'high': e[6],
            'date': e[7].strftime("%Y-%m-%d"),
        })
    response.body = json.dumps(body)
    return response


@get("/stocks")
def get_stockinfo():
    tickers = sql.query_all_tickers()
    body = []
    for e in tickers:
        body.append(e[0])
    response.body = json.dumps(body)
    return response


@get("/stocks/<ticker>")
def get_stockprice(ticker):
    info = sql.query_stockinfo(ticker)
    prices = sql.query_stockprice(ticker)
    body = {
        'ticker': info[0][0],
        'company-name': info[0][1],
        'market-cap': info[0][2],
        'data': []
    }
    for e in prices:
        body['data'].append({
            'open': e[1],
            'close': e[2],
            'low': e[3],
            'high': e[4],
            'date': e[5].strftime("%Y-%m-%d"),
        })
    response.body = json.dumps(body)
    return response


@get("/articles")
def get_articles():
    print("return all articles")
    articles = sql.query_all_articles()
    body = []
    for e in articles:
        print(e)
        body.append({
            'title': e[0],
            'contents': e[1],
            'date': e[2].strftime("%Y-%m-%d"),
            'positivity': e[3],
            'ticker': e[4],
            'articleID': e[5]
        })
    response.body = json.dumps(body)
    return response

@get("/articles/<ticker>")
def get_articles(ticker, startDate, endDate):
    # query the database for news articles in the date range
    articles = sql.query_newsdata_by_ticker_and_date(ticker, startDate, endDate)
    # if the list is empty, then we have to query the news api and get the data
    if len(articles) == 0:
        # do api query
        newsApiData = getNewsData(ticker, startDate, endDate)
        # insert each result into the articles table
        for article in newsApiData:
            sql.insert_newsdata(article[0], article[1], article[2], article[3], article[4])
        # return the articles
        response.body = json.dumps(newsApiData)
        return response

    else:
        # check the dates of the first and last articles in the returned list
        # TODO: double check that element at idx 3 is actally the date
        startDateArticle = articles[0][3]
        endDateArticle   = articles[-1][3]
        if startDateArticle != startDate:
            # pull the data in date range [startDate, startDateArticle]
            newsApiData = getNewsData(ticker, startDate, startDateArticle)
            for article in newsApiData:
                sql.insert_newsdata(article[0], article[1], article[2], article[3], article[4])
                articles.append(article)
        if endDateArticle != endDate:
            # pull the data in date range [endDateArticle, endDate]
            newsApiData = getNewsData(ticker, endDateArticle, endDate)
            for article in newsApiData:
                sql.insert_newsdata(article[0], article[1], article[2], article[3], article[4])
                articles.append(article)

        response.body = json.dumps(articles)
        return response

run(host='localhost', port=8080)
