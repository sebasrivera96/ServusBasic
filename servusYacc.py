from servusLex import *
import ply.yacc as yacc
from servusSymbolTable import *
from servusTemp import *

# ---------------------------- TYPES OF CUDRUPLES ------------------------------
# For arithmetic and logic expressions:
#   - Type A : CONST + CONST (len = 5)
#   - Type B : CONST + TEMP (len = 5)
#   - Type C : TEMP + CONST (len = 5)
#   - Type D : TEMP + TEMP (len = 5)
#   - Type E : VAR = CONST (len = 4)
#   - Type F : VAR = TEMP (len = 4)
# ------------------------------------------------------------------------------

# --------------------------- TYPES OF OPCODES ---------------------------------
# - p ==> PRINT
# - gF ==> GOTO FALSE
# ------------------------------------------------------------------------------

# ------------------------ GLOBAL VARIABLES ------------------------------------
servusSymbolTable = SymbolTable() 
newType = ""
newVars = []                        # List used for variable declaration
arithmLogicOut = []
# This avail will store temporals to execute the intermediate code
availOfTemps = []
intermediateCode = []
stJumps = []                        # Stack to save jumps
# ------------------------------------------------------------------------------

# ------------------------ HELPER FUNCTIONS ------------------------------------
"""
    LIST OF INTERMEDIATE CODE INSTRUCTIONS:
    operator operand1 operand2 temporalStoreVariable
    TODO:
    - Translate the if instruction
    - when currenInstruction is complete, add to the intermediate code
    - create the assign instruction
"""
def initAvail(n=15):
    global availOfTemps
    for i in range(n):
        t = Temp(int, 0)
        availOfTemps.append(t)

def isATemporal(v):
    return type(v) == Temp

def getOperators(i):
    global arithmLogicOut
    operator = arithmLogicOut.pop(i)
    firstOperand = arithmLogicOut.pop(i-2)
    secondOperand = arithmLogicOut.pop(i-2) 
    return operator, firstOperand, secondOperand        

def getOpCode(l):
    if len(l) == 4:
        op1 = l[1]
        op2 = l[2]
        # Type A
        if not isATemporal(op1) and not isATemporal(op2):
            return 'A'
        # Type B
        elif not isATemporal(op1) and isATemporal(op2):
            return 'B'
        # Type C
        elif isATemporal(op1) and not isATemporal(op2):
            return 'C'
        # Type D
        elif isATemporal(op1) and isATemporal(op2):
            return 'D'
    elif len(l) == 3:
        # Type E
        if not isATemporal(l[1]):
            return 'E'
        # Type F
        elif isATemporal(l[1]):
            return 'F'

def translateLetStatement(target):
    global servusSymbolTable
    global arithmLogicOut
    global availOfTemps
    currentInstruction = []
    artihmOperators = ('+','-','*','/','%','>','==','<','<=','>=','!=')
    i = 0
    while len(arithmLogicOut) > 1:
        if arithmLogicOut[i] in artihmOperators:
            operator, firstOperand, secondOperand = getOperators(i)    
            currentInstruction.append(operator)
            # Check if the operands are temporals of the avail
            if isATemporal(firstOperand):
                currentInstruction.append(firstOperand.value)
                availOfTemps.append(firstOperand)
                currentType = firstOperand.valueType
            else:
                currentInstruction.append(firstOperand)
                currentType = type(firstOperand)
            if isATemporal(secondOperand):
                currentInstruction.append(secondOperand.value)
                availOfTemps.append(secondOperand)
            else:
                currentInstruction.append(secondOperand)
            # TODO validate that both operands are of the same value for arithmetic operations
            t = availOfTemps.pop()
            t.valueType = currentType
            currentInstruction.append(t)
            # Append the OpCode
            currentInstruction.append(getOpCode(currentInstruction))
            print(currentInstruction)
            # TODO Code to execute the instruction 
            currentInstruction.clear()
            # print("Size of the avail: ", len(availOfTemps))
            arithmLogicOut.insert(i-2,t) 
            i -= 1
        else:
            i += 1
    currentInstruction.append('=')
    currentInstruction.append(arithmLogicOut[0])
    currentInstruction.append(target)
    currentInstruction.append(getOpCode(currentInstruction))

    print(currentInstruction)
    arithmLogicOut.clear()
    # When the while loop finishes, the only missing instruction is the assignation

def printTheP(p):
    i = 0
    for tP in p:
        if tP != None:
            print(i, tP)
        i += 1

# def translateIfStatement():
def printIntermediateCode():
    global intermediateCode
    print("##################################################################")
    print("###################### INTERMEDIATE CODE #########################")
    print("##################################################################")
    i = 0
    for line in intermediateCode:
        print(i,".\t", line)
        i += 1
    print("##################################################################")
# ------------------------------------------------------------------------------

# Here begins the PARSER
def p_HEAD(p):
    """ HEAD : START ';' S ENDE ';' """

def p_S(p):
    """
    S : instruction S
        | empty

    instruction : print 
        | clearScreen
        | if
        | doWhile
        | for
        | let
        | while
        | DIM declareVariable 
        | EINGABE input ';'
        | DEF ID '{' S RETURN '}'
        | GOSUB ID ';'
    """
    printTheP(p)

