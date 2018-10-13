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
        if(type == str):
            self.val = ""
        elif(type == float):
            self.val = 0.0
        self.rows = r
        self.cols = c

    def printSymbol(self):
        print(self.name, "\t", self.type, "\t", self.rows, "\t", self.cols, "\t", self.val)

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def stripNewVar(self, s):
        name = ""
        row = 1
        col = 1
        if(s.find('[') == -1):
            # Normal variable is being defined
            name = s
        else:
            tList = s.split('[')
            name = tList[0]
            # 1-D array size
            row = int(tList[1][:-1])
            if len(tList) == 3:
                # 2-D array size
                col = int(tList[2][:-1])
        return name, row, col

    # TODO What happens if var already exists ??? Right now it will be ignored
    def addElements(self, varList, ty):
        if(ty == "wort"):
            ty = str
        for elem in varList:
            newName, newRow, newCol = self.stripNewVar(elem)
            if newName not in self.symbols:
                newVar = Symbol(newName, ty, newRow, newCol)
                self.symbols[newName] = newVar



    def get(self, varName):
        if self.symbols.__contains__(varName):
            return self.symbols[varName]
        else:
            return None

    def displayTable(self):
        print("Name\tType\tRows\tCols\tValue")
        for key, val in self.symbols.items():
            val.printSymbol()