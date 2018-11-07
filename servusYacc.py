from servusLex import *
import ply.yacc as yacc
from servusSymbolTable import *
from servusTemp import *
import sys
import os

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
# - gF ==> GOTO on FALSE
# - gT ==> GOTO on TRUE
# - g ==> GOTO INCONDICIONAL
# - end ==> END OF PROGRAM
# ------------------------------------------------------------------------------

# ------------------------ GLOBAL VARIABLES ------------------------------------
servusSymbolTable = SymbolTable() 
newType = ""
newVars = []                        # List used for variable declaration
arithmLogicOut = []
availOfTemps = []                   # This avail will store temporals to execute
                                    #  the intermediate code                 
intermediateCode = []
stJumps = []                        # Stack to save jumps
stOperands = []                     # Stack to save operands in let statement
stForCounters = []                  # Stack to save the for counters
forCounter = 0
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

def getOperandValue(operand):
    global availOfTemps
    if isATemporal(operand):
        availOfTemps.append(operand)
        return operand.value
    else:
        return operand

def translateLetStatement(target=None):
    global servusSymbolTable
    global arithmLogicOut
    global availOfTemps
    global intermediateCode
    global forCounter
    artihmOperators = ('+','-','*','/','%','>','==','<','<=','>=','!=','=','&&','||')
    i = 0

    # print(arithmLogicOut)
    while i >=0 and i < len(arithmLogicOut):
        if arithmLogicOut[i] in artihmOperators:
            currentInstruction = []
            if arithmLogicOut[i] == '=':
                # ['=', valToBeAssigned, var, opCode]
                currentInstruction.append('=')
                currentInstruction.append(arithmLogicOut.pop(0)) # Val to be assigned
                currentInstruction.append(target)
                currentInstruction.append(getOpCode(currentInstruction))
                
                # Force a break from while loop
                arithmLogicOut.pop() 
            else:
                operator, firstOperand, secondOperand = getOperators(i)    
                currentInstruction.append(operator)

                currentInstruction.append(firstOperand)
                currentInstruction.append(secondOperand)

                # TODO validate that both operands are of the same type for arithmetic operations
                # t.valueType = currentType

                # Take a Temp from avail to store the intermediate result
                t = availOfTemps.pop()
                currentInstruction.append(t)
                # Append the OpCode
                currentInstruction.append(getOpCode(currentInstruction))
                arithmLogicOut.insert(i-2,t) 
                i -= 1

                # Return operands to avail if they areTemps
                if(type(firstOperand) == Temp):
                    availOfTemps.append(firstOperand)
                if(type(secondOperand) == Temp):
                    availOfTemps.append(secondOperand)
            intermediateCode.append(currentInstruction)
        else:
            i += 1
    if len(arithmLogicOut) > 0:
        availOfTemps.append(arithmLogicOut.pop())
    
def printTheP(p):
    i = 0
    for tP in p:
        if tP != None:
            print(i, tP)
        i += 1
    print("\nLength ==> ", len(p))

def printIntermediateCode():
    global intermediateCode
    print("\n###################################################################")
    print("###################### INTERMEDIATE CODE ##########################")
    print("###################################################################\n")
    i = 0
    for line in intermediateCode:
        print(i,".\t", line)
        i += 1
    print("\n###################################################################\n")

def fillCuadruple(index, val):
    global intermediateCode
    intermediateCode[index].append(val)

def getCont():
    global intermediateCode
    return len(intermediateCode)

def getResultOfLogicExpression():
    global availOfTemps
    translateLetStatement()
    return availOfTemps.pop()

def returnTempToAvail(t):
    global availOfTemps
    availOfTemps.append(t)

# ------------------------------------------------------------------------------

# Here begins the PARSER
def p_HEAD(p):
    """ HEAD : START checkpointSTART ';' S ENDE ';' """
    global intermediateCode

    endInstruction = ['end']
    intermediateCode.append(endInstruction)

def p_checkpointSTART(p):
    """ checkpointSTART : empty"""
    global intermediateCode

    beginInstruction = ['start']
    intermediateCode.append(beginInstruction)

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

def p_clearScreen(p):
    """ clearScreen : FREI ';' """
    global intermediateCode

    clearScreenInstruction = ['cls']
    intermediateCode.append(clearScreenInstruction)

def p_if(p):
    """
    if : WENN logicExpression checkpoint_if_1 '{' S '}' if_2 checkpoint_if_3
    if_2 : empty
        | SONST checkpoint_if_2 '{' S '}'
    """

def p_checkpoint_if_1(p):
    """
    checkpoint_if_1 : empty
    """
    global intermediateCode
    global stJumps
    currentInstruction = ['gF']

    resultLogicExpression = getResultOfLogicExpression()
    # TODO validate that the result of logic expr. is a boolean
    currentInstruction.append(resultLogicExpression)
    stJumps.append(len(intermediateCode)) # Push to jump stack to fill later
    intermediateCode.append(currentInstruction)
    
    # Return Temp to the avail
    returnTempToAvail(resultLogicExpression)

def p_checkpoint_if_2(p):
    """
    checkpoint_if_2 : empty
    """
    global intermediateCode
    global stJumps
    currentInstruction = ['g']
    intermediateCode.append(currentInstruction)
    cont = len(intermediateCode)
    fillCuadruple(stJumps.pop(), cont)
    stJumps.append(cont-1)

def p_checkpoint_if_3(p):
    """
    checkpoint_if_3 : empty
    """
    global stJumps
    global intermediateCode
    fillCuadruple(stJumps.pop(), len(intermediateCode))

