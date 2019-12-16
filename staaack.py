import dis
import re
import hashlib


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

def simpleStuff():
    x = 1
    y = 1.9
    p = 5*x
    z = (1,1.5*y,9)
    q = [1,2,3,4,5]
    r = z[0]

#dis.dis(main)

def LOAD_CONST(pyInstr, state):
    def checkVal(val):
        if(isinstance(val,int)):
            return ('PUSHINT %d' % val,)
        elif(isinstance(val,float)):
            return ('PUSHFLOAT %10.10f' % val,)
        elif(isinstance(val,tuple)):
            vals = ()
            for subitem in val:
                vals += checkVal(subitem)
            return vals
        else: return ()
    return state + checkVal(pyInstr.argval)

def LOAD_FAST(pyInstr,state):
    return state + ('PUSHVAR %s' % varNameEncode(pyInstr.argval),)

def STORE_FAST(pyInstr,state):
    # need to modify this to work for lists and tuples
    # need to add variable mapping thing in the state model
    return ('PUSHVAR %s # %s' % (varNameEncode(pyInstr.argval), pyInstr.argval), ) + state + ('ASSIGN',)

def SIMPLE(name):
    return lambda pyInstr,state: state + (name,)

def varNameEncode(var):
    return hashlib.md5(var.encode()).hexdigest()

instrMap = {
    'LOAD_CONST': LOAD_CONST,
    'STORE_FAST': STORE_FAST,
    'LOAD_FAST' : LOAD_FAST,
    'BINARY_MULTIPLY': SIMPLE('MULT')
}

state = ()
for instr in dis.Bytecode(simpleStuff):
    
    if(instr.starts_line != None):
        [print(line) for line in state]
        state = ()
    print(instr)
    if(instr.opname in instrMap):
        state = instrMap[instr.opname](instr, state)
        
    if(instr.opname== 'RETURN_VALUE'):
        [print(line) for line in state]


