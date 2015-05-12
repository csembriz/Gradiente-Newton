#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from string import ascii_letters
from findOptimum import *

def conditional(nabla):
	evalu = [ True if abs(N(nab)) > 10e-6 else False for nab in nabla ]
	return sum(evalu)


objective = bool(input("Object = "))
f = input("f = ")
varbls = input("varibales: ").split()

l = Symbol("lamb")
varbls = [ Symbol(var) for var in varbls if var in f ]
print (varbls)

f = Lambda(varbls, f)

Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

punto = input("v = ").split()
punto = Matrix([ float(l) for l in punto ])

nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

condition = conditional(nabla_eval)

while(condition > 0):

	maxi = -10e10
	for delt in nabla_eval:
		maxi = max(maxi, abs(delt))

	done = False
	for i in range(0, len(nabla_eval)):
		if abs(abs(nabla_eval[i])-maxi) > 10e-6 or done:
			nabla_eval[i] = 0
		else:
			done = True

	h = Lambda(l, f(*flatten(punto + l*nabla_eval)))
	#print (h)
	h_diff = Lambda(l, diff(h(l),l))

	#l_nopt = solve(sympify(h_diff(l)), l)
	l_nopt = findOptimum(h, objective)

	#print(l_nopt)
	#print("IC:", findOptimum(h, objective))

	punto = punto + l_nopt*nabla_eval

	nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])

	condition = conditional(nabla_eval)

print(punto)