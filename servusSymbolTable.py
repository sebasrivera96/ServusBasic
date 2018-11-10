'''
    Symbol Table of the ServusBasic Programming Language
    Author: Sebastian Rivera Gonzalez
    Date: 08/OCT/2018
'''
class Symbol:
    def __init__(self, name, type=float, r=1, c=1):
        self.val = 0.0
        self.name = name
        self.type = type
        self.rows = r
        self.cols = c

        # TODO Add one or to lists to store all the elements of the array or matrix
        if(type == str):
            self.val = ""
        elif(type == float):
            self.val = 0.0

        if r > 1:
           tVal = self.val
           self.val = []
           for i in range(self.rows):
               self.val.append(tVal)
        
        if c > 1:
           tVal = self.val
           self.val = []
           for i in range(self.cols):
               self.val.append(tVal)

    def printSymbol(self):
        print(self.name, "\t", self.type, "\t", self.rows, "\t", self.cols, "\t", self.val)

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def stripVar(self, s):
        # TODO Reise error if an element of more than two dimensions is declared
        name = ""
        row = 1
        str_row = ""
        col = 1
        str_col = ""
        index = 0
        state = 0
        # 3 states - 0 := name, 1 := row, 2 := col; change concatenation target

        while index < len(s):
            tC = s[index]
            index += 1

            if tC == '[':
                state += 1
            elif tC == ']':
                pass
            else:
                if state == 0:
                    name += tC
                elif state == 1:
                    str_row += tC
                elif state == 2:
                    str_col += tC
        
        if str_row != "":
            try:
                # Variable declaration
                row = int(str_row)
            except: 
                # Assign a new value
                row = str_row
            
        if str_col != "":
            try:
                col = int(str_col)
            except:
                col = str_col

        # print(name, type(row), type(col))
        return name, row, col

    # TODO What happens if var already exists ??? Right now it will be ignored
    def addElements(self, varList, ty):
        if(ty == "wort"):
            ty = str
        for elem in varList:
            newName, newRow, newCol = self.stripVar(elem)
            if newName not in self.symbols:
                newVar = Symbol(newName, ty, newRow, newCol)
                self.symbols[newName] = newVar

    def getValue(self, varName):
        tSymbol = self.symbols.get(varName)
        if tSymbol != None:
            return tSymbol.val
        else:
            return None

    def get(self, varName):
        tName, tRows, tCols = self.stripVar(varName)
        if self.symbols.__contains__(tName):
            return self.symbols[tName]
        else:
            return None

    def displayTable(self):
        print("\n###################################################################")
        print("####################### TABLE OF SYMBOLS ##########################")
        print("###################################################################\n")
        print("Name\tType\tRows\tCols\tValue")
        for key, val in self.symbols.items():
            val.printSymbol()
        print("\n###################################################################\n")
        