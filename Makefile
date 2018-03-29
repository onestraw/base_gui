check:
	@flake8 base_gui/config.py base_gui/base_window.py

install:
	pip install .

run:
	python demo/demo.py

build:
	pyinstaller -F -s -w -i demo/favicon.ico demo/demo.py

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} \;

distclean: clean_pyc
	rm -rf build/ dist/ demo.spec
