PROGNAME := PokemonGoInCanada
TESTNAME := PokemonGoInCanadaTests

all: deps
	pyinstaller ./main.py -n $(PROGNAME)

deps:
	pip install pyinstaller

test: deps
	pyinstaller ./test.py -n $(TESTNAME)
