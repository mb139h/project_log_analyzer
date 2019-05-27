# Project: Log Analysis

First is a first project written as a part of the Udacity Full Stack Web Developer Nanodegree.

# Pre-requisites

Database: PostgreSQL (psql)
Language: python 2.7
Database setup:
1. data provided by the course (newsdata.sql)
2. views below

# view calculates the usage of each log item whose path contains something valuable
# it will return the usage count and will covert the path to the more sutable for article search string 
create view article_usage as
	select REPLACE(REPLACE(path,'-',' '),'/article/','') as starts_with, COUNT(*) usage
	from log
	where path != '/'
	group by path;

# view calculates total number of logged requests and number of errors per day
create view daily_access as
	select DATE(time) as logdate, SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) as errcount, COUNT(*) as total
	from daily_access
	from log
	group by logdate;	

# How to run

python analyzer.py

# Expected Result

The program will use the provided data set to calculate answers to the 3 questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

---------------------------------
FOR EXAMPLE:
---------------------------------
vagrant@vagrant:/vagrant/project1$ python analyzer.py

Top popular articles:
1. Candidate is jerk, alleges rival - 338647 views
2. Bears love berries, alleges bear - 253801 views
3. Bad things gone, say good people - 170098 views

Author popularity:
1. Rudolf von Treppenwitz - 423457 views
2. Ursula La Multa - 338184 views
3. Anonymous Contributor - 170098 views
4. Markoff Chaney - 84557 views

Daily errors over 1 percent:
July      17, 2016 -    2.3% errors
