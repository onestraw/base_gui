
run:
	python demo.py

build:
	pyinstaller -F -s -w -i favicon.ico demo.py

check:
	@flake8 base_gui.py

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} \;

distclean: clean_pyc
	rm -rf build/ dist/ demo.spec
