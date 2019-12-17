import dis
import re
import hashlib

def LOAD_CONST(pyInstr, state):
    def checkVal(val):
        if(isinstance(val,int)):
            return ('PUSHINT %d' % val,)
        elif(isinstance(val,float)):
            return ('PUSHFLOAT %10.10f' % val,)
        elif(val == None):
            return ('PUSHINT 0',)
        elif(isinstance(val,tuple)):
            vals = ()
            for subitem in val:
                vals += checkVal(subitem)
            return vals
        else: return ()
    return state + checkVal(pyInstr.argval)

def LOAD_FAST(pyInstr,state):
    return state + ('PUSHVAR %s # %s' % (varNameEncode(pyInstr.argval), pyInstr.argval ), )

def STORE_FAST(pyInstr,state):
    # need to modify this to work for lists and tuples
    # need to add variable mapping thing in the state model
    return ('PUSHVAR %s # %s' % (varNameEncode(pyInstr.argval), pyInstr.argval), ) + state + ('ASSIGN',)

def SIMPLE(name):
    return lambda pyInstr,state: state + (name,)

def COMPARE_OP(pyInstr,state):
    map = { 
        '!=':'NEQ',
        '==': 'EQU',
        '>=':'GTE',
        '<=':'LTE',
        '>':'GT',
        '<':'LT',
    }
    return state + ('%s' % (map[pyInstr.argval]) ,)

def POP_JUMP_IF_FALSE(pyInstr,state):
    return state + ('BEZ %s' % 'LABEL',) #INCOMPLETE!

def varNameEncode(var):
    return hashlib.md5(var.encode()).hexdigest()

instrMap = {
    'LOAD_CONST': LOAD_CONST,
    'STORE_FAST': STORE_FAST,
    'LOAD_FAST' : LOAD_FAST,
    'BINARY_MULTIPLY': SIMPLE('MULT'),
    'BINARY_SUBTRACT': SIMPLE('SUB'),
    'BINARY_ADD': SIMPLE('ADD'),
    'BINARY_TRUE_DIVIDE': SIMPLE('DIV'),
    'POP_TOP': SIMPLE('POP'),
    'COMPARE_OP': COMPARE_OP,
    'UNARY_NOT': SIMPLE('NOT'),
    'RETURN_VALUE': SIMPLE('END_OF_FUNCTION'),
    'POP_JUMP_IF_FALSE': POP_JUMP_IF_FALSE,
    #'BINARY_POWER': 
}

def parse(func):
    state = ()
    for instr in dis.Bytecode(func):
        
        if(instr.starts_line != None):
            [print(line) for line in state]
            state = ()
        print(instr)
        if(instr.opname in instrMap):
            state = instrMap[instr.opname](instr, state)
            
        if(instr.opname== 'RETURN_VALUE'):
            [print(line) for line in state]
