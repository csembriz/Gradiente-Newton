#!/usr/bin/py
# -*- coding: UTF-8 -*-

def parseProblem(myProblem):
    myProblem = myProblem.split("\n")
    
    if myProblem[0].upper() == "MAXIMIZAR":
        act = 1
    elif myProblem[0].upper() == "MINIMIZAR":
        act = 0
    else:
        return None
    del myProblem[0]

    funcion = myProblem[0].split('=')
    variables = funcion[0].replace(' ', '').strip('fgh()').split(',')
    funcion = funcion[1].replace('^', '**').replace(' ', '*')
    del myProblem[0]

    p = myProblem[0].replace(' ','')
    if p[0].upper()=="P":
        p = p.strip('p=()').split(',')
    else:
        p = [0, 0]

    return act, variables, funcion, p


def writeDoc(act, variables, funcion, point):
    document = open("../data/data.in","w")
    document.write(str(act)+"\n")
    for var in variables:
        document.write(var+" ")
    document.write("\n"+funcion+"\n")
    for var in point:
        document.write(var+" ")
    document.close()


def getDataSalida():
    file = open("../data/data.out", "r")
    lineas = file.readlines()
    cadena = ""
    for i in range(len(lineas)):
        for j in range(len(lineas[i])):
            cadena += lineas[i][j]
    return cadena


if __name__ == "__main__":
    myProblem = "Maximizar\n\
f(x1,x2) = -(x1-3)**2-(x2-2)**2\n\
p = (0,0)"
    result = parseProblem(myProblem)
    print(result)
    writeDoc(result[0],result[1],result[2], result[3])