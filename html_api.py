from bottle import route, run, template, request, post, get, delete, put, response
import json
import sql
import random
import datetime

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


@put("/portfolio/<id>")
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


@delete("/portfolio/<id>")
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
    articles = sql.query_all_articles()
    body = []
    for e in articles:
        body.append({
            'articleID': e[0],
            'title': e[1],
            'contents': e[2],
            'date': e[3].strftime("%Y-%m-%d"),
            'positivity': e[4],
            'ticker': e[5],
        })
    response.body = json.dumps(body)
    return response


run(host='localhost', port=8080)
