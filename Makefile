.PHONY: clean-build

VERSION=$(shell python3 setup.py --version)

clean-build:
	rm -rfv build/
	rm -rfv dist/
	rm -rfv *.egg-info
	find . -name '*.pyc' -exec rm -fv {} +

test:
	# python3 -m nose --with-json-extended
	nosetests --with-json-extended

build:
	python3 setup.py sdist bdist_wheel

deploy: clean-build test build
	pip3 install --upgrade dist/typetastic-$(VERSION).tar.gz
