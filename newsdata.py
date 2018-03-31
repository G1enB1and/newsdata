# Python3
# Database code for newsdata (logs analysis project)
# Outputs the answers to three questions.
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2

DBNAME = "news"


def create_or_update_view_slug_from_path():
    """create or update the following postgresql view: slug_from_path."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("CREATE OR REPLACE VIEW slug_from_path AS " +
              "SELECT(REPLACE(log.path, '/article/', '')) AS " +
              # name the new views only column 'slug'
              "slug FROM log " +
              # don't include rows that only have '/'
              "WHERE log.path != '/'")

    db.close()


def get_3_most_popular_titles_views():
    """print the three most popular article titles and number of
    views."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # count the number of times each title appears in slug_from_path.slug
    # and call that count 'views'
    c.execute("SELECT articles.title, count(*) AS views " +
              "FROM articles JOIN slug_from_path " +
              "ON articles.slug = slug_from_path.slug " +
              "GROUP BY articles.title " +
              # only show the top 3 in descending order by number of views
              "ORDER BY views DESC LIMIT 3")

    qresult = c.fetchall()
    print('\n'+"1. What are the most popular three articles of all time?")
    # qresults[row][column] column 0 = title, column 1 = views
    print("\"" + qresult[0][0] + "\" — " + str(qresult[0][1]) + " views")
    print("\"" + qresult[1][0] + "\" — " + str(qresult[1][1]) + " views")
    print("\"" + qresult[2][0] + "\" — " + str(qresult[2][1]) + " views"+'\n')
    db.close()


def get_most_popular_authors():
    """print the most popular article authors and views in descending order."""
    # That is, when you sum up all of the articles each author has written,
    # which authors get the most page views? Present this as a sorted list
    # with the most popular author at the topself.

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # SUM the view counts from each article when grouped by author
    c.execute("SELECT subq1.name, SUM(subq1.views) AS views " +
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

    qresult = c.fetchall()
    print("2. Who are the most popular article authors of all time?")

    for row in qresult:
        print("\"" + row[0] + "\" — " + str(row[1]) + " views")

    db.close()


def get_dates_of_errors_over_one_percent():
    """print the dates and error percentages on days where error percentage is
    higher than one percent."""
    # The log table includes a column status that indicates the HTTP status
    # code that the news site sent to the user's browserself.
    # Example: Julu 29, 2016 — 2.5% errors

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # REPLACE THIS WITH APPROPRIATE CODE - THIS IS A PLACE HOLDER
    c.execute("SELECT date, error_percentage " +
              "FROM(SELECT log.time::timestamp::date AS date, " +
              "ROUND((SUM(CASE WHEN log.status = '404 NOT FOUND' " +
              "THEN 1 ELSE 0 END) " +
              "/ ( COUNT(*) * 1.0 ) ) * 100, 1 ) " +
              "AS error_percentage " +
              "FROM log " +
              "GROUP BY date ) " +
              "AS subq2 " +
              "WHERE error_percentage > 1")

    qresult = c.fetchall()
    print("\n" + "3. On which days did more than " +
          "1% of requests lead to errors?")

    for row in qresult:
        print("" + str(row[0]) + " — " + str(row[1]) + "% errors")

    print('\n')
    db.close()

create_or_update_view_slug_from_path()
get_3_most_popular_titles_views()
get_most_popular_authors()
get_dates_of_errors_over_one_percent()
