init:
	pip install -r requirements.txt

publish:
	pip install 'twine>=1.9.1'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info