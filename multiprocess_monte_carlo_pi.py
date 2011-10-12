#!/usr/bin/env python

from multiprocessing import Pool
import numpy as np

# points per call
N = 5e6
# number of calls
M = 100
# threads
C = 8

def find_pi(m):
	np.random.seed()
	x1 = np.random.random(N)
	y1 = np.random.random(N)
	np.square(x1,x1)
	np.square(y1,y1)
	np.add(x1,y1,x1)
	np.less_equal(x1, 1.0, x1)
	return np.add.reduce(x1)*4.0/N


if __name__ == '__main__':
	p = Pool(C)

	results = p.map(find_pi, range(M))
	print reduce(lambda x,y: (x+y)/2, results)
