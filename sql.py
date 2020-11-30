import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="main"
)

# The buffered==True I got from stackoverflow.
# it solves a "unread result found" runtime error.
cur = db.cursor(buffered=True)


def db_tear():
    cur.execute("DROP TABLE IF EXISTS newsdata ")
    cur.execute("DROP TABLE IF EXISTS stockprice")
    cur.execute("DROP TABLE IF EXISTS stockinfo")
    cur.execute("DROP TABLE IF EXISTS portfolio")
    cur.execute("DROP TABLE IF EXISTS userdata")


def db_init():
    cur.execute(
        "CREATE TABLE newsdata (title BLOB(255), contents BLOB(65535), articleDate DATE, positivity DOUBLE(255,2), ticker VARCHAR(10), link BLOB(255), articleID INT(255) AUTO_INCREMENT, PRIMARY KEY (articleID))")
    cur.execute(
        "CREATE TABLE stockprice (ticker VARCHAR(10), open DOUBLE(255,2), close DOUBLE(255,2), low DOUBLE(255,2), high DOUBLE(255,2), priceDate DATE, PRIMARY KEY (ticker, priceDate))")
    cur.execute(
        "CREATE TABLE stockinfo (ticker VARCHAR(10), companyName VARCHAR(255), marketCap BIGINT(255), PRIMARY KEY (ticker))")
    cur.execute(
        "CREATE TABLE portfolio (portfolioID VARCHAR(255), stockTicker VARCHAR(10))")
        #
        # portfolioID is just an username from the userdata table that tells us which stocks a user has in their portfolio
        #
    cur.execute(
        "CREATE TABLE userdata (username VARCHAR(255), password VARCHAR(255), PRIMARY KEY (username))")
    # view stocks page: list all tickers in portfolio, add/remove tickers
    # chart page: show historical stock data and news articles


def db_fake_insert():
    cur.execute("INSERT INTO userdata VALUES (\'test1\', \'pass\')")
    cur.execute("INSERT INTO userdata VALUES (\'test2\', \'pass2\')")

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

    cur.execute("INSERT INTO portfolio VALUES (\'test1\', \'AAPL\')")
    cur.execute("INSERT INTO portfolio VALUES (\'test1\', \'GOOG\')")
    cur.execute("INSERT INTO portfolio VALUES (\'test2\', \'MSFT\')")
    cur.execute("INSERT INTO portfolio VALUES (\'test2\', \'GOOG\')")

    # TODO: There are problems with inserting into newsdata
    cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title\', \' good good good good good \', \'2020-10-17\', 1.0, \'AAPL\')")
    cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title1\', \'bad bad bad bad bad bad bad \', \'2020-10-17\', 0.0, \'AAPL\')")
    cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title2\', \' test contents good bad good bad\', \'2020-10-17\', 0.5, \'AAPL\')")
    cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title3\', \' test contents bad good bad good\', \'2020-10-17\', 0.5, \'AAPL\')")
    # cur.execute("INSERT INTO newsdata VALUES (\'Abdu\', \'Reeee\', \'2020-10-17\', .5, \'AAPL\')")
    # cur.execute("INSERT INTO newsdata VALUES (\'Adam\', \'Bowl? Bowl? Bowl?\', \'2020-10-19\', .8, \'MSFT\')")


def query_userdata(username):
    condition = "username=\'" + username + "\'"
    cur.execute("SELECT * FROM userdata WHERE " + condition)
    return cur.fetchall()


def insert_userdata(username, password):
    values = "(\'" + username + "\',\'" + password + "\')"
    cur.execute("INSERT INTO userdata VALUES " + values)
    cur.execute("SELECT * FROM userdata")
    for x in cur:
        print(x)


def delete_userdata(username):
    condition = "username=\'" + username + "\'"
    cur.execute("DELETE FROM userdata WHERE " + condition)
    cur.execute("SELECT * FROM userdata")
    for x in cur:
        print(x)


def query_portfolio(portfolioID):
    condition = "portfolioID=\'" + portfolioID + "\'"
    cur.execute("SELECT * FROM portfolio WHERE " + condition)
    return cur.fetchall()


