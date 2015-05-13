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

def conjugados(objective, varbls, f, punto):
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
	
	condition = conditional(nabla_eval)

	while(condition > 0):


		maxi = -10e10
		ind  = 0
		for i in range(0, len(nabla_eval)):
			if (abs(nabla_eval[i]) > maxi):
				maxi = abs(nabla_eval[i])
				ind  = i

		done = False
		for i in range(0, len(nabla_eval)):
			if abs(abs(nabla_eval[i])-maxi) > 10e-6 or done:
				nabla_eval[i] = 0
			else:
				done = True


		### latex
		doc.append('\\textbf{Iteración '+str(count)+'.}\\\\')
		doc.append('Evaluamos $\\nabla f$ en el punto $p_{'+str(count-1)+'}=(' + parseVarbls([round(c, 3) for c in punto]) + \
			')$, entonces $\\nabla f =(' + parseVarbls([round(c, 3) for c in nabla_eval]) + ')$. Encontramos que el máximo delta'+ \
			' se encuentra en $'+str(varbls[ind])+'$. Obteniendo $h(r)$:')


		h = Lambda(l, f(*flatten(punto + l*nabla_eval)))
		l_nopt = findOptimum(h, objective)
		punto = punto + l_nopt*nabla_eval


		### salida
		out.write("\nIteración " + str(count))
		out.write("\n\nNabla(p_" + str(count - 1) + ") = " +  str(list(nabla_eval)) + "\n")
		out.write(("\nMAX " if objective == 1 else "\nMIN ") + "h(lamb)=" + str(h(l)).replace('**', '^'))
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
		count     = count + 1

	### latex
	doc.append('Por lo tanto el punto '+('máximo' if objective else 'mínimo')+' es: ('+parseVarbls([round(c, 3) for c in punto])+')')
<<<<<<< HEAD
	doc.generate_pdf('conjugados')
	os.system('mv conjugados.pdf ../pdfs/conjugados.pdf')
	os.system('okular ../pdfs/conjugados.pdf &')
=======
	doc.generate_pdf()
	os.system('qpdfview default_filename.pdf &')
>>>>>>> f56f3d0ec65bb6dc170856c95bea9bdfe6a5395d

	out.close()


if __name__ == "__main__":
    act = 1
    varbls = ['x1', 'x2']
    #f = '4*(x1+x2)+x1*x2-exp(x1)-exp(2*x2)'
    f = '-(x1-3)**2-(x2-2)**2'
    p = [0, 0]
    conjugados(act, varbls, f, p)