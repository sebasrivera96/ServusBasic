'''
AUTHOR: Sebastian Rivera Gonzalez
ID: A01280882
DATE: 13/09/2018
FILE NAME: holaQueTal.py
COURSE: Lenguajes y Traductores
LANGUAGE: Python3
'''
import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = (
    'HOLA',
    'COMA',
    'QUE',
    'TAL', 
    'ERROR'
)

t_COMA = r','

def t_WORD(t):
    r'[a-zA-Z_\d]+'
    if(t.value == 'hola'):
        t.type = 'HOLA'
    elif(t.value == 'que'):
        t.type = 'QUE'
    elif(t.value == 'tal'):
        t.type = 'TAL'
    else:
        t.type = 'ERROR'
    return t

def t_error(t):
    t.lexer.skip(1)

t_ignore = r' '

lexer = lex.lex()

def p_S(p):
    '''
    S : X QUE TAL
    '''
    print("\nGreat Job!\n")

def p_X(p):
    '''
    X : X COMA HOLA
      | HOLA
    '''
    p[0] = p[1]

def p_error(p):
    '''
    error : ERROR
    '''
    print("\nSyntax error!\n")

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None

parser = yacc.yacc()

while True:
    s = input('\nWrite a phrase: ')
    parser.parse(s)