#!/usr/bin/env python2
#
# Log Analyzer

import psycopg2

# What are the most popular three articles of all time
query_top_popular_articles = "\
    select a.title, u.usage \
    from articles a, \
        (select starts_with, usage \
            from article_usage \
            order by usage desc \
            fetch first {0} rows only) u \
    where a.slug = u.starts_with \
    order by u.usage desc;"

# Who are the most popular article authors of all time
query_author_popularity = "\
    select n.name, SUM(u.usage) as total \
    from authors n, \
        articles a, \
        article_usage u \
    where n.id = a.author and a.slug = u.starts_with \
    group by n.name \
    order by total desc;"

# On which days did more than X% of requests lead to errors
query_daily_errors = "\
    select TO_CHAR(logdate, 'Month DD, YYYY'), \
           TO_CHAR(errcount*100.0/total, '999.9') \
    from daily_access \
    where errcount*100.0/total > {0};"


def fetch_db_result(query_to_run):
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(query_to_run)
        return c.fetchall()
    finally:
        if c:
            c.close()
        if db:
            db.close()


def print_top_popular_articles(top_n):
    print '\nTop popular articles:'
    result = fetch_db_result(query_top_popular_articles.format(top_n))
    for index in range(len(result)):
        article = result[index][0]
        count = str(result[index][1])
        print str(index+1)+'. '+article+' - '+count+' views'


def print_author_popularity():
    print '\nAuthor popularity:'
    result = fetch_db_result(query_author_popularity)
    for index in range(len(result)):
        author = result[index][0]
        count = str(result[index][1])
        print str(index+1)+'. '+author+' - '+count+' views'


def print_daily_errors(min_percent):
    print '\nDaily errors over '+str(min_percent)+' percent:'
    result = fetch_db_result(query_daily_errors.format(min_percent))
    for index in range(len(result)):
        print result[index-1][0]+' - '+str(result[index-1][1])+'% errors'


if __name__ == '__main__':
    print_top_popular_articles(3)
    print_author_popularity()
    print_daily_errors(1)
    print '\n'