def p_empty(p):
    'empty :'
    pass

def p_print(p):
    """
    print : DRUCK ID ';'
        | DRUCK STRING ';'
    """
    global intermediateCode
    currenInstruction = ['p'] 
    currenInstruction.append(p[2])
    intermediateCode.append(currenInstruction)
    printTheP(p)

def p_clearScreen(p):
    """ clearScreen : FREI ';' """

def p_if(p):
    """
    if : WENN logicExpression '{' S '}' 
        | WENN logicExpression '{' S '}' SONST '{' S '}'
    """
    global intermediateCode
    global availOfTemps
    global stJumps
    # p[0] = p[1]
    # if p[2]:
    #     p[0] = p[4]
    # else:
    #     if p[6] != None:
    #         p[0] = p[8]
    currentInstruction = ['gF']
    currentInstruction.append(availOfTemps.pop())
    intermediateCode.append(currentInstruction)
    stJumps.append(len(intermediateCode) - 1) # Push the address to complete it later
    printTheP(p)

# def p_if_2(p):


def p_doWhile(p):
    """ doWhile : TUN '{' S '}' SOLANGE logicExpression ';' """

def p_for(p):
    """
    for : FUR ID LINKER_PFEIL forAssignation IN forTarget '{' S '}'
    forAssignation : arithmeticExpression
        | INTEGER_NUMBER
        | FLOAT_NUMBER
    forTarget : INTEGER_NUMBER
        | FLOAT_NUMBER
        | ID
    """

def p_let(p):
    """
    let : LASS ID LINKER_PFEIL letAssignation ';'
    letAssignation : arithmeticExpression
        | logicExpression
        | booleanAssignation
    """
    global arithmLogicOut
    global servusSymbolTable
    if p[1] == "lass":
        actualSymbol = servusSymbolTable.get(p[2])
        if actualSymbol == None:
            print("Variable ", p[2], " was not declared in this scope.")
            # TODO call an error function
        else:
            # print(arithmLogicOut)
            translateLetStatement(p[2])

def p_while(p):
    """ while : WAEREND logicExpression '{' S '}' """

def p_declareVariable(p):
    """
    declareVariable : ID declareVariable1 ALS type ';'
    declareVariable1 : ',' ID declareVariable1
        | empty
    type : WORT
        | FLOAT
    """
    global newType
    global newVars
    for l in p:
        if l != None and l != ',':
            if l == ';':
                if len(newVars) > 0 and newType != "":
                    servusSymbolTable.addElements(newVars, newType)
                    newVars.clear()
                    newType = ""
            elif l == "float" or l == "wort":
                newType = l
            elif l not in reserved:
                newVars.append(l)

def p_input(p):
    """
    input : ID input1
    input1 : ',' ID
        | empty
    """

precedence = (
    # LOWEST PRIORITY
    ('left', '+', '-'),
    ('left', 'GtE', 'StE', 'EQUAL'),
    ('left', 'UND', 'ODER', 'NOT'),
    ('left', '*', '/', '%'),    
    # ('right', 'UMINUS'),
    # HIGHEST PRIORITY
)

def p_logicExpression(p):
    """
    logicExpression : logicExpression ODER logicExpressionAND
        | logicExpressionAND
    logicExpressionAND : logicExpressionAND UND logicExpressionNOT
        | logicExpressionNOT
    logicExpressionNOT : logicExpressionNOT NOT logicExpressionGtE
        | logicExpressionGtE
    logicExpressionGtE : logicExpressionGtE GtE logicExpressionStE
        | logicExpressionStE
    logicExpressionStE : logicExpressionStE StE logicExpressionSmaller
        | logicExpressionSmaller
    logicExpressionSmaller : logicExpressionSmaller '<' logicExpressionGreater
        | logicExpressionGreater
    logicExpressionGreater : logicExpressionGreater '>' logicExpressionEq
        | logicExpressionEq
    logicExpressionEq : logicExpressionEq EQUAL operand
        | '(' logicExpression ')'
        | operand
    operand : ID
        | INTEGER_NUMBER
        | FLOAT_NUMBER
        | STRING
    """
    global arithmLogicOut
    global servusSymbolTable
    invalidElements = (None, '(', ')')
    for element in p:
        if element not in invalidElements:
            arithmLogicOut.append(element)

def p_arithmeticExpression(p):
    """
    arithmeticExpression : arithmeticExpression '+' subs
        | subs
    subs : subs '-' mul
        | mul
    mul : mul '*' mod
        | mod
    mod : mod '%' divi
        | divi
    divi : divi '/' arithOperand
        | '(' arithmeticExpression ')'
        | arithOperand
    arithOperand : ID
        | INTEGER_NUMBER
        | FLOAT_NUMBER
    """
    global arithmLogicOut
    global servusSymbolTable
    invalidElements = (None, '(', ')')
    for element in p:
        if element not in invalidElements:
            arithmLogicOut.append(element)

def p_booleanAssignation(p):
    """
    booleanAssignation : logicExpression '?' arithmeticExpression ':' arithmeticExpression
    """

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! ", p)

#Initialize the Avail of Temporals
initAvail()
# Build the parser
parser = yacc.yacc()