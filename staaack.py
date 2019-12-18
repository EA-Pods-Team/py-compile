import SimpleCompiler as sc


def main():
    x = 1
    y = (5*2+x)
    z = (1,2,3,4,5)
    for i in z:
        print(i)
    def subfcn(a):
        b = a*5
        return b
    q = subfcn(x)
    return x*y*q

def assignment():
    x = 1
    y = 1.9
    p = 5
    z = (1,1.5,9)
    q = [1,2,3,4,5]
    r = z[0]

def arithmetic():
    x = 1
    y = 2
    x+y
    x-y
    x*y
    x/y

def logops():
    a = 5
    b = 9
    a == b
    a != b
    a > b
    a < b
    a >= b
    a <= b
    (not a)

def simpleIf():
    a = 5
    b = 9
    if(a == 2):
        c = 5
    d = 6
        

def flowops():
    a = 5
    b = 9
    if(a == 2):
        c = 5
    elif(b == 3):
        d = 6
    else:
        e = 7
    
    #(a or b)
    #(a and b)

#sc.parse(arithmetic)
#sc.parse(logops)
#sc.parse(simpleIf)
sc.parse(flowops)


