run: main.py display.py draw.py matrix.py parser.py
	if ! python main.py script -v; then python2.7 main.py script -v; fi

debug:
	if ! python main.py script -dv; then python2.7 main.py script -dv; fi

clean:
	rm *.pyc
	rm *~
