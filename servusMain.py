'''
    TODO:
    - Add the UMINUS token for negative numbers
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

# ------------------------------------------------------------------------------

programToExecute = "servusProgram2.py"

if len(sys.argv) > 1:
    programToExecute = str(sys.argv[1])

testProgram_fileObj = open(programToExecute,'r')
testProgram = testProgram_fileObj.read()

testParser()
printIntermediateCode()
executeIntermediateCode()
servusSymbolTable.displayTable()
# printServusSubroutines()

testProgram_fileObj.close()