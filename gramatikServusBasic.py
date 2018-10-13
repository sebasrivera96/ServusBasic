'''
    TODO:
    - Add the UMINUS token for negative numbers
    - Let all the lexical analysis be done on the servusLex.py file
'''
import ply.yacc as yacc
from symbolTable import *
from servusLex import *
import sys

# ------------------------ GLOBAL VARIABLES ------------------------------------
servusSymbolTable = SymbolTable() 
newType = ""
newVars = []
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

def p_booleanAssignation(p):
    """
    booleanAssignation : logicExpression '?' arithmeticExpression ':' arithmeticExpression
    """

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! ", p)

# Build the parser
parser = yacc.yacc()

def testParser():
    result = parser.parse(testProgram)

testParser()
servusSymbolTable.displayTable()