def insert_portfolio(portfolioID, stockTicker):
    values = "(\'" + portfolioID + "\',\'" + stockTicker + "\')"
    cur.execute("INSERT INTO portfolio VALUES " + values)
    cur.execute("SELECT * FROM portfolio")
    for x in cur:
        print(x)


def delete_portfolio(portfolioID):
    condition = "portfolioID=\'" + portfolioID + "\'"
    cur.execute("DELETE FROM portfolio WHERE " + condition)
    cur.execute("SELECT * FROM portfolio")
    for x in cur:
        print(x)


def query_stockinfo(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("SELECT * FROM stockinfo WHERE " + condition)
    return cur.fetchall()


def insert_stockinfo(ticker, companyName, marketCap):
    values = "(\'" + ticker + "\',\'" + companyName + "\'," + str(marketCap) + ")"
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
    values = "(\'" + ticker + "\'," + str(open) + "," + str(close) + "," + str(low) + "," + str(high) + ",\'" + priceDate + "\')"
    cur.execute("INSERT INTO stockprice VALUES " + values)


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


def insert_newsdata(title, contents, articleDate, positivity, ticker, link):
    print("insert_newsdata")
    values = "(\"" + title + "\",\"" + contents + "\",\'" + articleDate + "\'," + positivity + ",\'" + ticker + "\',\'" + link + "\')"
    statment = "INSERT INTO newsdata (title, contents, articleDate, positivity, ticker, link) VALUES " + values
    print(statment)
    cur.execute(statment)
    cur.execute("SELECT * FROM newsdata")
    # for x in cur:
    #     print(x)

def delete_newsdata(articleID):
    condition = "articleID=" + str(articleID) + ""
    cur.execute("DELETE FROM newsdata WHERE " + condition)
    cur.execute("SELECT * FROM newsdata")
    for x in cur:
        print(x)


def query_stockprice_by_portfolio_by_date(portfolioID, date):
    select = "i.ticker, i.companyName, i.marketCap, sp.open, sp.close, sp.low, sp.high, sp.priceDate"
    db = "portfolio p LEFT JOIN stockinfo i ON p.stockTicker = i.ticker LEFT JOIN stockprice sp ON i.ticker = sp.ticker"
    condition = "portfolioID=\'" + portfolioID + "\' AND sp.priceDate=\'" + date + "\'"
    cur.execute("SELECT " + select + " FROM " + db + " WHERE " + condition)
    return cur.fetchall()


def query_all_tickers():
    cur.execute("SELECT ticker FROM stockinfo")
    return cur.fetchall()


def query_all_articles():
    cur.execute("SELECT * FROM newsdata")
    return cur.fetchall()


def query_newsdata_by_ticker(ticker):
    condition = "ticker=\'" + ticker + "\'"
    cur.execute("SELECT * FROM newsdata WHERE " + condition)
    return cur.fetchall()

def query_newsdata_by_ticker_and_date(ticker, startDate, endDate):
    condition = "ticker=\'" + ticker + "\' AND articleDate BETWEEN \'" + startDate +"\' AND \'" + endDate + "\' "
    cur.execute("SELECT * FROM newsdata WHERE " + condition + " ORDER BY articleDate")
    return cur.fetchall()

def delete_ticker_from_portfolio(portfolioID, ticker):
    condition = "portfolioID=\'" + portfolioID + "\' AND stockTicker=\'" + ticker + "\'"
    cur.execute("DELETE FROM portfolio WHERE " + condition)
    cur.execute("SELECT * FROM portfolio")
    for x in cur:
        print(x)

def query_stockprice_dates():
    cur.execute("SELECT DISTINCT priceDate FROM stockprice ORDER BY priceDate DESC")
    return cur.fetchall()

def query_login_info(username, password):
    condition = "username=\'" + username + "\' AND password=\'" + password + "\'"
    statment = "SELECT * FROM userdata WHERE " + condition
    # print(statment)
    cur.execute(statment)
    return cur.fetchall()

db_tear()
db_init()
db_fake_insert()
cur.execute("SHOW TABLES")
for x in cur:
    print(x)
