env/bin/activate: requirements.txt
	python3 -m venv env
	./env/bin/pip3 install -r requirements.txt

build: romcomPrep.py
	./env/bin/python3 romcomPrep.py
	
test: env/bin/activate romcomSQL.py test_romcom.py
	./env/bin/python3 romcomSQL.py
	./env/bin/python3 -m unittest test_romcom -v

run: env/bin/activate
	./env/bin/python3 romcom.py

refresh: romcomPrep.py
	./env/bin/python3 romcomPrep.py

clean: *.pkl.gz *.tsv.gz *.tsv __pycache__
	rm *.tsv.gz
	rm *.tsv
	rm -rf __pycache__

