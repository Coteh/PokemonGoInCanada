all: deps
	pyinstaller ./main.py

deps:
	pip install pyinstaller

test: deps
	pyinstaller ./test.py
