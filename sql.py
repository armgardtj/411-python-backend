import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="main"
)

cur = db.cursor()


def db_tear():
    cur.execute("DROP TABLE newsdata")
    cur.execute("DROP TABLE stockprice")
    cur.execute("DROP TABLE stockinfo")
    cur.execute("DROP TABLE portfolio")
    cur.execute("DROP TABLE userdata")


def db_init():
    cur.execute(
        "CREATE TABLE newsdata (articleID INT(255), title VARCHAR(255), contents TEXT(65535), articleDate DATE, positivity INT(255), ticker VARCHAR(10), PRIMARY KEY (articleID))")
    cur.execute(
        "CREATE TABLE stockprice (ticker VARCHAR(10), open DOUBLE(255,2), close DOUBLE(255,2), low DOUBLE(255,2), high DOUBLE(255,2), priceDate DATE, PRIMARY KEY (ticker, priceDate))")
    cur.execute(
        "CREATE TABLE stockinfo (ticker VARCHAR(10), companyName VARCHAR(255), marketCap INT(255), PRIMARY KEY (ticker))")
    cur.execute(
        "CREATE TABLE portfolio (portfolioID INT(255), stockTicker VARCHAR(10))")
    cur.execute(
        "CREATE TABLE userdata (email VARCHAR(255), name VARCHAR(255), password VARCHAR(255), portfolioID INT(255), PRIMARY KEY (email))")
    # view stocks page: list all tickers in portfolio, add/remove tickers
    # chart page: show historical stock data and news articles

def db_fake_insert():
    cur.execute("INSERT INTO userdata VALUES (\'test1@email\', \'name\', \'pass\', 1)")
    cur.execute("INSERT INTO userdata VALUES (\'test2@email\', \'nam2\', \'pass2\', 2)")

    cur.execute("INSERT INTO stockinfo VALUES (\'AAPL\', \'Apple Inc\', 1)")
    cur.execute("INSERT INTO stockinfo VALUES (\'GOOG\', \'Google TM\', 2)")
    cur.execute("INSERT INTO stockinfo VALUES (\'MSFT\', \'Microhard\', 3)")

    cur.execute("INSERT INTO stockprice VALUES (\'AAPL\', 12, 13, 14, 15, \'2020-11-05\')")
    cur.execute("INSERT INTO stockprice VALUES (\'AAPL\', 13, 14, 15, 16, \'2020-11-04\')")
    cur.execute("INSERT INTO stockprice VALUES (\'AAPL\', 14, 15, 17, 23498, \'2020-11-03\')")
    cur.execute("INSERT INTO stockprice VALUES (\'GOOG\', 122, 153, 184, 195, \'2020-11-05\')")
    cur.execute("INSERT INTO stockprice VALUES (\'GOOG\', 113, 144, 145, 1896, \'2020-11-04\')")
    cur.execute("INSERT INTO stockprice VALUES (\'GOOG\', 124, 1455, 177, 232498, \'2020-11-03\')")
    cur.execute("INSERT INTO stockprice VALUES (\'MSFT\', 1442, 1325, 1144, 1415, \'2020-11-05\')")
    cur.execute("INSERT INTO stockprice VALUES (\'MSFT\', 1753, 1844, 12165, 84516, \'2020-11-04\')")
    cur.execute("INSERT INTO stockprice VALUES (\'MSFT\', 1474, 1541, 1247, 233456498, \'2020-11-03\')")

    cur.execute("INSERT INTO portfolio VALUES (1, \'AAPL\')")
    cur.execute("INSERT INTO portfolio VALUES (1, \'GOOG\')")
    cur.execute("INSERT INTO portfolio VALUES (2, \'MSFT\')")
    cur.execute("INSERT INTO portfolio VALUES (2, \'GOOG\')")


def query_userdata(email):
    condition = "email=\'" + email + "\'"
    cur.execute("SELECT * FROM userdata WHERE " + condition)
    return cur.fetchall()


