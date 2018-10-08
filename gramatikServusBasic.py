'''
    TODO:
    - How are final IDs for the variables handled?
    - Where do I define logic and arithmetic expressions?
    - How to define the ID of a variable on the lexer side?
'''
import ply.lex as lex
import ply.yacc as yacc
import sys

testProgram = '''
# Este es un programa de prueba
    START
    FREI;
    DIM A1, A2, B1, B2 als float;
    LASS A1 <- 10.0;
    DIM MAT1 als float[100][100];
    DIM MAT2 als float[100][100];
    DIM MAT3 als float[100][100];
    ENDE
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
    'waerend' : 'WAEREND'
}

literals = [
    '+',
    '-',
    '!',
    '@',
    '$',
    '/',
    '&',
    '^',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    '+',
    '=',
    '_',
    '?',
    ';',
    ':',
    ',',
    '<',
    '>',
    '.',
    '|',
    '"',
    '%'
]

tokens = [
    'ID', 
    'LINKER_PFEIL',
    'STRING',
    'FLOAT_NUMBER',
    'INTEGER_NUMBER',
    'QUOTATION_MARK',
    'GrTorE',
    'SmTorE',
    'EQUAL',
    'NOT'
] + list(reserved.values())

def t_COMMENT(t):
    r'\#.*'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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
t_GrTorE = r'\>\='
t_SmTorE = r'\<\='
t_EQUAL = r'\=\='
t_NOT = r'\!\='


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
    '''
    HEAD : START S ENDE
    '''

def p_S(p):
    '''
    S : instruction
        | instruction S
    instruction : print 
        | clearScreen
        | if
        | doWhile
        | for
        | let
        | while
        | DIM declareVariable 
        | EINGABE input ';'
        | DEF ID '{' S RETURN ';' '}'
        | GOSUB ID ';'
    '''

def p_print(p):
    '''
    print : DRUCK ID ';'
        | DRUCK STRING ';'
    '''

def p_clearScreen(p):
    '''
    clearScreen : FREI ';'
    '''

def p_if(p):
    '''
    if : WENN logicExpression '{' S '}' SONST '{' S '}'
        | WENN logicExpression '{' S '}'
    '''

def p_doWhile(p):
    '''
    doWhile : TUN '{' S '}' SOLANGE logicExpression ';'
    '''

def p_for(p):
    '''
    for : FUR ID LINKER_PFEIL forAssignation IN forTarget '{' S '}'
    forAssignation : arithmeticExpression
        | INTEGER_NUMBER
        | FLOAT_NUMBER
    forTarget : INTEGER_NUMBER
        | FLOAT_NUMBER
    '''

def p_let(p):
    '''
    let : ID LINKER_PFEIL letAssignation ';'
    letAssignation : arithmeticExpression
        | logicExpression
        | booleanAssignation
    '''

def p_while(p):
    '''
    while : WAEREND logicExpression '{' S '}'
    '''

def p_declareVariable(p):
    '''
    declareVariable : ID ',' declareVariable
        | ID ALS type
    type : dataTypes '[' INTEGER_NUMBER ']' '[' INTEGER_NUMBER ']' ';'
        | dataTypes '[' INTEGER_NUMBER ']' ';'
        | dataTypes ';'
    dataTypes : WORT
        | FLOAT
    '''

def p_input(p):
    '''
    input : ID ',' input
        | ID ';'
    '''

def p_logicExpression(p):
    '''
    logicExpression : '(' logicOperand logicOperator secondLogicOperand ')'
    secondLogicOperand : logicExpression
        | logicOperand
    logicOperand : ID
        | INTEGER_NUMBER
        | FLOAT_NUMBER
        | STRING
    logicOperator : '>'
        | '<'
        | '&'
        | '|'
        | 'GrTorE'
        | 'SmTorE'
        | 'EQUAL'
        | 'NOT'
        | 'UND'
        | 'ODER'
    '''

def p_arithmeticExpression(p):
    '''
    arithmeticExpression : '(' arithOperand arithOperator secondArithOperand ')'
        | arithOperand
    secondArithOperand : arithmeticExpression
        | arithOperand
    arithOperand : ID
        | INTEGER_NUMBER
        | FLOAT_NUMBER
    arithOperator : '+'
        | '-'
        | '*'
        | '/'
        | '%'
    '''

def p_booleanAssignation(p):
    '''
    booleanAssignation : logicExpression '?' arithmeticExpression ':' arithmeticExpression
    '''

# Build the parser
parser = yacc.yacc()