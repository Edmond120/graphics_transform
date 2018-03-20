from display import *
from matrix import *
from draw import *
import traceback

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
transform = new_matrix()

quit_flag = False
man = """
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""

def to_int(matrix):
	m = []
	for row in matrix:
		r = []
		for col in row:
			r.append(int(col))
		m.append(r)
	return m

def _raw_input( file, debug, verbose):
	try:
		return raw_input() + '\n'
	except EOFError:
		return ''

def _file(file, debug=False, verbose=0):
	line = file.readline()
	if verbose > 0:
		print line
	return line

def _print_matrix(title,matrix):
	print title
	print "--------------------"
	print_matrix(matrix)
	print ''

def parse_line( line, debug=False, verbose=0):
	global edges, transform, screen, color, quit_flag
	if(line == '\n'):
		return
	try:
		args = line.split()
		if args[0] == 'ident':
			transform = ident(4)
			if(verbose > 0):
				_print_matrix("Transfrom", transform)
			return
		elif args[0] == 'scale':
			if(len(args) <= 3):
				print "not enough args"
			else:
				scale = make_scale(float(args[1]), float(args[2]), float(args[3]))
				transform = matrix_mult(transform,scale)
				if(verbose > 0):
					_print_matrix("Scale", scale)
					_print_matrix("Transform", transform)
				return
		elif args[0] == 'move':
			if(len(args) <= 3):
				print "not enough args"
			else:
				translate = make_translate(int(args[1]),int(args[2]),int(args[3]))
				transform = matrix_mult(transform,translate)
				if(verbose > 0):
					_print_matrix("Translate", translate)
					_print_matrix("Transform", transform)
				return
		elif args[0] == 'help':
			print man
			return
		elif args[0] == 'quit':
			if(verbose > 0):
				print 'exiting'
			quit_flag = True
			return
		elif args[0] == 'apply':
			edges = matrix_mult(edges,transform)
			if(verbose > 0):
				_print_matrix("edges", edges)
			return
		elif args[0] == 'rotate':
			no_error = False
			rotate_matrix = None
			if(len(args) <= 2):
				print "not enough args"
			else:
				no_error = True
				if(args[1] == 'x'):
					rotate_matrix = make_rotX(float(args[2]))
				elif(args[1] == 'y'):
					rotate_matrix = make_rotY(float(args[2]))
				elif(args[1] == 'z'):
					rotate_matrix = make_rotZ(float(args[2]))
				else:
					print "invalid argument"
					no_error = False
			if(no_error):
				t1 = make_translate( -XRES/2, -YRES/2, 0)
				t2 = make_translate(  XRES/2,  YRES/2, 0)
				transform = matrix_mult(transform,t1)
				transform = matrix_mult(transform,rotate_matrix)
				transform = matrix_mult(transform,t2)
			if(no_error and verbose > 0):
				print "translating to orgin before rotating"
				_print_matrix("Rotate", rotate_matrix)
				print "translating back"
				_print_matrix("Transform", transform)
			if(no_error):
				return
		elif args[0] == 'line':
			if(len(args) <= 6):
				print "not enough args"
			else:
				add_edge(edges,int(args[1]),int(args[2]),\
							   int(args[3]),int(args[4]),\
							   int(args[5]),int(args[6]))
				if(verbose > 0):
					_print_matrix("Edges",edges)
				return
		elif args[0] == 'save':
			if(len(args) <= 1):
				print "not enough args"
			else:
				save_extension(screen,args[1])
				if(verbose > 0):
					print "saved screen as: " + args[1]
				return
		elif args[0] == 'display':
			screen = new_screen()
			draw_lines(to_int(edges),screen,color)
			display(screen)
			if(verbose > 0):
				print "finished display"
			return
		elif args[0] == 'clear':
			clear_screen(screen)
			if(verbose > 0):
				print "screen cleared"
			return
		elif args[0] == 'debug':
			debug = True
		else:
			print "no such command: " + args[0]
	except:
		traceback.print_exc()
	if debug:
		try:
			while(not quit_flag):
				debug_args = raw_input('debug: ').split()
				if(len(debug_args) > 0):
					if(debug_args[0] == 'manual_override'):
						print "debug mode= manual_override: "
						debug_line = _raw_input(None, debug, verbose)
						while(debug_line != ''):
							parse_line(debug_line)
							print "debug mode= manual_override: "
							debug_line = _raw_input(None, debug, verbose)
					elif(debug_args[0] == 'continue'):
						print "continueing..."
						return
					else:
						print "no such command: " + debug_args[0]
		except EOFError:
			print "\ncontinueing..."
			return
	else:
		print "error status: uncorrected\n"
		return


def parse_file( fname, debug=False, verbose=0 ):
	global edges, transfrom, screen, color, quit_flag
	if fname == '-':
		input_function = _raw_input
		file = None
		debug = False
	else:
		#check for file not found exception
		input_function = _file
		file = open(fname, 'r')
	line = input_function(file, debug, verbose)
	while(line != ''):
		parse_line(line, debug, verbose)
		if(quit_flag):
			break
		line = input_function(file, debug, verbose)
