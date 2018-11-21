from servusYacc import *
from servusSymbolTable import *
import sys
import os

# sys.exit("ERROR")

# ---------------------------- TYPES OF CUDRUPLES ------------------------------
# For arithmetic and logic expressions:
#   - Type A : CONST + CONST (len = 5)
#   - Type B : CONST + TEMP (len = 5)
#   - Type C : TEMP + CONST (len = 5)
#   - Type D : TEMP + TEMP (len = 5)
#   - Type E : VAR = CONST (len = 4)
#   - Type F : VAR = TEMP (len = 4)
# ------------------------------------------------------------------------------

# ---------------------------- GLOBAL VARIABLES --------------------------------
instructionIndex = 0
# ------------------------------------------------------------------------------

def cleanOpernd(operand):
    numeric = [int, float]

    if type(operand) in numeric:
        return operand
    else:
        tVal = servusSymbolTable.getValue(operand)
        return float(tVal)

def computeValue(op, n1, n2):

    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        return n1 / n2
    elif op == '%':
        return n1 % n2
    elif op == '<':
        return n1 < n2
    elif op == '<=':
        return n1 <= n2
    elif op == '>':
        return n1 > n2
    elif op == '>=':
        return n1 >= n2
    elif op == '||':
        if type(n1) != bool or type(n2) != bool:
            sys.exit("Invalid data type for logic comparison")

        return n1 or n2
    elif op == '&&':
        if type(n1) != bool or type(n2) != bool:
            sys.exit("Invalid data type for logic comparison")

        return n1 and n2
    elif op == '!=':
        return n1 != n2
    elif op == '==':
        return n1 == n2
    
def executeArithmetic(instruction):
    typeOfOperation = instruction[-1]
    # print("Type of arithmLogic operation:= ", typeOfOperation)

    if typeOfOperation == 'A':
        operand1 = instruction[1]
        operand2 = instruction[2]

        # Befor start, clean both operands (a.k.a. get the valu of the variable)
        operand1 = cleanOpernd(operand1)
        operand2 = cleanOpernd(operand2)

        newValue = computeValue(instruction[0], operand1, operand2)
        newType = type(instruction[1]) # or type(instruction[2])

    elif typeOfOperation == 'B':
        operand1 = instruction[1]
        operand2 = instruction[2]
        # Befor start, clean 1st operand (a.k.a. get the valu of the variable)
        operand1 = cleanOpernd(operand1)

        newValue = computeValue(instruction[0], operand1, operand2.value)
        newType = instruction[2].valueType

    elif typeOfOperation == 'C':
        operand1 = instruction[1]
        operand2 = instruction[2]
        # Befor start, clean 2nd operand (a.k.a. get the valu of the variable)
        operand2 = cleanOpernd(operand2)

        newValue = computeValue(instruction[0], operand1.value, operand2)
        newType = instruction[1].valueType

    elif typeOfOperation == 'D':
        operand1 = instruction[1]
        operand2 = instruction[2]
        newValue = computeValue(instruction[0], operand1.value, operand2.value)
        newType = instruction[1].valueType

    instruction[-2].set(newType, newValue)

def executeLogic(instruction):
    typeOfOperation = instruction[-1]
    newType = bool

    if typeOfOperation == 'A':
        # print(instruction)
        operand1 = instruction[1]
        operand2 = instruction[2]

        # Befor start, clean both operands (a.k.a. get the valu of the variable)
        operand1 = cleanOpernd(operand1)
        operand2 = cleanOpernd(operand2)

        newValue = computeValue(instruction[0], operand1, operand2)

    elif typeOfOperation == 'B':
        operand1 = instruction[1]
        operand2 = instruction[2]
        # Befor start, clean 1st operand (a.k.a. get the valu of the variable)
        operand1 = cleanOpernd(operand1)

        newValue = computeValue(instruction[0], operand1, operand2.value)

    elif typeOfOperation == 'C':
        operand1 = instruction[1]
        operand2 = instruction[2]
        # Befor start, clean 2nd operand (a.k.a. get the valu of the variable)
        operand2 = cleanOpernd(operand2)

        newValue = computeValue(instruction[0], operand1.value, operand2)

    elif typeOfOperation == 'D':
        operand1 = instruction[1]
        operand2 = instruction[2]
        newValue = computeValue(instruction[0], operand1.value, operand2.value)

    instruction[-2].set(newType, newValue)

def modifyInstructionIndex(val):
    global instructionIndex
    instructionIndex = val

def executeInstruction(instruction):
    global instructionIndex
    opCode = instruction[0]
    arithmeticOperators = ['+','-','*','/','%']
    logicOperators = ['<','>','<=','>=','!=','==','&&','||']
    # print("OpCode:= ", opCode)

    if opCode in arithmeticOperators:
        executeArithmetic(instruction) 

    elif opCode == "=": # VAL -> variable
        typeOfOperation = instruction[-1]
        # symb = servusSymbolTable.get(instruction[2])
        symbolToBeAssigned = instruction[2]
        # TODO assign a new data-type to the variable, if it changes

        if typeOfOperation == 'E':
            newValue = servusSymbolTable.getValue(instruction[1])
        elif typeOfOperation == 'F':
            newValue = instruction[1].value
        
        # symb.val = newValue
        servusSymbolTable.setValue(symbolToBeAssigned, newValue)

    elif opCode == "++": # A + 1 -> A
        symb = servusSymbolTable.getSymbolFromTable(instruction[1])
        symb.val += 1

    elif opCode in logicOperators:
        executeLogic(instruction)

    elif opCode == "p":
        # tVal = servusSymbolTable.getValue(instruction[1])
        tSymbol = servusSymbolTable.getSymbolFromTable(instruction[1])
        
        if tSymbol != None:
            # print(instruction[1], '= ', tVal)
            tSymbol.printValue()
        else:
            print(instruction[1][1:-1]) # Remove "" with [1:-1]
        print("")

    elif opCode == "gF":
        if not instruction[1].value:
            jumpInstr = instruction[-1]
            instructionIndex = jumpInstr

    elif opCode == "g":
        jumpInstr = instruction[-1]
        instructionIndex = jumpInstr

    elif opCode == "gT":
        if instruction[1].value:
            jumpInstr = instruction[-1]
            instructionIndex = jumpInstr

    elif opCode == "cls":
        os.system('cls')

    elif opCode == "inp":
        newValue = input("")
        symbolToBeAssigned = instruction[1]
        servusSymbolTable.setValue(symbolToBeAssigned, newValue)

    elif opCode == "return":
        global stReturn
        modifyInstructionIndex(stReturn.pop())
    
    elif opCode == "gSub":
        # Store the index of return in stack stReturn 
        returnIndex = instruction[-1]
        appendReturnIndex(returnIndex)
        # Move to first cuadruple of the subroutine
        modifyInstructionIndex(instruction[1])

    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":

def printBeginOfProgram():
    # os.system('cls')

    print("\n###################################################################")
    print("##################### ANFANG DES PROGRAMMS ########################")
    print("###################################################################\n")

def printEndOfProgram():
    print("\n###################### ENDE DES PROGRAMMS #########################\n")

def executeIntermediateCode():
    global instructionIndex
    global servusSubroutines

    while instructionIndex < len(intermediateCode):
        instruction = intermediateCode[instructionIndex]
        instructionIndex += 1
        if instruction[0] == "start":
            printBeginOfProgram()
            # instructionIndex = servusSubroutines.get("main")
        elif instruction[0] == "end":
            printEndOfProgram()
        else:
            # print("Cuad: ", instructionIndex)
            executeInstruction(instruction)
        # print(instructionIndex)
        