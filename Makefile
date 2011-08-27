.PHONY: test

test:
	@coverage run --omit=/tmp/*,*tests/* -m unittest discover src/adama/tests

report: test
	@coverage html
	@chromium-browser htmlcov/index.html
