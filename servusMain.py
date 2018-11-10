'''
    TODO:
    - Add the UMINUS token for negative numbers
    - Where should the intermediate code should be stored?
    - How should the intermediate code be constructed?
'''
# from symbolTable import *
from servusLex import *
from servusYacc import *
from collections import deque
from servusInterpreter import *
import sys

# ------------------------ GLOBAL VARIABLES ------------------------------------
# servusSymbolTable = SymbolTable() 
# newType = ""
# availOfTemps = []
# newVars = [] # List used for variable declaration
# arithmLogicOut = [] 
# ------------------------------------------------------------------------------

# ----------------------- HELPER FUNCTIONS -------------------------------------

def testParser():
    result = parser.parse(testProgram)


testProgram_fileObj = open("servusProgram2.txt",'r')
testProgram = testProgram_fileObj.read()

testParser()
printIntermediateCode()
executeIntermediateCode()
servusSymbolTable.displayTable()