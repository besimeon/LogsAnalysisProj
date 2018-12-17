#!/usr/bin/env python3
#
# Fullstack Nanodegree Logs Analysis Project

import psycopg2

dbName = "news"
db = psycopg2.connect(database=dbName)
c = db.cursor()
def checkIfExists(name):
    ''' checking that view exists before creating, per :
    https://stackoverflow.com/questions/20582500/how-
    to-check-if-a-table-exists-in-a-given-schema '''
    c.execute(        "SELECT EXISTS ( "
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "AND table_name = \'"+name+"') "    )
    exists = c.fetchall()
    return exists

# create a view with author id's, names, and article slugs:
def create_view_authorArticles():
    # Check the bool located in the first slice of the return value:    if checkIfExists("authorarticles")[0][0]:
        # exit if view already exists:
        return
    c.execute(        "CREATE VIEW authorArticles AS "
        "SELECT authors.name, articles.slug "
        "FROM articles JOIN authors "
        # compare articles.author with the corresponding column in authors:
        "ON articles.author = authors.id"    )
    db.commit()
    return
# create a view with dates and error percentages:
# reference from where I got clarification on FILTER:# https://blog.2ndquadrant.com/the-within-group-and-# filter-sql-clauses-of-postgresql-9-4/
def create_view_percentErrorsDaily():
    # Check the bool located in the first slice of the return value:
    if checkIfExists("percenterrorsdaily")[0][0]:
        # exit if view already exists:
        return
    c.execute(        "CREATE VIEW percenterrorsdaily AS "
        # cast values in my calculations as DOUBLE PRECISION to calculate:
        "SELECT DATE(time), (100 * ((count(*) FILTER(WHERE status LIKE '4%' "
        "OR status LIKE '5%'))::DOUBLE PRECISION / "
        "count(*)::DOUBLE PRECISION)) as percentErrors "
        "FROM log "
        "GROUP BY DATE(time)"    )
    db.commit()
    return

# get top 3 viewed articles
def get_popular_articles():
    c.execute(        "SELECT articles.title, count(log.*) as views "
        "FROM articles, log "
        # compare log.path with articles.slug:
        "WHERE log.path LIKE CONCAT('%', articles.slug, '%') "
        "GROUP BY articles.title "
        "ORDER BY views DESC "
        "LIMIT 3"    )
    articles = c.fetchall()
    return articles

def get_popular_authors():
    # get top 3 viewed authors
    # first, make sure view is created containing columns    # needed in the join being used in the query:
    create_view_authorArticles()
    # make aggregate of views from a join of the    # log table & the authorArticles view:
    c.execute(        "SELECT authorArticles.name, count(log.*) as views "
        "FROM authorArticles, log "
        "WHERE log.path LIKE CONCAT('%', authorArticles.slug, '%') "
        "GROUP BY authorArticles.name "
        "ORDER BY views DESC "    )
    authors = c.fetchall()
    return authors

def get_error_days():
    # first, make sure view is created containing columns needed in the query:
    create_view_percentErrorsDaily()
    # query percentErrorsDaily view for days with > 1.0% errors:
    c.execute(        "SELECT * "
        "FROM percenterrorsdaily "
        "WHERE percentErrors > 1.0 "
        "ORDER BY date"    )
    errorDays = c.fetchall()
    return errorDays


# extract contents of get_popular_articles returned list
def print_popular_articles():
    articles = get_popular_articles()
    ''' reference for using range in for loop:
    https://stackoverflow.com/questions/32554527/
    typeerror-list-indices-must-be-integers-or-
    slices-not-str '''
    for i in range(len(articles)):
        print("\""+articles[i][0]+"\" --- "+str(articles[i][1])+" views")
    return

def print_popular_authors():
    authors = get_popular_authors()
    for i in range(len(authors)):
        print(authors[i][0] + " --- "+str(authors[i][1])+" views")
    return

def print_most_errors():
    errorDays = get_error_days()
    for i in range(len(errorDays)):
        print(            str(errorDays[i][0]) +            " --- "+str(round(errorDays[i][1], 1)) +            "% errors"        )
    return

# print seperators and line returns to make more aesthetic:
def output_newSection():
    print("\n")
    print("-" * 10)    return

output_newSection()
print("The most popular three articles of all time are:")
print_popular_articles()

output_newSection()
print("The most popular three authors of all time are:")
print_popular_authors()

output_newSection()
print("The most errors were on the following days:")
print_most_errors()

output_newSection()

db.close()