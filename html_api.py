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
        return
    portfolio_id = random.randint(0, 255)
    while portfolio_id in portfolioSet:
        portfolio_id = random.randint(0, 255)
    portfolioSet.add(portfolio_id)
    sql.insert_userdata(email, name, password, portfolio_id)


@delete("/account")
def delete_account():
    email = request.forms.get('email')
    if not email:
        return
    accounts = sql.query_userdata(email)
    for account in accounts:
        portfolioId = account[3]
        portfolioSet.remove(portfolioId)
        sql.delete_portfolio(portfolioId)
    sql.delete_userdata(email)


@get("/portfolio/<id>")
def get_stocks_in_portfolio(id):
    portfolio = sql.query_portfolio(id)
    print(portfolio)
    for stock in portfolio:
        ticker = stock[1]
        print(sql.query_stockinfo(ticker))
        print(sql.query_stockprice(ticker))
    # send response


@get("/stocks")
def get_ticker():
    ticker = request.params.get('ticker')
    print(ticker)
    stock_info = sql.query_stockinfo(ticker)
    stock_data = sql.query_stockprice(ticker)
    print(stock_info)
    print(stock_data)
    # send response


run(host='localhost', port=8080)
