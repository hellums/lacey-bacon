# INITIATIVE OVERVIEW
This repo is a work in progress (not complete). It contains files and related project data for a 12-week introductory bootcamp course (Jan-Mar 2022) on Python programming and data analysis/science in a group learning environment. However, all programming and data analysis is individual, and shared/coordinated with instructors and mentors as necessary. Primary coding was completed in 7 weeks, through Feb 25.

### INITIATIVE PAGES
- [Kanban](https://github.com/hellums/hallmarkish/projects/1)
- [Wiki](https://github.com/hellums/hallmarkish/wiki/1.-Data-Analytics-Course-Project)
- [Notebook/EDA](https://github.com/hellums/lacey-bacon/blob/root/romcom.pdf)

# INITIATIVE GOALS
This repo and project will have several purposes:
- Satisfy the 4+ minimum requirements of the bootcamp assignment in the syllabus
- Satisfy as many optional requirements as possible

### INITIATIVE SCOPE
Is Lacey Chabert indeed the "Center of the (Hallmark) Universe," as Kevin Bacon reputably is to Hollywood? Given the time and resource limitations, this project is not meant to be an all-inclusive or full programming approach to the _"6 Degrees of Kevin Bacon"_ topic itself (using BFS or Breadth-First Search algorithms, for example). It merely provides a working environment to support the programming and data science portions of the course, using a subset of movies and actors specific to Hallmark original movies, romantic comedies, mysteries, and dramas.

# SPECIAL INSTRUCTIONS (use your own Python 3 interpreter command, such as py3 or python, if it is different than 'python3' used here) 

TO INSTALL PROGRAM AND CREATE A VIRTUAL ENVIRONMENT:
- >git clone <span>git@</span>github.com:hellums/lacey-bacon.git
- >cd lacey-bacon
- >python3 -m venv env
- >echo "env/" >> .git/info/exclude (optional command)

TO ACTIVATE VIRTUAL ENVIRONMENT:
- Mac/Linux: 
  >source env/bin/activate
- PC:
  >env\scripts\activate.bat

TO INSTALL PREREQUISITES:
  - >python3 -m pip install -r requirements.txt

TO RUN PROGRAM (ALL BUT MENU ITEM 3 WILL WORK "OUT OF THE BOX," WITHOUT FULL REBUILD BELOW):
  - >python3 romcom.py

TO RUN FLASK MICROSITE (ALL WILL WORK WITHOUT FULL REBUILD BELOW):
  - >python3 romcomWeb.py
  - >in a web browser tab, go to http://localhost:5000/ 

TO PERFORM FULL DOWNLOAD AND REBUILD DATA/DATABASE: (optional)
  - >python3 romcomPrep.py (NOTE: compressed files total 4 GB, uncompressed another 2 GB)

TO TEST FLASK APIs (WITH romcomWeb):
  - >in a web browser tab, go to http://localhost:5000/ to load the app and api functions

  - >http://localhost:5000/actors returns the top 10 books in JSON format

  - >http://localhost:5000/movies returns the top 10 movies in JSON format

  - >http://localhost:5000/rating/?tt=tt13831504 returns the rating of "It Was Always You" in JSON format 

  - >    (tt is the IMDB title code for a romcom in the database)

TO RUN AND TEST FLASK APIs (standalone):
  - >python3 romcomApi.py to load just the api functions (on port 8080)

  - >in a web browser tab, go to http://localhost:8080/ (other API calls same as above)

  - >http://localhost:8080/actors, etc.

TO TEST AND VALIDATE INTEGRITY OF DATA STRUCTURES: (optional)
  - >python3 -m unittest test_romcom -v

TO TEST SQLITE3 DATABASE: (optional)
  - >python3 romcomSQL.py

# PACKAGES INVOLVED
See requirements.txt file in project folder. 

Primarily:
- matplotlib==3.5.1
- networkx==2.6.3
- numpy==1.22.2
- pandas==1.4.1
- requests==2.27.1
- tabulate==0.8.9
- urllib3==1.26.8
- Flask=2.0.3

# STATUS OF FEATURES PLANNED AT INITIATIVE OUTSET

- [x] Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program.
- [x] Create a class, then create at least one object of that class and populate it with data. The value of at least one object must be used somewhere in your code. (implemented, but not used in main module, in preference of functions for now)
- [x] Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program.
- [x] Create and call at least 3 functions or methods, at least one of which must return a value that is used somewhere else in your code.

Category 2: Utilize External Data:
- [x] Read data from an external file, such as text, JSON, CSV, etc, and use that data in your application.
- [x] Connect to a database and read data using SQL.

Category 3: Data Display
- [x] Visualize data in a graph, chart, or other visual representation of data.

Category 4: Best Practices
- [x] The program should utilize a virtual environment and document library dependencies in a requirements.txt file.
- [x] Create 3 or more unit tests for your application.

"Stretch" list:

- [x] Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display.
- [x] Use a Jupyter notebook to document your data analysis.

### TECHNOLOGIES LEVERAGED
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
- Networkx (node/ege, centrality)
- BeautifulSoup
- Docker (introductory)
- Cookiecutter (introductory)
- IMDB (data source for movies and custom watchlist)
- "Balanced" scale, 1 witch, 1 duck, very small rocks (that float)
- 2 African swallows, 1 coconut, twine for sling-loading
