'''
    Symbol Table of the ServusBasic Programming Language
    Author: Sebastian Rivera Gonzalez
    Date: 08/OCT/2018
'''
import sys

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
               self.val.append(tVal.copy())

    def printSymbol(self):
        print(self.name, "\t", self.type, "\t", self.rows, "\t", self.cols, "\t", self.val)

    # TODO Reise error when trying to set a value outside of the valid range, i.e. i or j >= rows or cols
    def setValue(self, val, i=1, j=1):
        # numeric = {int, float}
        # Retrieve the real value of val if necessary, i.e. val not in numeric
        # if type(val) not in numeric:
        #     val = val.getValue()

        # Three cases for setting the value:
        # Normal variable
        if self.rows == 1 and self.cols == 1:
            self.val = val
        else:
            # Reise error if i or j are out of range
            if i < 0 or i >= self.rows or j < 0 or j >= self.rows:
                sys.exit("Reference out of range when indexing! i=%d, j=%d" % (i,j))

            # 1D array
            if self.rows > 1 and self.cols == 1:
                self.val[i] = val
            # 2D matrix
            elif self.rows > 1 and self.cols > 1:
                self.val[i][j] = val

    # TODO Same as the one from the function above
    def getValue(self, i=1, j=1):
        # Three cases for getting the value:
        # Normal variable
        if self.rows == 1 and self.cols == 1:
            return self.val
        else:
            # Reise error if i or j are out of range
            if i < 0 or i >= self.rows or j < 0 or j >= self.rows:
                sys.exit("Reference out of range when indexing! i=%d, j=%d" % (i,j))

            # 1D array
            if self.rows > 1 and self.cols == 1:
                return self.val[i]
            # 2D matrix
            elif self.rows > 1 and self.cols > 1:
                return self.val[i][j]

class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def stripVar(self, s):
        """
        RETURN VALUES:
        - Normal variable: name(of the variable), 1, 1
        - 1D Array: name, string(index) | # of rows, 1
        - 2D Matrix: name, string(index) | # of rows, string(index) | # of cols
        """
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

    def addElements(self, varList, tType):
        if(tType == "wort"):
            tType = str
        for elem in varList:
            newName, newRow, newCol = self.stripVar(elem)
            if newName not in self.symbols:
                newVar = Symbol(newName, tType, newRow, newCol)
                self.symbols[newName] = newVar

    def getSymbolFromTable(self, varName):
        tName, tRows, tCols = self.stripVar(varName)
        # print(tName)
        if self.symbols.__contains__(tName):
            return self.symbols[tName]
        else:
            return None

    def purifyRowsAndCols(self, tR, tC):
        """
            Convert the indexes used to access a matrix or array element from
            vars to an integer value.
        """
        tRows = tR
        tCols = tC
        
        if type(tRows) == str: # Assignation using an index, e.g. i varriable
            tRows = self.getValue(tRows)
        if type(tCols) == str: # Assignation using an index, e.g. j variable
            tCols = self.getValue(tCols)

        return tRows, tCols

    def getValue(self, varName):
        numeric = {int, float}
        # If a varName is a numeric constant, return the value and stop the processing
        if type(varName) in numeric:
            return varName
        
        # Once here, for sure varName is a str, so begin the process.
        tName, tRows, tCols = self.stripVar(varName)
        # print(tName)
        tRows, tCols = self.purifyRowsAndCols(tRows, tCols)
        # tSymbol = self.getSymbolFromTable(tName) # Reference to Symbol on the SymbolTable
        tSymbol = self.symbols.get(tName)

        if tSymbol != None: # Verify that the variable exists already
            # tSymbol.printSymbol()
            return tSymbol.getValue(tRows, tCols)
        else:
            # print("No symbol found")
            return None

    def setValue(self, varName, newVal):
        tName, tRows, tCols = self.stripVar(varName)
        tRows, tCols = self.purifyRowsAndCols(tRows, tCols)
        # print(tName, tRows, tCols)
        
        symb = self.getSymbolFromTable(tName)
        symb.setValue(newVal, tRows, tCols)

    def displayTable(self):
        print("\n###################################################################")
        print("####################### TABLE OF SYMBOLS ##########################")
        print("###################################################################\n")
        print("Name\t\tType\tRows\tCols\tValue")
        for key, val in self.symbols.items():
            val.printSymbol()
        print("\n###################################################################\n")
        