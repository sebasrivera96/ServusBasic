from servusLex import *
import ply.yacc as yacc
from symbolTable import *


# ------------------------ GLOBAL VARIABLES ------------------------------------
servusSymbolTable = SymbolTable() 
newType = ""
newVars = [] # List used for variable declaration
arithmLogicOut = []
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
def translateLetStatement(target):
    global servusSymbolTable
    global arithmLogicOut
    currentInstruction = []
    artihmOperators = ('+','-','*','/','%')
    i = 0
    if len(arithmLogicOut) == 1:
        print("ONLY ASSIGN INSTRUCTION")
        arithmLogicOut.clear()
    while len(arithmLogicOut) > 1:
        if arithmLogicOut[i] in artihmOperators:
            currentInstruction.append(arithmLogicOut.pop(i))
            currentInstruction.append(arithmLogicOut.pop(i-2))
            currentInstruction.append(arithmLogicOut.pop(i-2))
            # currentInstruction.append(top of the avail)
            currentInstruction.append("temp")
            print(currentInstruction)
            currentInstruction.clear()
            arithmLogicOut.insert(i-2,"temp")
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

# Build the parser
parser = yacc.yacc()