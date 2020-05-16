.PHONY: clean-build

VERSION=$(shell python3 setup.py --version)

dev:
	pip3 install --upgrade pip
	pip3 install wheel
	pip3 install setuptools
	pip3 install -r requirements-ci.txt

clean:
	rm -rfv build/
	rm -rfv dist/
	rm -rfv *.egg-info
	find . -name '*.pyc' -exec rm -fv {} +

test:
	python -m nose -v --ignore-files="test_robot_run_python\.py"

build: clean dev test
	python3 setup.py sdist bdist_wheel