def insert_userdata(email, name, password, portfolioId):
    values = "(\'" + email + "\',\'" + name + "\',\'" + password + "\'," + str(portfolioId) + ")"
    cur.execute("INSERT INTO userdata VALUES " + values)
    cur.execute("SELECT * FROM userdata")
    for x in cur:
        print(x)


def delete_userdata(email):
    condition = "email=\'" + email + "\'"
    cur.execute("DELETE FROM userdata WHERE " + condition)
    cur.execute("SELECT * FROM userdata")
    for x in cur:
        print(x)


def query_portfolio(portfolioID):
    condition = "portfolioID=" + str(portfolioID) + ""
    cur.execute("SELECT * FROM portfolio WHERE " + condition)
    return cur.fetchall()


def insert_portfolio(portfolioID, stockTicker):
    values = "(" + str(portfolioID) + ",\'" + stockTicker + "\')"
    cur.execute("INSERT INTO portfolio VALUES " + values)
    cur.execute("SELECT * FROM portfolio")
    for x in cur:
        print(x)


def delete_portfolio(portfolioID):
    condition = "portfolioID=" + str(portfolioID) + ""
    cur.execute("DELETE FROM portfolio WHERE " + condition)
    cur.execute("SELECT * FROM portfolio")
    for x in cur:
        print(x)


def query_stockinfo(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("SELECT * FROM stockinfo WHERE " + condition)
    return cur.fetchall()


def insert_stockinfo(ticker, companyName, marketCap):
    values = "(\'" + ticker + "\',\'" + companyName + "\'," + marketCap + ")"
    cur.execute("INSERT INTO stockinfo VALUES " + values)
    cur.execute("SELECT * FROM stockinfo")
    for x in cur:
        print(x)


def update_stockinfo(ticker, companyName):
    update = "companyName = \'" + companyName + "\'"
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("UPDATE stockinfo SET " + update + " WHERE " + condition)
    cur.execute("SELECT * FROM stockinfo")
    for x in cur:
        print(x)


def delete_stockinfo(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("DELETE FROM stockinfo WHERE " + condition)
    cur.execute("SELECT * FROM stockinfo")
    for x in cur:
        print(x)


def query_stockprice(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("SELECT * FROM stockprice WHERE " + condition)
    return cur.fetchall()


def insert_stockprice(ticker, open, close, low, high, priceDate):
    values = "(\'" + ticker + "\'," + open + "," + close + "," + low + "," + high + ",\'" + priceDate + "\')"
    cur.execute("INSERT INTO stockprice VALUES " + values)
    cur.execute("SELECT * FROM stockprice")
    for x in cur:
        print(x)


def delete_stockprice(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("DELETE FROM stockprice WHERE " + condition)
    cur.execute("SELECT * FROM stockprice")
    for x in cur:
        print(x)


def query_newsdata(articleID):
    condition = "articleID=" + str(articleID) + ""
    cur.execute("SELECT * FROM newsdata WHERE " + condition)
    return cur.fetchall()


def query_newsdata_by_ticker(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("SELECT * FROM newsdata WHERE " + ticker)
    return cur.fetchall()


def insert_newsdata(articleID, title, contents, articleDate, positivity, ticker):
    values = "(" + str(articleID) + ",\'" + title + "\',\'" + contents + "\',\'" + articleDate + "\'," + positivity + ",\'" + ticker + "\')"
    cur.execute("INSERT INTO newsdata VALUES " + values)
    cur.execute("SELECT * FROM newsdata")
    for x in cur:
        print(x)


def delete_newsdata(articleID):
    condition = "articleID=" + str(articleID) + ""
    cur.execute("DELETE FROM newsdata WHERE " + condition)
    cur.execute("SELECT * FROM newsdata")
    for x in cur:
        print(x)


db_tear()
db_init()
db_fake_insert()
cur.execute("SHOW TABLES")
for x in cur:
    print(x)
