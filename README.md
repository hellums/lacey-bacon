# OVERVIEW
This repo is product from a 12-week introductory bootcamp course (Jan-Mar 2022) on Python programming and data analysis.

# GOALS
This repo and project has several purposes:
- Satisfy the 4+ minimum requirements of the bootcamp assignment in the syllabus
- Satisfy as many optional requirements as possible

# SCOPE
Is Lacey Chabert indeed the "Center of the (Hallmark) Universe," as Kevin Bacon reputably is to Hollywood? Given the time and resource limitations, this project is not meant to be an all-inclusive or full programming approach to the _"6 Degrees of Kevin Bacon"_ topic itself (using BFS or Breadth-First Search algorithms, for example). It merely provides a working environment to support the programming and data science portions of the course, using a subset of movies and actors specific to Hallmark original movies, romantic comedies, mysteries, and dramas.

# Basic Functionality (Code Louisville Project)
This program was built and tested using:

- > Python version 3.10.1

- > pip version 21.3.1

Use your own Python 3 interpreter command, such as py3 or python, if it is different than 'python3' used here. Python's recommended best practice is to upgrade to and use the latest version of pip, if you are behind.

All of the features of the command-line program will work "out-of-the-box" except for menu option 3, finding movies two people both starred in. This is a result of the size limitation of raw data files in Github, as well as the considerable amount of space required for the original build and downloaded IMDB source files. All features of the optional Web-based and API versions of the program run using the files supplied, and also do not require a full download and rebuild. The optional unittest and SQL tests are only included as part of the original Code Louisville project requirements.

Prerequisites include:
- matplotlib==3.5.1
- networkx==2.6.3
- numpy==1.22.2
- pandas==1.4.1
- requests==2.27.1
- tabulate==0.8.9
- urllib3==1.26.8
- Flask=2.0.3
- natsort=8.1.0

TO INSTALL PREREQUISITES AND RUN COMMAND-LINE VERSION:
  - >git clone <span>git@</span>github.com:hellums/lacey-bacon.git
  - >cd lacey-bacon
  - >python -m pip install -r requirements.txt
  - >python romcom.py

(OPTIONAL) TO CREATE AND ACTIVATE A VIRTUAL ENVIRONMENT (IF DESIRED)
- >python -m venv env
- Mac/Linux: 
  >source env/bin/activate
- PC:
  >env\Scripts\activate.bat

# Code Louisville Requireements met
Satisfaction of requirements are called out in code, just search for "Code Louisville"

Category 1 - Python Programming Basics
- [x] Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program.
- [x] Create a class, then create at least one object of that class and populate it with data. The value of at least one object must be used somewhere in your code. (implemented, but not used in main module, in preference of functions for now)
- [x] Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program.
- [x] Create and call at least 3 functions or methods, at least one of which must return a value that is used somewhere else in your code.

Category 2 - Utilize External Data
- [x] Read data from an external file, such as text, JSON, CSV, etc, and use that data in your application.
- [x] Connect to a database and read data using SQL.

Category 3 - Data Display
- [x] Visualize data in a graph, chart, or other visual representation of data.

Category 4 - Best Practices
- [x] The program should utilize a virtual environment and document library dependencies in a requirements.txt file.
- [x] Create 3 or more unit tests for your application.

"Stretch" list:

- [x] Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display.
- [x] Use a Jupyter notebook to document your data analysis.

### Technologies Leveraged
- GitHub, Git
- Slack, Pluralsight
- Visual Studio Code
- Python, Anaconda
- Flask, Jinja
- APIs
- HTML, CSS
- SQLite3
- Unittest
- Jupyter Notebook
- Pandas
- Matplotlib 
- Networkx (node/edge, centrality)
- BeautifulSoup (supplemental work, not in romcom)
- Docker (introductory)
- Cookiecutter (introductory)
- IMDB (data source for movies and custom watchlist)
- "Balanced" scale, 1 witch, 1 duck, very small rocks (that float)
- 2 African swallows, 1 coconut, twine for sling-loading

# Extended Functionality 

(OPTIONAL) TO RUN THE BROWSER VERSION:
  - >python romcomWeb.py
  - >in a web browser tab, go to http://localhost:5000/ 

(OPTIONAL) TO RUN THE API VERSION:
  - >python romcomAPI.py

  - >in a web browser tab, http://localhost:8080/actors will return top 10 actors in JSON simple list format

  - >http://localhost:8080/movies will return the top 10 movies in JSON simple list format

  - >http://localhost:8080/rating/?tt=tt13831504 will return the rating of "It Was Always You" as JSON list 

  - >    (tt is the IMDB title code for a romcom in the database)

(OPTIONAL) TO TEST AND VALIDATE INTEGRITY OF DATA STRUCTURES:
  - >python -m unittest test_romcom -v

(OPTIONAL) TO TEST SQLITE3 DATABASE:
  - >python romcomSQL.py

(OPTIONAL) TO PERFORM FULL DOWNLOAD AND REBUILD DATA/DATABASE:
  - >python romcomPrep.py (NOTE: compressed files total 4 GB, uncompressed another 2 GB)

### INITIATIVE PAGES
- [Kanban](https://github.com/hellums/lacey-bacon/projects/1)
- [Wiki](https://github.com/hellums/lacey-bacon/wiki/1.-Data-Analytics-Course-Project)
- [Notebook/EDA](https://github.com/hellums/lacey-bacon/blob/root/romcomEDA.pdf)


### SCREEN SHOTS

<p align="center">
  <img src="https://user-images.githubusercontent.com/83464025/156023028-09a53cc7-01e8-49f8-bc2a-37ae3f663e9d.png" />
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/83464025/156022771-72977fa3-bfa9-4812-922e-d605bcd3e682.png" />
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/83464025/156023338-7bfa39cc-7c42-45a4-96d9-faeca56a3374.png" />
</p>

