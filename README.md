# Project: Log Analysis

First is a first project written as a part of the Udacity Full Stack Web Developer Nanodegree.

# Environment setup

The code is written to make use of the:
- Linux VM configured via Vagrant/VirtualBox.
- Python 2.7
- PostgreSQL (psql) database
- Data set provided by the course (newsdata.sql)
- Custom database views

## Vagrant/VirtualBox installation

If using Windows, you can make use of a VirtualBox Linux environment.
To set up,
- Download <a href="https://www.virtualbox.org/wiki/Download_Old_Builds_5_1">Oracle VirtualBox</a>. Do not launch it, Vagrant will do that for you later.
- Download <a href="https://www.vagrantup.com/downloads.html">Vagrant</a>. Grant it network permissions if asked. 
- Check Vagrant is installed properly via terminal: `vagrant --version`

## VM installation

- Clone Github directory with a VM configuration: https://github.com/udacity/fullstack-nanodegree-vm
- Open the directory with the dowloaded code in the terminal and switch to vagrant sub-directory: `cd vagrant`
- Bring VM up: `vagrant up`

This will take some time as VM is being configured.

## Database configuration

Vagrant VM comes with Python and PostgreSQL that are required for this code to run.

Fill the database with some test data:
- Download data set <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">newsdata.zip</a>
- Unzip it and copy newsdata.sql to your /vagrant directory
- Log in to VM: `vagrant ssh`
- Switch to vagrant directory: `cd /vagrant`
- Load data to the database: `psql -d news -f newsdata.sql`

## Custom view creation

While in the VM:
- Connect to the database: `psql "news"`
- Copy/paste each code's view and run in psql.

### View1:
Calculates the usage of each log item whose path contains something valuable.
it will return the usage count and will covert the path to the more sutable for article search string
```sql
create view article_usage as
	select REPLACE(path,'/article/','') as starts_with, COUNT(*) usage
	from log
	where path != '/'
	group by path;
```

### View2: 
Calculates total number of logged requests and number of errors per day
```sql
create view daily_access as
	select DATE(time) as logdate, SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) as errcount, COUNT(*) as total
	from log
	group by logdate;
```

# How to run code

While in the VM, execute `python analyzer.py`

# Expected Result

The program will use the provided data set to calculate answers to the 3 questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

### FOR EXAMPLE:
```
vagrant@vagrant:/vagrant/project1$ python analyzer.py

Top popular articles:
1. Candidate is jerk, alleges rival - 338647 views
2. Bears love berries, alleges bear - 253801 views
3. Bad things gone, say good people - 170098 views

Author popularity:
1. Ursula La Multa - 507594 views
2. Rudolf von Treppenwitz - 423457 views
3. Anonymous Contributor - 170098 views
4. Markoff Chaney - 84557 views

Daily errors over 1 percent:
July      17, 2016 -    2.3% errors
```
