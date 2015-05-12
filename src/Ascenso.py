#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from string import ascii_letters
from Newton import newton

def conditional(nabla):
	evalu = [ True if abs(N(nab)) > 10e-6 else False for nab in nabla ]
	return sum(evalu)


objective = bool(input("Object = "))
f = input("f = ")
varbls = input("vars = ").split()

l = Symbol("lamb")
varbls = [ Symbol(var) for var in varbls if var in f ]
f = Lambda(varbls, f)

Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

punto = input("v = ").split()
punto = Matrix([ float(l) for l in punto ])

nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

condition = conditional(nabla_eval)

while(condition > 0):
	h = Lambda(l, f(*flatten(punto + l*nabla_eval)))
	h_diff = Lambda(l, diff(h(l),l))

	#l_n = solve(sympify(h_diff(l)), l)
	#l_n = [ sympify(sol) for sol in l_n if N(sol).is_real ]

	'''if len(l_n) > 1:
		l_nopt = l_n[0]
		for j in range(1, len(l_n)):
			if h(l_n[j]) > h(l_nopt) and o:
				l_nopt = l_n[j]
			elif h(l_n[j]) < h(l_nopt) and not o:
				l_nopt = l_n[j]
	else:
		l_nopt = l_n[0]'''
	l_nopt = newton(h)

	punto = punto + l_nopt*nabla_eval

	nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])

	condition = conditional(nabla_eval)
print(punto)