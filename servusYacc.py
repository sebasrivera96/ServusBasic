from servusLex import *
import ply.yacc as yacc
from servusSymbolTable import *
from servusTemp import *

# ------------------------ GLOBAL VARIABLES ------------------------------------
servusSymbolTable = SymbolTable() 
newType = ""
newVars = [] # List used for variable declaration
arithmLogicOut = []
# This avail will store temporals to execute the intermediate code
availOfTemps = []
# ------------------------------------------------------------------------------

# ------------------------ HELPER FUNCTIONS ------------------------------------
"""
    LIST OF INTERMEDIATE CODE INSTRUCTIONS:
    operator operand1 operand2 storeVariable
    TODO:
    - add more fileds to handle special cases.
    - use temporals for intermediate operations
    - when currenInstruction is complete, add to the intermediate code
    - identify if element is a constant or a variable
    - create the assign instruction
"""
def initAvail(n=15):
    global availOfTemps
    for i in range(n):
        t = Temp(int, 0)
        availOfTemps.append(t)

def getOperators(i):
    global arithmLogicOut
    operator = arithmLogicOut.pop(i)
    firstOperand = arithmLogicOut.pop(i-2)
    secondOperand = arithmLogicOut.pop(i-2) 
    return operator, firstOperand, secondOperand        

def translateLetStatement(target):
    global servusSymbolTable
    global arithmLogicOut
    global availOfTemps
    currentInstruction = []
    artihmOperators = ('+','-','*','/','%')
    i = 0
    if len(arithmLogicOut) == 1:
        print("ONLY ASSIGN INSTRUCTION")
        arithmLogicOut.clear()
    while len(arithmLogicOut) > 1:
        if arithmLogicOut[i] in artihmOperators:
            operator, firstOperand, secondOperand = getOperators(i)    
            currentInstruction.append(operator)
            # Check if the operands are temporals of the avail
            if type(firstOperand) == Temp:
                currentInstruction.append(firstOperand.value)
                availOfTemps.append(firstOperand)
                currentType = firstOperand.valueType
            else:
                currentInstruction.append(firstOperand)
                currentType = type(firstOperand)
            if type(secondOperand) == Temp:
                currentInstruction.append(secondOperand.value)
                availOfTemps.append(secondOperand)
            else:
                currentInstruction.append(secondOperand)
            # TODO validate that both operands are of the same value for arithmetic operations
            t = availOfTemps.pop()
            t.valueType = currentType
            currentInstruction.append(t)
            print(currentInstruction)
            # TODO Code to execute the instruction 
            currentInstruction.clear()
            print("Size of the avail: ", len(availOfTemps))
            arithmLogicOut.insert(i-2,t) 
            i -= 1
        else:
            i += 1

    # When the while loop finishes, the only missing instruction is the assignation


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

def p_empty(p):
    'empty :'
    pass

def p_print(p):
    """
    print : DRUCK ID ';'
        | DRUCK STRING ';'
    """

def p_clearScreen(p):
    """ clearScreen : FREI ';' """

def p_if(p):
    """
    if : WENN logicExpression '{' S '}' SONST '{' S '}'
        | WENN logicExpression '{' S '}'
    """

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
    logicExpressionStE : logicExpressionStE StE logicExpressionEq
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