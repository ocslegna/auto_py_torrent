init:
	pip3 install -r requirements.txt

publish:
	pip3 install 'twine>=1.9.1'
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info