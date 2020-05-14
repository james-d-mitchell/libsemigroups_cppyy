black: 
	black setup.py libsemigroups_cppyy/*.py tests/*.py

check:
	tox -- -x tests/

# JDM: couldn't get the coverage target to work outside a virtual env
coverage:
	pip install .
	coverage run -m nose --where tests/
	coverage html
	@echo "See: htmlcov/index.html" 
