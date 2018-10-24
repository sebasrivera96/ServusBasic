import ply.lex as lex

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

literals = "+-!@$/&*^()[]{}+=_?;:,<>.|%"

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

def testLexer():
    lexer.input(testProgram)
    for tok in lexer:
        print(tok)

# Build the lexer
lexer = lex.lex()
