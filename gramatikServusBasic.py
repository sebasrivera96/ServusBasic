'''
    TODO:
    - Add the UMINUS token for negative numbers
    - Let all the lexical analysis be done on the servusLex.py file
'''
import ply.lex as lex
import ply.yacc as yacc
from symbolTable import *
import sys

servusSymbolTable = SymbolTable() 

testProgram = ''' 
start;
frei;

dim A1, A2, B1, B2 als float;
dim MAT1[100][100] als float;
dim MAT2[100][100] als float;
dim MAT3[100][100] als float;
dim A2, A3[10] als wort;

ende;
'''

reserved = {
    'start' : 'START', 
    'ende' : 'ENDE',
    'frei' : 'FREI',
    'wenn' : 'WENN', 
    'sonst' : 'SONST', 
    'tun' : 'TUN', 
    'gosub' : 'GOSUB', 
    'dim' : 'DIM',
    'eingabe' : 'EINGABE', 
    'als' : 'ALS', 
    'fur' : 'FUR', 
    'in' : 'IN',
    'return' : 'RETURN', 
    'def' : 'DEF',
    'wort' : 'WORT',
    'float' : 'FLOAT',
    'und' : 'UND',
    'oder' : 'ODER',
    'druck' : 'DRUCK',
    'solange' : 'SOLANGE',
    'waerend' : 'WAEREND',
    'lass' : 'LASS'
}

literals = "+!@$/&*^()[]{}+=_?;:,<>.|%"

tokens = [
    'ID', 
    'LINKER_PFEIL',
    'STRING',
    'FLOAT_NUMBER',
    'INTEGER_NUMBER',
    'GtE',
    'StE',
    'EQUAL',
    'NOT',
    'COMMENT',
    'QUOTATION_MARK'
    # 'UMINUS'
] + list(reserved.values())

def t_COMMENT(t):
    r'\#.*'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_\d\[\]]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"[a-z A-Z_\d]+\"'
    t.value = str(t.value)
    return t

t_LINKER_PFEIL = r'\<\-'
t_GtE = r'\>\='
t_StE = r'\<\='
t_EQUAL = r'\=\='
t_NOT = r'\!\='
t_QUOTATION_MARK = r'\"'
# t_UMINUS = r'\-'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def testLexer():
    lexer.input(testProgram)
    for tok in lexer:
        print(tok)

# testLexer()

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

newType = ""
newVars = []
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
    # TODO insert new variable to servusSymbolTable
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
    # print(result)

testParser()
servusSymbolTable.displayTable()