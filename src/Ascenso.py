#!/usr/bin/py
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division
from sympy import *
from findOptimum import *
from Parse import *
from pylatex import Document, Section, Math, Package, TikZ, Axis, Plot
import os

def conditional(nabla):
	evalu = [ True if abs(N(nab)) > 10e-6 else False for nab in nabla ]
	return sum(evalu)

def Ascenso(objective, varbls, f, punto):
	l      = Symbol("r")
	s      = Symbol("x")
	varbls = [ Symbol(var) for var in varbls if var in f ]
	f      = Lambda(varbls, f)

	Nabla = [ Lambda(varbls, diff(f(*flatten(varbls)),var)) for var in varbls ]

	punto = Matrix(punto)
	count = 1

	nabla_eval = Matrix([ Nab(*flatten(punto)) for Nab in Nabla ])

	out = open("../data/data.out", "w")

	### Para crear el .pdf con latex
	doc = Document()
	doc.packages.append(Package('geometry', options=['margin=1in']))
	doc.packages.append(Package('inputenc', options=['utf8']))
	doc.packages.append(Package('babel', options=['spanish', 'activeacute']))
	doc.packages.append(Package('enumerate'))
	doc.packages.append(Package('amsthm'))
	doc.packages.append(Package('amssymb'))
	doc.packages.append(Package('amsmath'))
	doc.append('\\decimalpoint')

	doc.append('Maximizar:' if objective else 'Minimizar:')
	doc.append(Math(data = ['f('+ parseVarbls(varbls) + ')=' + parseFunction(f, varbls)] ))
	doc.append('Derivando la función:')

	doc.append('\\begin{align*}')
	for i in range(len(Nabla)):
		out.write('D_' + str(varbls[i]) + " = " + str(Nabla[i](*flatten(varbls))).replace('**', '^') + '\n' )
		doc.append('\\nabla f_{' + str(varbls[i]) + "} & = " + parseFunction(Nabla[i], varbls) + '\\\\' )
	doc.append('\\end{align*}')

	doc.append('Tomamos como punto inicial $p_0 =('+parseVarbls(list(punto))+')$.\
		Iterando con el método del \\textit{ascenso/descenso más pronunciado} obtenemos:$$$$')

	condition = conditional(nabla_eval)

	while(condition > 0):

		### latex
		doc.append('\\textbf{Iteración '+str(count)+'.}\\\\')
		doc.append('Evaluamos $\\nabla f$ en el punto $p_{'+str(count-1)+'}=(' + parseVarbls([round(c, 3) for c in punto]) + \
			')$, entonces $\\nabla f =(' + parseVarbls([round(c, 3) for c in nabla_eval]) + ')$. Obteniendo $h(r)$:')


		h = Lambda(l, f(*flatten(punto + l*nabla_eval)))
		l_nopt = findOptimum(h, objective)
		punto = punto + l_nopt*nabla_eval


		### salida
		out.write("\nIteración " + str(count)+'\\\\')
		out.write("\n\nNabla(p_" + str(count - 1) + ") = " +  str(list(nabla_eval)) + "\n")
		out.write(("\nMAX " if objective == 1 else "\nMIN ") + "h(r)=" + str(h(l)).replace('**', '^'))
		out.write("\nlamb = " + str(l_nopt) + "\n")
		out.write('\np_' + str(count) + ' = ' + str(list(punto)) + '\n')

		
		### latex
		doc.append(Math(data=['h(r)='+parseFunction(h, [l])]))
		doc.append(('Maximizando' if objective else 'Minimizando')+' $h$ encontramos $r$='+str(round(l_nopt, 3))+'.\
			Así $p_{'+str(count)+'}$=('+parseVarbls([round(c, 3) for c in punto])+').$$$$')

		with doc.create(TikZ()):
			plot_options = 'height=9cm, width=9cm, xmin=' + str(l_nopt-5)
			with doc.create(Axis(options=plot_options)) as plot:
				plot_options = 'smooth, red'
				functoplot = str(h(s).expand()).replace('**', '^')
				plot.append(Plot(name='h(r)', func=functoplot, options=plot_options))
				plot.append(Plot(name='(h(r),r)', coordinates=[[N(l_nopt), N(h(l_nopt))]]))

		doc.append('$$$$')


		nabla_eval = Matrix([ N(Nab(*flatten(punto))) for Nab in Nabla ])
		condition = conditional(nabla_eval)
		count = count + 1

	### latex
	doc.append('Por lo tanto el punto '+('máximo' if objective else 'mínimo')+' es: ('+parseVarbls([round(c, 3) for c in punto])+')')

	doc.generate_pdf('ascenso')
	os.system('mv ascenso.pdf ../pdfs/ascenso.pdf')
	os.system('okular ../pdfs/ascenso.pdf &')
 
	out.close()


if __name__ == "__main__":
    act = 1
    varbls = ['x1', 'x2']
    f = '-(x1-3)**2-(x2-2)**2'
    p = [0, 0]
    Ascenso(act, varbls, f, p)
