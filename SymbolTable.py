
class SymbolTable:
    def __init__(self, ancestor):
        self.ancestor = ancestor
        self.table = {}
    
    def get_value(self, key):
        try:
            return self.table[key]
        except KeyError:
            if self.ancestor is None:
                raise Exception(f'Variable {key} does not exist')
            return self.ancestor.get_value(key)
    
    def get_value_recursive(self, key):
        try:
            if self.table[key][0] is None:
                if self.ancestor is None:
                    raise Exception(f'Variable {key} does not exist')

                return self.ancestor.get_value_recursive(key)
            else:
                return self.table[key]
        except KeyError:
            if self.ancestor is None:
                raise Exception(f'Variable {key} does not exist')
            

            return self.ancestor.get_value_recursive(key)
    
    def alloc(self, key, var_type):
        self.table[key] = [None, var_type]

    def set_value(self, key, value):
        self.table[key][0] = value