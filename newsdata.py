#! /usr/bin/env Python3

# Database code for newsdata (logs analysis project)
# Outputs the answers to three questions.
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def create_or_update_view_slug_from_path():
    """create or update the following postgresql view: slug_from_path."""
    db, cursor = connect()

    query = ("CREATE OR REPLACE VIEW slug_from_path AS " +
             "SELECT(REPLACE(log.path, '/article/', '')) AS " +
             # name the new views only column 'slug'
             "slug FROM log " +
             # don't include rows that only have '/'
             "WHERE log.path != '/'")

    cursor.execute(query)

    db.close()


def get_3_most_popular_titles_views():
    """print the three most popular article titles and number of
    views."""
    db, cursor = connect()

    # count the number of times each title appears in slug_from_path.slug
    # and call that count 'views'
    query = ("SELECT articles.title, count(*) AS views " +
             "FROM articles JOIN slug_from_path " +
             "ON articles.slug = slug_from_path.slug " +
             "GROUP BY articles.title " +
             # only show the top 3 in descending order by number of views
             "ORDER BY views DESC LIMIT 3")

    cursor.execute(query)

    qresult = cursor.fetchall()
    print('\n'+"1. What are the most popular three articles of all time?")
    for row in qresult:
        print("\"" + row[0] + "\" — " + str(row[1]) + " views")

    db.close()


def get_most_popular_authors():
    """print the most popular article authors and views in descending order."""
    # That is, when you sum up all of the articles each author has written,
    # which authors get the most page views? Present this as a sorted list
    # with the most popular author at the topself.

    db, cursor = connect()

    # SUM the view counts from each article when grouped by author
    query = ("SELECT subq1.name, SUM(subq1.views) AS views " +
             # count the number of times each title appears in slug_from_path
             # .slug and call that count 'views'
             "FROM (SELECT articles.title, name, count(*) AS views " +
             "FROM articles JOIN authors ON authors.id = articles.author " +
             "JOIN slug_from_path " +
             "ON articles.slug = slug_from_path.slug " +
             "GROUP BY articles.title, authors.name " +
             "ORDER BY views DESC) as subq1 " +
             "GROUP BY subq1.name " +  # group by author name
             "ORDER BY views DESC")  # in descending order by number of views

    cursor.execute(query)

    qresult = cursor.fetchall()
    print("\n2. Who are the most popular article authors of all time?")

    for row in qresult:
        print("\"" + row[0] + "\" — " + str(row[1]) + " views")

    db.close()


def get_dates_of_errors_over_one_percent():
    """print the dates and error percentages on days where error percentage is
    higher than one percent."""
    # The log table includes a column status that indicates the HTTP status
    # code that the news site sent to the user's browserself.
    # Example: Julu 29, 2016 — 2.5% errors

    db, cursor = connect()

    # Make a query that returns the date and error percentages
    # for every date that has more than 1% errors.
    query = ("SELECT to_char(date, 'FMMonth FMDD, YYYY'), " +
             "err/total AS ratio " +
             "FROM (SELECT time::date AS date, " +
             "count(*) AS total, " +
             "(SUM((status != '200 OK')::int)::float * 100) " +
             "AS err " +
             "FROM log " +
             "GROUP BY date) AS errors " +
             "WHERE err/total > 1")

    cursor.execute(query)

    qresult = cursor.fetchall()
    print("\n" + "3. On which days did more than " +
          "1% of requests lead to errors?")

    for row in qresult:
        print("" + str(row[0]) + " — " + str(round(row[1], 1)) + "% errors")

    print('')
    db.close()

if __name__ == "__main__":
    create_or_update_view_slug_from_path()
    get_3_most_popular_titles_views()
    get_most_popular_authors()
    get_dates_of_errors_over_one_percent()
    
