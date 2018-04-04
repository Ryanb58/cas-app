venv: requirements.txt
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt
	touch venv

deps: venv

run: deps
	venv/bin/python manage.py runserver

