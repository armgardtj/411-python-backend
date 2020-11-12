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
    cur.execute("CREATE TABLE newsdata (articleID INT(255), title VARCHAR(255), contents TEXT(65535), articleDate VARCHAR(255), positivity INT(255), ticker VARCHAR(10), PRIMARY KEY (articleID))")
    cur.execute("CREATE TABLE stockprice (ticker VARCHAR(10), open DOUBLE(255,2), close DOUBLE(255,2), low DOUBLE(255,2), high DOUBLE(255,2), priceDate VARCHAR(255), PRIMARY KEY (ticker, priceDate))")
    cur.execute("CREATE TABLE stockinfo (ticker VARCHAR(10), companyName VARCHAR(255), marketCap INT(255), PRIMARY KEY (ticker))")
    cur.execute("CREATE TABLE portfolio (portfolioID INT(255), stockTickers VARCHAR(10), PRIMARY KEY (portfolioID))")
    cur.execute("CREATE TABLE userdata (email VARCHAR(255), name VARCHAR(255), password VARCHAR(255), portfolioID INT(255), PRIMARY KEY (email))")
    # view stocks page: list all tickers in portfolio, add/remove tickers
    # chart page: show historical stock data and news articles

db_tear()
db_init()
cur.execute("SHOW TABLES")
for x in cur:
    print(x)