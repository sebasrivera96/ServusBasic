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
import sys

# ------------------------ GLOBAL VARIABLES ------------------------------------
# servusSymbolTable = SymbolTable() 
# newType = ""
# availOfTemps = []
# newVars = [] # List used for variable declaration
# arithmLogicOut = [] 
# ------------------------------------------------------------------------------

# ----------------------- HELPER FUNCTIONS -------------------------------------


testProgram = """
start;
frei;
dim a1 als float;
lass a1 <- 8.9 + 3 - 2;
wenn (3.5 > 2.0) {
    druck "HOLA MUNDO";
}
sonst{
    druck "FALSE";
}
ende;

"""

def testParser():
    result = parser.parse(testProgram)

testParser()
# servusSymbolTable.displayTable()
printIntermediateCode()