#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from findOptimum import *

def Ascenso(objective, varbls, f, p):
	l = Symbol("lamb")
	varbls = [ Symbol(var) for var in varbls if var in f ]
	f = Lambda(varbls, f)

	Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

	nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

	condition = conditional(nabla_eval)

	while(condition > 0):
		h = Lambda(l, f(*flatten(punto + l*nabla_eval)))
		h_ = Lambda(l, diff(h(l),l))

		l_nopt = findOptimum(h_, objective)

		punto = punto + l_nopt*nabla_eval

		nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])

		condition = conditional(nabla_eval)
	print(punto)


if __name__ == "__main__":
    act = 1
    varbls = ['x1', 'x2']
    f = '-(x1-3)**2-(x2-2)**2'
    p = [0, 0]
    Ascenso(act, varbls, f, p)