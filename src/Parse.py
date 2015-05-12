
def parseProblem(myProblem):
    myProblem = myProblem.split("\n")
    
    if myProblem[0].upper() == "MAXIMIZAR":
        act = 1
    elif myProblem[0].upper() == "MINIMIZAR":
        act = 0
    else:
        return None
    del myProblem[0]

    funcion = myProblem[0].replace(' ','').split('=')
    variables = funcion[0].strip('fgh()').split(',')
    funcion = funcion[1]
    del myProblem[0]

    p = myProblem[0].replace(' ','').strip('()').split(',')

    return act, variables, funcion


def writeDoc(act, variables, funcion):
    document = open("../Data/data.in","w")
    document.write(str(act)+"\n")
    for var in variables:
        document.write(var+" ")
    document.write("\n"+funcion)
    document.close()


if __name__ == "__main__":
    myProblem = "Maximizar\n\
f(x1,x2) = -(x1-3)**2-(x2-2)**2\n\
p = (0,0)"
    result = parseProblem(myProblem)
    print(result)
    writeDoc(result[0],result[1],result[2])