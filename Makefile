
PYTHON=`which python`
PYTHON3=`which python3`


all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make clean - Get rid of scratch and byte files"


source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	$(PYTHON) setup.py install
	$(PYTHON3) setup.py install


test: test2 test3

test2:
	$(PYTHON) -m pytest pytest_data_test.py

test3:
	$(PYTHON3) -m pytest pytest_data_test.py


clean:
	$(PYTHON) setup.py clean
	find . -name '*.pyc' -delete
