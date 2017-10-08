#!/usr/bin/env Python3

import sys
import psycopg2

DBNAME = "news"

# Questions
question_1 = "What are the most popular three articles of all time?"
question_2 = "Who are the most popular authors of all time?"
question_3 = "On which day(s) did more than 1% of requests lead to errors?"

#Units for print function
views = " views"
err = "% error rate"

# Database queries
query_1 = """
    select articles.title, count(*) as num
    from articles, log
    where log.path = concat('/article/', articles.slug)
    and log.status = '200 OK'
    group by articles.title
    order by num desc
    limit 3"""

query_2 = """
    select authors.name, count(*) as num
    from authors, articles, log
    where log.path = concat('/article/', articles.slug)
    and log.status = '200 OK'
    and articles.author = authors.id
    group by authors.name
    order by num desc"""

query_3 = """
    with error_log as (
        select log.time::date,
        round(100.0*sum(
          case log.status
          when '404 NOT FOUND'
          then 1
          else 0
          end)/count(log.status), 2)
        as p_error
        from log
        group by log.time::date
        order by p_error desc)
    select * from error_log where p_error > 1"""


# Returns query results from database
def query_results(query):
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except queryerror:
        print("Error: Could not complete query.")
        sys.exit(1)

# Formats query results
def print_results(results, unit):
    if len(results) > 0: 
        for i in range(0, len(results), 1):
            print(
                "    " + str(results[i][0]) +
                " - " + str(results[i][1]) + unit)
    else:
        print("None.")
    print(" ")

# Writes query results into a new text file.
def file_output():
    print("Creating new text file...")
    filename = input("Enter name of file:")
    filename = filename+".txt"
    try:
        log_output = open(filename, 'w')
    except fileerror:
        print("Error. File could not be created.")
        sys.exit(0)
    print("Writing to file...")
    sys.stdout = log_output
    print(question_1)
    print_results(query_results(query_1), views)
    print(question_2)
    print_results(query_results(query_2), views)
    print(question_3)
    print_results(query_results(query_3), err)
    log_output.close()
    sys.stdout = sys.__stdout__
    print("File saved.")


if __name__ == '__main__':
    file_output()
