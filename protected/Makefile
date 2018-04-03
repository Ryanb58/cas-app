venv: requirements.txt
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt
	touch venv

deps: venv

test: deps
	venv/bin/python manage.py test

run: deps
	venv/bin/python manage.py runserver

