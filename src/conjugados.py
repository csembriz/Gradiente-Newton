#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from findOptimum import *


def conditional(nabla):
	evalu = [ True if abs(N(nab)) > 10e-6 else False for nab in nabla ]
	return sum(evalu)

def conjugados(objective, varbls, f, punto):
	l      = Symbol("lamb")
	varbls = [ Symbol(var) for var in varbls if var in f ]
	f      = Lambda(varbls, f)

	Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

	punto = Matrix(punto)
	count = 1

	nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

	out = open("../data/data.out", "w")
	for i in range(len(Nabla)):
		out.write('D_' + str(varbls[i]) + " = " + str(Nabla[i](*flatten(varbls))).replace('**', '^') + '\n' )

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

		out.write('\np_' + str(count) + ' = ' + str(list(punto)))

		nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])

		condition = conditional(nabla_eval)
		count     = count + 1

	out.close()


if __name__ == "__main__":
    act = 1
    varbls = ['x1', 'x2']
    f = '-(x1-3)**2-(x2-2)**2'
    p = [0, 0]
    conjugados(act, varbls, f, p)