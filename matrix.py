import math

def make_translate( x, y, z ):
	m = ident(4)
	m[3][0] = x
	m[3][1] = y
	m[3][2] = z
	return m

def make_scale( x, y, z ):
	m = new_matrix(4,4)
	m[0][0] = x
	m[1][1] = y
	m[2][2] = z
	m[3][3] = 1
	return m

def make_rotX( theta ):    
    return \
		[
			[  1 ,         0       ,         0       , 0 ],
			[  0 , math.cos(theta) , math.sin(theta) , 0 ],
			[  0 ,-math.sin(theta) , math.cos(theta) , 0 ],
			[  0 ,         1       ,         0       , 1 ],
		]

def make_rotY( theta ):
	return \
		[
			[ math.cos(theta) ,   0,-math.sin(theta) , 0 ],
			[         0       ,   1,         0       , 0 ],
			[ math.sin(theta) ,   0, math.cos(theta) , 0 ],
			[         0       ,   0,         0       , 1 ],
		]

def make_rotZ( theta ):
	return \
		[
			[  math.cos(theta),  math.sin(theta),   0, 0 ],
			[ -math.sin(theta),  math.cos(theta),   0, 0 ],
			[         0       ,         0       ,   1, 0 ],
			[         0       ,         0       ,   0, 1 ],
		]

def print_matrix( matrix ):
	rows = len(matrix)
	cols = len(matrix[0])
	for row in xrange(rows):
		print '[ ',
		for col in xrange(cols):
			s = str(matrix[row][col])
			print ' ' * (3 - len(s)) + s + ' ',
		print ']'

def ident( r ):
	l = r
	m = new_matrix(rows=l,cols=l)
	for i in xrange( l ):
		m[i][i] = 1
	return m

#m1 * m2 -> m2
def matrix_mult( m1, m2 ):
	if(len(m1[0]) == len(m2)):
		rows = len(m1)
		cols = len(m2[0])
		m = new_matrix(rows,cols)
		for row in xrange(len(m1)):
			m2c = xrange(len(m2[0]))
			for i in xrange(len(m1[0])):
				for col in m2c:
					m[row][col] += m1[row][i] * m2[i][col]
		return m
	else:
		return None


def new_matrix(rows = 4, cols = 4):
    m = []
    for r in xrange( rows ):
        m.append( [] )
        for c in xrange( cols ):
            m[r].append( 0 )
    return m
