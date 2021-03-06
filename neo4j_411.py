# plz don't rename the file to 'neo4j.py' or this line wont work.
from neo4j import GraphDatabase
# import copy

neo4j_uri  = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_pass = 'password'
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))

#
#
#
def neo4j_insert_ticker(ticker):
    print("neo4j_insert_ticker - start")
    # First, check if it exists.
    with driver.session() as session:
        result = session.run("MATCH (t:Ticker {ticker : $ticker}) "
                             "RETURN t", ticker=ticker)

        if result.peek():
            print("neo4j_insert_ticker - ticker already in neo4j, doing nothing")
            return
        session.close()

    with driver.session() as session:
        result = session.run("CREATE (t:Ticker) "
                             "SET t.ticker = $ticker "
                             "RETURN t.ticker AS ticker", ticker=ticker)
        session.close()
    print("neo4j_insert_ticker - ticker added successfully")

#
#
#
def neo4j_insert_article(title, ticker):
    #print("neo4j_insert_article - start")
    # First, check if it exists.
    with driver.session() as session:
        result = session.run("MATCH (a:Article {title : $title}) "
                             "RETURN a", title=title
                            )
        if result.peek():
            #print("neo4j_insert_article - article already in neo4j, only need to set relation")
            session.close()
            neo4j_insert_relationship(title, ticker)
            return
        session.close()

    with driver.session() as session:
        result = session.run("CREATE (a:Article) "
                             "SET a.title = $title "
                             "RETURN a", title=title)
        session.close()
    neo4j_insert_relationship(title, ticker)

    #print("neo4j_insert_article - article added successfully")



def neo4j_insert_relationship(title, ticker):
    #print("neo4j_insert_relationship - start")
    with driver.session() as session:
        result = session.run("MATCH (a:Article), (t:Ticker), (a)-[r:written_about]->(t) "
                             "WHERE a.title=$title AND t.ticker=$ticker "
                             "RETURN r ",
                              ticker=ticker, title=title)
        if result.peek():
            #print("neo4j_insert_relationship - relation already in neo4j")
            session.close()
            return
        session.close()

    with driver.session() as session:
        result = session.run("MATCH (a:Article), (t:Ticker) "
                             "WHERE a.title=$title AND t.ticker=$ticker "
                             "CREATE (a)-[:written_about]->(t) ",
                              ticker=ticker, title=title)
        session.close()
        #print("neo4j_insert_relationship - relation added successfully")

#
# gets back all the articles that are written about more than one ticker
#
def neo4j_get_high_impact_articles():
    #print("neo4j_get_high_impact_articles - start")

    with driver.session() as session:
        result = session.run("MATCH (a:Article)-[:written_about]->(t1:Ticker), (a:Article)-[:written_about]->(t2:Ticker) "
                             "RETURN a")
        #print("neo4j_get_high_impact_articles - returning articles")
        return result

#
#
#
def neo4j_get_tickers():
    with driver.session() as session:
        result = session.run("MATCH (t1:Ticker) "
                             "RETURN t1.ticker")
        #print("neo4j_get_tickers - query success, processing data")
        ret = []
        for record in result:
            # print(record.values())
            new_set = set(record.values())
            if new_set not in ret:
                ret.append(new_set)
        info = result.consume()
        #print("neo4j_get_tickers - returning")
        return ret

def neo4j_get_articles():
    with driver.session() as session:
        result = session.run("MATCH (a:Article) "
                             "RETURN a.title")
        #print("neo4j_get_tickers - query success, processing data")
        ret = []
        for record in result:
            # print(record.values())
            new_set = set(record.values())
            if new_set not in ret:
                ret.append(new_set)
        info = result.consume()
        #print("neo4j_get_tickers - returning")
        return ret

def neo4j_get_related_tickers():
    #print("neo4j_get_related_tickers - start")
    with driver.session() as session:
        result = session.run("MATCH (a:Article)-[:written_about]->(t1:Ticker) "
                             "MATCH (a:Article)-[:written_about]->(t2:Ticker) "
                             "WHERE t1.ticker <> t2.ticker "
                             "RETURN DISTINCT t1.ticker, t2.ticker")
        #print("neo4j_get_related_tickers - query success, processing data")
        ret = []
        for record in result:
            # print(record.values())
            new_set = set(record.values())
            if new_set not in ret:
                ret.append(new_set)
        info = result.consume()
        #print("neo4j_get_related_tickers - returning")
        return ret


# When I insert a ticker into sql, check if that ticker exists in neo4j
#       If the ticker does not exist, insert it
#       Else do nothing.
#
#
#
# When I insert an article into sql, check if that artciel exists in neo4j
#       If the article does not exist, add the node, then set the relation
#       If the article does exist, dont add the node, ONLY set the relation.
#
#

def fake_insert():

    # title = "Apple shares good"
    title = "Apple and Google shares good"

    ticker = "AAPL"
    ticker = "GOOG"
    # ticker = "nothing"
    # ret = neo4j_get_high_impact_articles()
    # print(ret)
    # print(ret.peek())
    # for r in ret:
    #     print(r)
    neo4j_insert_ticker(ticker="AAPL")
    neo4j_insert_ticker(ticker="GOOG")
    neo4j_insert_article(title="Apple shares good", ticker="AAPL")
    neo4j_insert_article(title="Apple and Google shares good", ticker="AAPL")
    neo4j_insert_article(title="Apple and Google shares good", ticker="GOOG")
    ret = neo4j_get_related_tickers()
    #print(ret)
    # print(ret.peek())
    # for r in ret:
        # print(r)
    # neo4j_insert_ticker(ticker)
    # driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    # session = driver.session()
    # result = session.run("CREATE (a:Article) "
    #                      "SET a.title = $title "
    #                      "RETURN a", title=title)
    # print(result.peek())
    # session.close()
    # session = driver.session()
    # result = session.run("CREATE (t:Ticker) "
    #                      "SET t.ticker = $ticker "
    #                      "RETURN t.ticker AS ticker", ticker=ticker)
    # print(result.peek())
    # driver.close()
    # greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "password")
    # greeter.print_greeting("hello, world")
    # greeter.close()

with driver.session() as session:
    session.run("MATCH(n) "
                "DETACH DELETE n")