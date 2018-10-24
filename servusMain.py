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
dim a1,a2 als float;
lass a1 <- 3.0;
lass a2 <- 7 + 5 * 8 + 3 * 7 - 10 * (3 + 4);
ende;

"""

def testParser():
    result = parser.parse(testProgram)

testParser()
servusSymbolTable.displayTable()