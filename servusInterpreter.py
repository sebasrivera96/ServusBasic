from servusYacc import *

# ---------------------------- TYPES OF CUDRUPLES ------------------------------
# For arithmetic and logic expressions:
#   - Type A : CONST + CONST (len = 5)
#   - Type B : CONST + TEMP (len = 5)
#   - Type C : TEMP + CONST (len = 5)
#   - Type D : TEMP + TEMP (len = 5)
#   - Type E : VAR = CONST (len = 4)
#   - Type F : VAR = TEMP (len = 4)
# ------------------------------------------------------------------------------

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
    
def executeArithmetic(instruction):
    typeOfOperation = instruction[-1]
    # print("Type of arithmLogic operation:= ", typeOfOperation)

    if typeOfOperation == 'A':
        newValue = computeValue(instruction[0], instruction[1], instruction[2])
        newType = type(instruction[1]) # or type(instruction[2])
    elif typeOfOperation == 'B':
        newValue = computeValue(instruction[0], instruction[1], instruction[2].value)
        newType = instruction[2].valueType
    elif typeOfOperation == 'C':
        newValue = computeValue(instruction[0], instruction[1].value, instruction[2])
        newType = instruction[1].valueType
    elif typeOfOperation == 'D':
        newValue = computeValue(instruction[0], instruction[1].value, instruction[2].value)
        newType = instruction[1].valueType

    instruction[-2].set(newType, newValue)
    
def executeInstruction(instruction):
    opCode = instruction[0]
    arithmeticOperators = ['+','-','*','/','%']
    # print("OpCode:= ", opCode)

    if opCode in arithmeticOperators:
        executeArithmetic(instruction) 
    elif opCode == "=": # VAL -> variable
        typeOfOperation = instruction[-1]
        symb = servusSymbolTable.get(instruction[2])
        # TODO assign a new data-type to the variable, if it changes

        if typeOfOperation == 'E':
            newValue = instruction[1]
        elif typeOfOperation == 'F':
            newValue = instruction[1].value
            
        symb.val = newValue
    elif opCode == "++": # A + 1 -> A
        symb = servusSymbolTable.get(instruction[2])
        symb.val += 1

    # elif opCode == "<": # A Smaller than B -> stored to a Temp
    # elif opCode == ">": # A Grater than B -> stored to a Temp
    # elif opCode == ">=": # A Greater than or equal B -> stored to a Temp
    # elif opCode == "<=": # A Smaller than or equal B -> stored to a Temp
    # elif opCode == "!=": # A is not equal to B -> stored to a Temp
    # elif opCode == "==": # A is equal to B -> stored to a Temp
    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":
    # elif opCode == "":

def executeIntermediateCode():

    for instruction in intermediateCode:
        if instruction[0] != "end":
            executeInstruction(instruction)
        else:
            print("VIELEN DANK")