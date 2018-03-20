from display import *
from draw import *
from parser import *
from matrix import *
import sys

def _occur_list(thing,list):
	o = 0
	for t in list:
		if t == thing:
			o += 1
	return o

if __name__ == '__main__':
	if '--help' in sys.argv:
		print man
		exit(0)
	debug = '--debug' in sys.argv
	verbose = _occur_list('--verbose',sys.argv)
	for arg in sys.argv:
		if arg[0] == '-' and arg[1] != '-':
			for letter in arg:
				if letter == 'd':
					debug = True
				elif letter == 'v':
					verbose += 1
				elif letter == 'h':
					print man
					exit(0)
				elif letter == '-':
					pass
				else:
					print "unknown flag: " + letter
					exit(1)
	if debug and verbose == 0:
		verbose = 1
	if len(sys.argv) > 1:	
		if sys.argv[1][0] != '-':
			parse_file(sys.argv[1],debug,verbose)
			exit(0)
	parse_file('-',debug,verbose)
