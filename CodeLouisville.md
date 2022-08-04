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
