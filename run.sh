echo   
echo "First step is to set up environment and install prerequisites. No interaction needed at this point."
printf "%s " "Press enter to continue"
read ans
python3 -m venv env
env/bin/pip3 install -r requirements.txt
echo
echo "Next step runs a few tests of SQL database and tables. No interaction needed, you should just see a few query results and table sizes."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 romcomSQL.py
echo
echo "Next step runs test of data structures and functions. No interaction needed, you should just see that 5 tests passed."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 -m unittest test_romcom
echo
echo "Next step runs the command line program main loop. This will involve interaction. When you select quit, you will return here."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 romcom.py
echo "Next step runs the class-based command line main loop. This will involve interaction. When you select quit, you will return here."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 romcomClass.py
echo "Next step runs the Flask engine and launches the web interface in the default browser. Interact as you wish, then close the window and click back here."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 romcomWeb.py &
sleep 5
open http://localhost:5000 
echo "Next step runs the Flask engine and launches the API interface in the default browser. Interact as you wish, then close the window and click back here."
printf "%s " "Press enter to continue"
read ans
env/bin/python3 romcomAPI.py &
sleep 5
open http://localhost:8080 
echo
echo "This concludes the demonstration of the Hallmark romcom application and academic project."
printf "%s " "Press enter to continue"
read ans
echo
echo "Don't have a good day. Have a GREAT day!"