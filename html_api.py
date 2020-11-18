from bottle import route, run, template, request, post, get, delete, put
import sql
import random

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
        return "failed"
    portfolio_id = random.randint(0, 255)
    while portfolio_id in portfolioSet:
        portfolio_id = random.randint(0, 255)
    portfolioSet.add(portfolio_id)
    sql.insert_userdata(email, name, password, portfolio_id)
    return "success"


@delete("/account")
def delete_account():
    email = request.forms.get('email')
    if not email:
        return "failed"
    accounts = sql.query_userdata(email)
    for account in accounts:
        portfolioId = account[3]
        portfolioSet.remove(portfolioId)
        sql.delete_portfolio(portfolioId)
    sql.delete_userdata(email)
    return "success"


@get("/portfolio/<id>")
def get_stocks_in_portfolio(id):
    portfolio = sql.query_portfolio(id)
    print(portfolio)
    for entry in portfolio:
        yield str.encode(entry[1] + "\n")


@get("/stocks")
def get_ticker():
    ticker = request.params.get('ticker')
    print(ticker)
    stock_info = sql.query_stockinfo(ticker)
    stock_data = sql.query_stockprice(ticker)
    d = {'stock-info': {
        'ticker': stock_info[0][0],
        'company-name': stock_info[0][1],
        'market-cap': stock_info[0][2]
    },
        'stock-data': {}}
    for data in stock_data:
        time = data[5].strftime("%Y-%m-%d")
        d['stock-data'][time] = {'open': data[1], 'close': data[2], 'low': data[3], 'high': data[4]}
    return d


run(host='localhost', port=8080)
