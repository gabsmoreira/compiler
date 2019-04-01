
class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def get_value(self, key):
        try:
            return self.table[key]
        except KeyError:
            raise Exception(f'Variable {key} does not exist')
    
    def set_value(self, key, value):
        self.table[key] = value