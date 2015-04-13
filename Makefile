build:
	python setup.py sdist bdist_wheel

publish:
	python setup.py sdist bdist_wheel upload

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -delete
	rm -rf m2x.egg-info dist build

.PHONY: build publish clean
