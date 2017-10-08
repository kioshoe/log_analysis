# Python3

import sys
import psycopg2

DBNAME = "news"

# Questions
question_1 = "What are the most popular three articles of all time?"
question_2 = "Who are the most popular authors of all time?"
question_3 = "On which day(s) did more than 1% of requests lead to errors?"

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
    except:
        print ("Error: Could not complete query.")


# Formats and writes query results into a new text file.
def file_output():
    print ("Creating new text file...")
    filename = input("Enter name of file:")
    filename = filename+".txt"
    try:
        log_output = open(filename, 'w')
    except:
        print ("Error. File could not be created.")
        sys.exit(0)
    print ("Writing to file...")
    sys.stdout = log_output
    print (question_1)
    q1_results = query_results(query_1)
    for i in range(0, len(q1_results), 1):
        print (
          "     " + q1_results[i][0] +
          " - " + str(q1_results[i][1]) + " views")
    print (" ")
    print (question_2)
    q2_results = query_results(query_2)
    for i in range(0, len(q2_results), 1):
        print (
          "     " + q2_results[i][0] +
          " - " + str(q2_results[i][1]) + " views")
    print (" ")
    print (question_3)
    q3_results = query_results(query_3)
    if len(q3_results) > 0:
        for i in range(0, len(q3_results), 1):
            print (
              "     " + str(q3_results[i][0]) +
              " - " + str(q3_results[i][1]) + "% error rate")
    else:
        print ("None.")
    log_output.close()
    sys.stdout = sys.__stdout__
    print ("File saved.")

if __name__ == '__main__':
    file_output()
