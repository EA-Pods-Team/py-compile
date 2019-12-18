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
    
    state.lineState.extend( checkVal(pyInstr.argval) )

def LOAD_FAST(pyInstr,state):
    state.lineState.append( ('PUSHVAR %s # %s' % (varNameEncode(pyInstr.argval), pyInstr.argval ) ) )

def STORE_FAST(pyInstr,state):
    # need to modify this to work for lists and tuples
    # need to add variable mapping thing in the state model
    state.lineState.insert(0, 'PUSHVAR %s # %s' % (varNameEncode(pyInstr.argval), pyInstr.argval))
    state.lineState.append('ASSIGN')

def SIMPLE(name):
    return lambda pyInstr,state: state.lineState.append(name)

def COMPARE_OP(pyInstr,state):
    map = { 
        '!=':'NEQ',
        '==': 'EQU',
        '>=':'GTE',
        '<=':'LTE',
        '>':'GT',
        '<':'LT',
    }
    return state.lineState.append( '%s' % map[pyInstr.argval] )

def POP_JUMP_IF_FALSE(pyInstr,state):
    state.addLabel(pyInstr.argval)
    state.lineState.append('BEZ %s' % state.getLabel(pyInstr.argval) ) 

def JUMP_FORWARD(pyInstr,state):
    state.addLabel(pyInstr.argval)
    state.lineState.append('JMP %s' % state.getLabel(pyInstr.argval) )

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
    'JUMP_FORWARD':JUMP_FORWARD,
    #'BINARY_POWER': 
}

class CompilerState:
    def __init__(self):
        self.lineState = []
        self.labelDict = {}
        self.fullStack = []
    def getLabel(self, offset):
        return "LABEL%0.3d" % self.labelDict[offset]
    def addLabel(self, offset):
        if(offset not in self.labelDict):
            self.labelDict[offset] = len(self.labelDict.keys())

def parse(func):
    
    state = CompilerState()
    for instr in dis.Bytecode(func):
        
        # second OR part handles that special case when there is no return argument after a function
        if(instr.starts_line != None or (instr.starts_line == None and instr.argval == None and instr.opname == 'LOAD_CONST')):
            if(instr.is_jump_target):
                label = state.getLabel(instr.offset)
                state.lineState.append("%s:" % label)

            state.fullStack.extend(state.lineState)
            state.lineState = []
        print(instr)

        if(instr.opname in instrMap):
            instrMap[instr.opname](instr, state)


            
        if(instr.opname == 'RETURN_VALUE'):
            #[print(line) for line in state.lineState]
            state.fullStack.extend(state.lineState)
            [print(line) for line in state.fullStack]

