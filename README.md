# Logs Analysis Project
----------------------
-This is a project created for Udacity Course: Full Stack Web Developer.

-This project uses Python3 + PostgreSql to connect to a news database, checking for existence of &/or creating database views, performs multiple queries utilizing aforementioned views and existing tables, and outputs data in a visually aesthetic format to answer questions posed in the project assignment.

## Table of Contents
-------------------
- [Prerequisites](#prerequisites)
- [Install](#install)

## Prerequisites
---------------
- Python 3.
- Sufficient user permissions to run Python files.
- Enviornment with PostgreSql installed


## Install
---------
- ensure Python3 and PostgreSql are installed, and that a database titled 'news' is created.  This project was tested on the virtual machine supplied by Udacity during the Fullstack Web Developer Nanodegree in Part 3 Lesson 2.17.  The virtual machine was run in a Linux enviornment with VirtualBox and Vagrant.  PostgreSql & the news database were already setup in this virtual machine.  Instructions to replicate this testing enviornment can be accessed in the aformentioned Fullstack Web Developer Nanodegree section.
- extract contents of LogsAnalysisProj.zip.
- navigate to the LogsAnalysisProj directory.
- run the following command: `python3 LogsAnalysisProj.py`
- a sample of the program's output can be found in the following file: `SampleOutput.txt`


### View Definitions
-------------------
#### NOTE: the views listed below are AUTOMATICALLY CREATED by the program.  You DON'T need to manually create these views.  The display of the code used to create these views is for informal purposes only, as per project Rubric.
- this program utilizes the following views:
1. authorArticles
    i. contains author id's, names, and article slugs
    ii. code: ``CREATE VIEW authorArticles AS SELECT authors.name, articles.slug FROM articles JOIN authors ON articles.author = authors.id``
2. percentErrorsDaily
    i.  contains dates and percentage of errors per date.
    ii.  code: ``CREATE VIEW percentErrorsPerDay AS
    SELECT DATE(time), (100 * ((count(*) FILTER(WHERE status LIKE '4%' OR status LIKE '5%'))::DOUBLE PRECISION / count(*)::DOUBLE PRECISION)) as percentErrors
    FROM log
    GROUP BY DATE(time);``