# OVERVIEW
Is Lacey Chabert indeed the "Center of the (Hallmark) Universe," as Kevin Bacon reputably is to Hollywood? This project addresses that proposition, using a [subset of IMDB listed movies](https://github.com/hellums/lacey-bacon/blob/root/watchlist.txt) and actors from Hallmark original movies, romantic comedies, mysteries, and dramas.  

All images and websites shown here belong to the original copyright holders and are used for academic and demonstration purposes only. Source and derived data is [publicly available and courtesy of IMDB](https://www.imdb.com/interfaces/).

# Project-Related Github Pages
- [Kanban board](https://github.com/hellums/lacey-bacon/projects/1) for managing project schedule
- [Issues](https://github.com/hellums/lacey-bacon/issues) for incident management
- [Wiki](https://github.com/hellums/lacey-bacon/wiki/Data-Analytics-Course-Project) for related project links and information

# COMMAND-LINE WALKTHROUGH VIDEO
[<img alt="romcom video walkthrough" width="600px" src="images/romcom.jpg" />](https://screencast-o-matic.com/watch/c3e6FLVFY4U)

# Mac/Linux instructions:
  - >git clone https://github.com/hellums/lacey-bacon.git
  - >cd lacey-bacon
  - >python -m venv env
  - >source env/bin/activate
  - >pip install -r requirements.txt
  - >python romcom.py

# Windows instructions:
If using VSC, a DOS command prompt terminal is highly recommended, NOT PowerShell.

Perform same steps as above, except replace the "source env/bin/activate" command in step 4 with 
  - >env\Scripts\activate (or activate.bat)

# To view Jupyter Notebook output and data analysis
- [Notebook/EDA](https://github.com/hellums/lacey-bacon/blob/root/romcomEDA.pdf)

# FLASK API SCREENSHOT
<p><img alt="API screenshot" width="600px" src="https://user-images.githubusercontent.com/83464025/157280816-da3468ad-3ffe-482f-8161-ed3696d6c61c.png" ></p>

# To Launch the Flask API Server and RomCom API Client:
- >python romcomAPI.py
  - >in a web browser tab, http://localhost:8080/actors will return top 10 actors in JSON simple list format    
  - >http://localhost:8080/movies will return the top 10 movies in JSON simple list format
  - >http://localhost:8080/rating/?tt=tt13831504 will return the rating of "It Was Always You" (IMDB title code tt13831504) as JSON list 

# Database Refresh
To perform a full download of the current IMDB source files, and initialize or rebuild data structures (NOTE: requires 6 GB space, 3-5 minute compile time):
  - >python romcomPrep.py 

# Clean Up
- To get everything back to normal and remove files, type deactivate, then remove the lacey-bacon directory. Your system will be back to normal, as before the test.