def p_doWhile(p):
    """ doWhile : TUN checkpoint_doWhile_1 '{' S '}' SOLANGE logicExpression checkpoint_doWhile_2 ';' """

def p_checkpoint_doWhile_1(p):
    """ checkpoint_doWhile_1 : empty """
    global stJumps
    cont = getCont()
    stJumps.append(cont)

def p_checkpoint_doWhile_2(p):
    """ checkpoint_doWhile_2 : empty """
    global intermediateCode
    global stJumps
    currentInstruction = ['gT']

    resultLogicExpression = getResultOfLogicExpression()
    # TODO veirfy that resultLogicExpression.valueType == boolean
    dir = stJumps.pop()
    currentInstruction.append(resultLogicExpression)
    currentInstruction.append(dir)
    intermediateCode.append(currentInstruction)

    # Return Temp to the avail
    returnTempToAvail(resultLogicExpression)

def p_while(p):
    """ while : WAEREND checkpoint_while_1 logicExpression checkpoint_while_2 '{' S '}' checkpoint_while_3 """

def p_checkpoint_while_1(p):
    """ checkpoint_while_1 : empty """
    global stJumps
    cont = getCont()
    stJumps.append(cont)

def p_checkpoint_while_2(p):
    """ checkpoint_while_2 : empty """
    global intermediateCode
    global stJumps
    currentInstruction = ['gF']

    resultLogicExpression = getResultOfLogicExpression()
    # TODO veirfy that resultLogicExpression.valueType == boolean
    currentInstruction.append(resultLogicExpression)
    cont = getCont()
    stJumps.append(cont)
    intermediateCode.append(currentInstruction)

    # Return Temp to Avail
    returnTempToAvail(resultLogicExpression)

def p_checkpoint_while_3(p):
    """ checkpoint_while_3 : empty """
    global stJumps
    global intermediateCode
    currentInstruction = ['g']
    dir2 = stJumps.pop()
    dir1 = stJumps.pop()
    
    currentInstruction.append(dir1)
    intermediateCode.append(currentInstruction)

    cont = getCont()
    fillCuadruple(dir2, cont)

def p_for(p):
    """
    for : FUR forAssignation '{' S '}'
    """
    global intermediateCode
    global stJumps
    global stForCounters
    cont = getCont()

    # 1. Fill the GOTO ON FALSE from the beginning of the for loop
    index = stJumps.pop()
    fillCuadruple(index, cont + 2)

    # 2. Increase ID ++
    currentInstruction = ['++', stForCounters.pop()]
    intermediateCode.append(currentInstruction)

    # 3. Create cuadruple of GOTO to logic expression
    currentInstruction2 = ['g', stJumps.pop()]
    intermediateCode.append(currentInstruction2)

    # printTheP(p)

def p_forAssignation(p):
    """
    forAssignation : ID LINKER_PFEIL arithmeticExpression IN forTarget
    forTarget : INTEGER_NUMBER
        | FLOAT_NUMBER
        | ID
    """
    global intermediateCode
    global stJumps
    global availOfTemps
    global stForCounters
    global arithmLogicOut

    # printTheP(p)

    if len(p) > 2:
        # 1. Generate cuadruples of the arithmetic expression and store result in ID
        arithmLogicOut.append('=')
        translateLetStatement(p[1])

        # 2. Generate cuadruple to check ID <= forTarget
        temp = availOfTemps.pop()
        cont = getCont()
        currentInstruction = ['<']
        currentInstruction.append(p[1])     # ID
        currentInstruction.append(p[5])     # forTarget
        currentInstruction.append(temp)     # Temp to store the result
        currentInstruction.append('A')      # Type of operation

        # Push the NEW iterator of the current for LOOP to a Stack
        stForCounters.append(p[1])
        stJumps.append(cont)                # Store address to jump & compare again
        intermediateCode.append(currentInstruction) # ['<=', ID, forTarget, T1]

        # 3. Generate cuadruple GOTO ON FALSE
        cont = getCont()
        currentInstruction2 = []
        currentInstruction2.append('gF')
        currentInstruction2.append(temp)
        intermediateCode.append(currentInstruction2) # ['gF', T1, __]

        stJumps.append(cont) # Store index to fill in later
        returnTempToAvail(temp)
    else:
        p[0] = p[1]
    
def p_let(p):
    """
    let : LASS ID LINKER_PFEIL letAssignation ';'
    letAssignation : arithmeticExpression
        | logicExpression
        | booleanAssignation
    """
    global arithmLogicOut
    global servusSymbolTable
    global stOperands

    if p[1] == "lass":
        actualSymbol = servusSymbolTable.get(p[2])
        stOperands.append(p[2])
        if actualSymbol == None:
            print("Variable ", p[2], " was not declared in this scope.")
            # TODO call an error function
        else:
            arithmLogicOut.append('=')
            translateLetStatement(p[2])

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
    booleanAssignation : logicExpression checkpoint_if_1 '?' arithmeticExpression checkpoint_boolean_1 ':' arithmeticExpression checkpoint_boolean_2
    """
    global stOperands


    # Final Step - Clear the stack of operands 
    while len(stOperands) > 0:
        stOperands.pop()

def p_checkpoint_boolean_1(p):
    """
    checkpoint_boolean_1 : empty
    """
    global intermediateCode
    global stOperands
    global availOfTemps

    newValue = availOfTemps[-1].value
    id = stOperands[-1]
    currenInstruction = ['=', newValue, id]

def p_checkpoint_boolean_2(p):
    """
    checkpoint_boolean_2 : empty
    """

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! ", p)
    sys.exit("Syntax error in input! ", p)

#Initialize the Avail of Temporals
initAvail()
# Build the parser
parser = yacc.yacc()