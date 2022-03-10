# OVERVIEW
Is Lacey Chabert indeed the "Center of the (Hallmark) Universe," as Kevin Bacon reputably is to Hollywood? This project seeks to find out, using a subset of IMDB listed movies and actors from Hallmark original movies, romantic comedies, mysteries, and dramas.  

  <img src="https://user-images.githubusercontent.com/83464025/156023028-09a53cc7-01e8-49f8-bc2a-37ae3f663e9d.png" />

This repo is the product of a Code Louisville course on Python programming and data analysis.


# WALKTHROUGH VIDEO
[Walkthrough Video](https://user-images.githubusercontent.com/83464025/157714425-978554df-bca1-479d-b223-48d0da9a87af.mp4)

# GOALS
- Satisfy the 4+ minimum requirements of the bootcamp assignment in the syllabus (one from each category)
- Satisfy as many optional and "stretch" requirements and enhancements as possible

# BASIC FUNCTIONALITY (Code Louisville Project)
## This program was built and tested using:

- python version 3.10.1
- pip version 21.3.1

Substitute your own Python 3 interpreter command below, be it py, py3, python, or python3, if it is different than
'python' used below. Best practice is to also upgrade pip first (pip install --upgrade pip).

## Prerequisites include:
- matplotlib==3.5.1
- networkx==2.6.3
- numpy==1.22.2
- pandas==1.4.1
- requests==2.27.1
- tabulate==0.8.9
- urllib3==1.26.8
- Flask=2.0.3
- natsort=8.1.0

## Mac/Linux instructions for command-line version:
  - >git clone https://github.com/hellums/lacey-bacon.git
  - >cd lacey-bacon
  - >python -m venv env
  - >source env/bin/activate  
  - >pip install -r requirements.txt
  - >python romcom.py

## Windows instructions for command-line version:
Same as above, except replace the "source env/bin/activate" command in step 4 with 
  - >env\Scripts\activate (or activate.bat)

## To view Jupyter Notebook output and data analysis
- [Notebook/EDA](https://github.com/hellums/lacey-bacon/blob/root/romcomEDA.pdf)
(or open romcomEDA.pdf in the project folder using Adobe or other PDF viewer)

## To run a few unit tests for data integrity
(OPTIONAL) To test functions and data:
  - >python -m unittest test_romcom -v

(OPTIONAL) To test SQLite3 database:
  - >python romcomSQL.py

## Clean Up
- To get everything back to normal and remove files, type deactivate, then remove the lacey-bacon directory. Your system will be back to normal, as before the test.

# Satisfaction of Code Louisville Requirements
Requirements are called out in code, just search for "Code Louisville" in the python files

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

# Technologies Used in Class and Project
- GitHub, Git
- Slack, Pluralsight
- Visual Studio Code
- Python, Anaconda
- Flask, Jinja
- APIs
- HTML, CSS, Bootstrap
- SQLite3
- Unittest
- Jupyter Notebook
- Pandas
- Matplotlib 
- Networkx (node/edge, centrality)
- Selenium, BeautifulSoup (supplemental work, not in submission)
- Docker (introductory)
- Cookiecutter (introductory)
- IMDB (data source for movies and custom watchlist)
- "Balanced" scale, 1 witch, 1 duck, very small rocks (that float)
- 2 African swallows, 1 coconut, twine for sling-loading

# EXTENDED FUNCTIONALITY (Not Part of Code Louisville submission)
# Related Pages
- [Kanban board](https://github.com/hellums/lacey-bacon/projects/1) for managing project schedule
- [Issues](https://github.com/hellums/lacey-bacon/issues) for incident management
- [Wiki](https://github.com/hellums/lacey-bacon/wiki/1.-Data-Analytics-Course-Project) for related project links and information

(OPTIONAL) To Launch the Flask Web Server and RomCom Web Client:
  - >python romcomWeb.py
  - >in a web browser tab, go to http://localhost:5000/ 
    <p><img src="https://user-images.githubusercontent.com/83464025/157280420-8e86c900-60eb-4b0f-a4c9-f332698ba291.png" ></p>

(OPTIONAL) To Launch the Flask API Server and RomCom API Client:
  - >python romcomAPI.py
  - >in a web browser tab, http://localhost:8080/actors will return top 10 actors in JSON simple list format  
    <p><img src="https://user-images.githubusercontent.com/83464025/157280816-da3468ad-3ffe-482f-8161-ed3696d6c61c.png" ></p>
  
  - >http://localhost:8080/movies will return the top 10 movies in JSON simple list format
  - >http://localhost:8080/rating/?tt=tt13831504 will return the rating of "It Was Always You" (IMDB title code tt13831504) as JSON list 

(OPTIONAL) To perform full download of all IMDB data, and rebuild data structures:
  - >python romcomPrep.py 
  
  - (NOTE: compressed files total 4 GB, uncompressed another 2 GB)




