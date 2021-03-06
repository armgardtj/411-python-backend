from bottle import route, run, template, request, post, get, delete, put, response
import json
import sql
import random
import datetime
import stock_api

from news_api import getData as getNewsData
import neo4j_411

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
    username = request.query.get('username')
    password = request.query.get('password')
    if not username or not password:
        response.status = 400
        return response
    sql.insert_userdata(username, password)
    response.body = json.dumps({'username': username})
    return response


@delete("/account")
def delete_account():
    username = request.query.get('username')
    if not username:
        response.status = 400
        return
    accounts = sql.query_userdata(username)
    for account in accounts:
        portfolioId = account[3]
        portfolioSet.remove(portfolioId)
        sql.delete_portfolio(portfolioId)
    sql.delete_userdata(username)
    return response


@get("/account")
def login_to_account():
    print("login_to_account - starting")
    # this function logs the user in and returns their portfolio IDs - which is their username
    # the user should only have one portfolio ID, but it returns all in the event there are several
    # after this is called, the /portfolio/<id> endpoint should be called to return the tickers
    username = request.query.get('username')
    password = request.query.get('password')
    if not username or not password:
        print("login_to_account - username or pass is null")
        response.status = 400
        return
    accounts = sql.query_login_info(username, password)
    if len(accounts) == 0:
        print("login_to_account - invalid username or pass")
        response.status = 400
        return
    body = []
    for account in accounts:
        body.append(account[0])
    print("login_to_account - returning")
    response.body = json.dumps(body)
    return response


@get("/account/rename")
def rename_account():
    # This function renames the user for UPDATE points
    print('Rename account starting')
    oldName = request.query.get('oldName')
    newName = request.query.get('newName')
    print('OldName:', oldName, 'NewName:', newName)
    sql.rename_userdata(oldName, newName)


@get("/portfolio/<id>")
def get_portfolio_data_by_date(id):
    # this function returns the tickers for a given portfolio ID
    # you may provide a date for the tickers you want to retrieve
    # if no date is given, the most recent date in the database is used
    date = request.query.get('date')
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
def add_ticker_to_portfolio(id, tickerParam=None):
    ticker = tickerParam if tickerParam else request.query.get('ticker')
    company = sql.query_stockinfo(ticker)
    if len(company) == 0:  # need to query stock api
        success = add_ticker_to_db(ticker)
        if not success:
            response.status = 500
            return response
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


def add_ticker_to_db(ticker):
    stock_info = stock_api.getStockInfo(ticker)
    if not stock_info:
        return False
    sql.insert_stockinfo(stock_info['Ticker'], stock_info['Name'], stock_info['MarketCap'])
    #neo4j_411.neo4j_insert_ticker(stock_info['Ticker'])
    end_date = sql.query_stockprice_dates()[0][0] + datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=30)  
    newsApiData = getNewsData(ticker, start_date, end_date)
    for article in newsApiData:
        sql.insert_newsdata(article['title'], article['text'], article['articleDate'][0:10], str(article['sentiment']),
                            ticker, article['link'], article['articleID'])
        #neo4j_411.neo4j_insert_article(article['title'], stock_info['Ticker'])
    stock_data = stock_api.getStockData(start_date, end_date, ticker)
    for d in stock_data:
        sql.insert_stockprice(ticker, d['open'], d['close'], d['low'], d['high'], d['date'])
    return True


@get("/portfolio/<id>/delete")
def remove_ticker_from_portfolio(id):
    ticker = request.query.get('ticker')
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

@get("/stocks/<ticker>/related")
def get_related_stocks(ticker):
    print('Starting GetRelatedStocks')
    resp = neo4j_411.neo4j_get_related_tickers()
    body = []
    for r in resp:
        print(r)
        if ticker not in r:
            continue;
        for s in r:
            if s != ticker:
                body.append(s)
    response.body = json.dumps(body)
    return response


@get("/articles/<ticker>")
def get_articles(ticker):
    start = request.query.get('startDate')
    end = request.query.get('endDate')
    if not start or not end:
        end = sql.query_stockprice_dates()[0][0]
        start = (end - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        end = end.strftime("%Y-%m-%d")
    articles = sql.query_newsdata_by_ticker_and_date(ticker, start, end)
    if len(articles) == 0:
        # add queried articles to database
        newsApiData = getNewsData(ticker, start, end)
        for article in newsApiData:
            sql.insert_newsdata(article['title'], article['text'], article['articleDate'][0:10], str(article['sentiment']),
                                ticker, article['link'], article['articleID'])
    articles = sql.query_newsdata_by_ticker_and_date(ticker, start, end)
    body = []
    for e in articles:
        body.append({
            'title': e[0].decode("utf-8"),
            'contents': e[1].decode("utf-8"),
            'date': e[2].strftime("%Y-%m-%d"),
            'positivity': e[3],
            'ticker': e[4],
            'link': e[5].decode("utf-8"),
            'articleID': e[6]
        })
    response.body = json.dumps(body)
    return response


@get("/articles/big/<ticker>")
def get_big_articles(ticker):
    bigdays = sql.query_bigdays(ticker)
    body = []
    for e in bigdays:
        print(e)
        if not e[8]: 
            print('Continue...')
            continue
        body.append({
            'ticker': e[0],
            'bigdate': e[1].strftime("%Y-%m-%d"),
            'percentdiff': e[2],
            'title': e[3].decode("utf-8"),
            'contents': e[4].decode("utf-8"),
            'articledate': e[5].strftime("%Y-%m-%d"),
            'positivity': e[6],
            'link': e[7].decode("utf-8"),
            'articleID': e[8]
        })
    response.body = json.dumps(body)
    return response

@get("/neo4j")
def get_neo4j():
    ticker = request.query.get('ticker')
    print(neo4j_411.neo4j_get_tickers())
    print(neo4j_411.neo4j_get_articles())
    print(neo4j_411.neo4j_get_related_tickers())

neo4j_411.fake_insert()
print(neo4j_411.neo4j_get_related_tickers())
run(host='localhost', port=8080)

