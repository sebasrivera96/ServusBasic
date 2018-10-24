"""
    This class will be used to store intermediate values when creating the 
    intermediate code. 
"""

class Temp:
    def __init__(self, valueType = int, val = 0):
        self.valueType = valueType
        self.value = val

    def set(self, valueType, val):
        self.valueType = valueType
        self.val = val

    def get(self):
        return valueType, val
