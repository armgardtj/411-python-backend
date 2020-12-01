import mysql.connector

from neo4j_411 import neo4j_insert_article, neo4j_insert_ticker

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
    cur.execute("DROP TABLE IF EXISTS bigdays")


def db_init():
    cur.execute(
        "CREATE TABLE newsdata (title BLOB(255), contents BLOB(65535), articleDate DATE, positivity DOUBLE(255,2), ticker VARCHAR(10), link BLOB(255), articleID BIGINT(255), PRIMARY KEY (articleID))")
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

    cur.execute(
        "CREATE TABLE bigdays (ticker VARCHAR(255), bigdate DATE, percentdiff DOUBLE(255,2),title BLOB(255), contents BLOB(65535), articleDate DATE, positivity DOUBLE(255,2), link BLOB(255), articleID INT(255))")
    # view stocks page: list all tickers in portfolio, add/remove tickers
    # chart page: show historical stock data and news articles


def db_fake_insert():
    cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker, link, articleID) VALUES (\'test title\', \' good good good good good \', \'2020-11-05\', 1.0, \'AAPL\', \'link\', 1)")

    cur.execute("INSERT INTO userdata VALUES (\'test1\', \'pass\')")
    cur.execute("INSERT INTO userdata VALUES (\'test2\', \'pass2\')")

    cur.execute("INSERT INTO stockinfo VALUES (\'AAPL\', \'Apple Inc\', 1)")
    cur.execute("INSERT INTO stockinfo VALUES (\'GOOG\', \'Google TM\', 2)")
    cur.execute("INSERT INTO stockinfo VALUES (\'MSFT\', \'Microhard\', 3)")

    neo4j_insert_ticker('AAPL')
    neo4j_insert_ticker('GOOG')
    neo4j_insert_ticker('MSFT')

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
    # cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title\', \' good good good good good \', \'2020-10-17\', 1.0, \'AAPL\')")
    # cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title1\', \'bad bad bad bad bad bad bad \', \'2020-10-17\', 0.0, \'AAPL\')")
    # cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title2\', \' test contents good bad good bad\', \'2020-10-17\', 0.5, \'AAPL\')")
    # cur.execute("INSERT INTO newsdata (title, contents, articleDate, positivity, ticker) VALUES (\'test title3\', \' test contents bad good bad good\', \'2020-10-17\', 0.5, \'AAPL\')")

    # neo4j_insert_article('test title', 'AAPL')
    # neo4j_insert_article('test title1', 'AAPL')
    # neo4j_insert_article('test title2', 'AAPL')
    # neo4j_insert_article('test title3', 'AAPL')

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
    neo4j_insert_ticker(ticker)


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


def query_newsdata(link):
    condition = "link=\'" + link + "\'"
    cur.execute("SELECT * FROM newsdata WHERE " + condition)
    return cur.fetchall()


def insert_newsdata(title, contents, articleDate, positivity, ticker, link, articleID):
    values = "(\"" + title + "\",\"" + contents + "\",\'" + articleDate + "\'," + positivity + ",\'" + ticker + "\',\'" + link + "\'," + str(articleID) + ")"
    statement = "INSERT IGNORE INTO newsdata VALUES " + values
    cur.execute(statement)
    cur.execute("SELECT * FROM newsdata")
    neo4j_insert_article(title, ticker)
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

def create_trigger():
    cur.execute("drop trigger if exists main.trg ")
    statment = "CREATE TRIGGER main.trg BEFORE INSERT ON stockprice FOR EACH ROW BEGIN"
    statment += " IF (ABS(100*(NEW.close - NEW.open)/(NEW.open)) > 50) "
    statment += " THEN INSERT INTO bigdays VALUES (\'AAPL\', \'2020-11-05\', 100*(NEW.close - NEW.open)/(NEW.open),"
    statment += " (SELECT title FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1),"
    statment += " (SELECT contents FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1),"
    statment += " (SELECT articleDate FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1),"
    statment += " (SELECT positivity FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1),"
    statment += " (SELECT link FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1),"
    statment += " (SELECT articleID FROM newsdata WHERE ticker = NEW.ticker AND NEW.priceDate = articleDate LIMIT 1) );"
    statment += " END IF;  END"
    cur.execute(statment)

def query_bigdays(tickers):
    cur.execute("SELECT * FROM bigdays WHERE  ticker = \'"+ tickers+ "\'")
    return cur.fetchall()

db_tear()
db_init()
create_trigger()
db_fake_insert()


#print(query_stockprice("AAPL"))
print(query_bigdays("AAPL"))
#print(query_all_articles())