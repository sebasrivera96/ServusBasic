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


testProgram = """
start;
# frei;
dim f1, f2, f3, i als float;
lass f1 <- 8.9 + 3 - 2;
lass f2 <- 0;
lass f3 <- 3 + 2;
lass i <- 0;
# lass i <- (f3 > f2) ? 0 : f2;

wenn (f2 == 0) && f3 > 0 {
    druck "IF TRUE";
}
sonst {
    druck "IF FALSE";
}

waerend (f2 <= f3){
    druck f2;
    lass f2  <- f2 + 1;
}

druck "dowhile loop";
tun{
    lass f3 <- f3 + 3;
    druck f3;
} solange (f3 < 30);

druck "This is a for loop";
fur i <- 5 in 8{
    druck i;
}
ende;
"""

def testParser():
    result = parser.parse(testProgram)

testParser()
printIntermediateCode()
executeIntermediateCode()
servusSymbolTable.displayTable()