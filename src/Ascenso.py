#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from findOptimum import *

def conditional(nabla):
	evalu = [ True if abs(N(nab)) > 10e-6 else False for nab in nabla ]
	return sum(evalu)

def Ascenso(objective, varbls, f, punto):
	l = Symbol("lamb")
	varbls = [ Symbol(var) for var in varbls if var in f ]
	f = Lambda(varbls, f)

	Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

	punto = Matrix([ float(l) for l in punto ])

	nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

	condition = conditional(nabla_eval)

	while(condition > 0):
		h = Lambda(l, f(*flatten(punto + l*nabla_eval)))

		l_nopt = findOptimum(h, objective)

		punto = punto + l_nopt*nabla_eval

		nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])

		condition = conditional(nabla_eval)
	document = open("../data/data.out","w")
	document.write(str(punto[0]))
	document.close()


if __name__ == "__main__":
    act = 1
    varbls = ['x1', 'x2']
    f = '-(x1-3)**2-(x2-2)**2'
    p = [0, 0]
    Ascenso(act, varbls, f, p)