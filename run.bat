 @echo off
echo.   
echo First step is to set up environment and install prerequisites. No interaction needed at this point.
pause
@REM let's try each of the possible commands that python version 3 may be using on Windows
py3 -m venv env
if %ERRORLEVEL% neq 0 goto Python3
:Python3
python3 -m venv env
if %ERRORLEVEL% neq 0 goto Python
:Python
python -m venv env
if %ERRORLEVEL% neq 0 exit /b 1
@REM continue on, if one version of python installed VENV correctly
.\env\Scripts\pip install -r requirements.txt
echo.
echo Next step runs a few tests of SQL database and tables. No interaction needed, you should just see a few query results and table sizes.
pause
.\env\Scripts\python romcomSQL.py
echo. 
echo Next step runs test of data structures and functions. No interaction needed, you should just see that 5 tests passed.
pause
.\env\Scripts\python -m unittest test_romcom
echo.
echo Next step runs the command line program main loop. This will involve interaction. When you select quit, you will return here.
pause
.\env\Scripts\python romcom.py
echo Next step runs the Flask engine and launches the web interface in the default browser. Interact as you wish, then close both windows and return here.
pause
start .\env\Scripts\python romcomWeb.py
start http://localhost:5000
echo.
echo Next step runs the Flask engine and launches the API interface in the default browser. Interact as you wish, then close both windows and return here.
pause
start .\env\Scripts\python romcomAPI.py
start http://localhost:8080
echo.
echo This concludes the demonstration of the Hallmark romcom application and academic project.
pause
echo.
echo Don't have a good day. Have a GREAT day!
