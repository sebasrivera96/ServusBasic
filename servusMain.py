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
dim f1, f2, f3 als float;
# lass f1 <- 8.9 + 3 - 2;
# lass f2 <- 3.4;
# lass f3 <- 10 % 5 * (9+ 54);
tun{
    druck "This is a doWhile";
    lass f2  <- f2 - 1;
}solange (f2 == f3);
ende;

"""

def testParser():
    result = parser.parse(testProgram)

testParser()
# servusSymbolTable.displayTable()
printIntermediateCode()