
class SymbolTable:
    def __init__(self):
        self.table = {}
        self.disp = 0
    
    def get_value(self, key):
        try:
            return [self.table[key][0], self.table[key][1]]
        except KeyError:
            raise Exception(f'Variable {key} does not exist')
    
    def alloc(self, key, var_type):
        self.new_displ()
        self.table[key] = [None, var_type, self.disp]

    def set_value(self, key, value):
        self.table[key][0] = value
    
    def new_displ(self):
        self.disp -=4
        return self.disp