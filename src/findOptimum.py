#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from random import *

def Newton(g, x0):
	r   = Symbol("r")
	g_  = Lambda(r, diff(g(r)))
	g__ = Lambda(r, diff(g(r)))
	xn  = x0

	limit = 100

	try:
		while limit > 0:
			#sig = xn - g(xn)/g_(xn)
			a = g(xn)
			b = g_(xn)
			c = g__(xn)
			sig = xn - (a*b)/(b**2 - a*c)
			if (abs(sig-xn) < 10e-5):
				break

			xn = sig
			limit -= 1

	except:
		pass

	return xn

def findOptimum(h, objective):
	r   = Symbol("r")
	dh  = Lambda(r, diff(h(r)))
	seed(None)

	#print (h)
	mroot = None
	lsup  = 100
	linf  = -100
	best  = (-10e8 if objective else 10e8)
	for i in range(0, 10):

		root = Newton(dh, uniform(lsup, linf))
		
		while abs(dh(root)) > 10:
			if dh(root) > -10 and dh(root) < 0:
				linf = root
			elif dh(root) > 10 and dh(root) > 0:
				lsup = root
			root = Newton(dh, uniform(lsup, linf))
		
		#print ("posible", root)
		if (abs(N(dh(root))) < 10e-5):
			if (objective):
				if (h(root) > best):
					mroot = root
					best  = h(root)
			else:
				if (h(root) < best):
					mroot = root
					best  = h(root)
	return mroot


if __name__ == "__main__":
    act = 1
    r = Symbol('r')
    f = Lambda(r, -(6*r-3)**2)
    print(findOptimum(f,act))