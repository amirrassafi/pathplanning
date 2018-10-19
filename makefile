venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv --python=/usr/bin/python3.6
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

