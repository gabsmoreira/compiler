class Node:
    def evaluate():
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.left = children[0]
        self.right = children[1]
    def evaluate(self, symbol_table):
        val1, var_type1 = self.left.evaluate(symbol_table)
        val2, var_type2 = self.right.evaluate(symbol_table)

        if var_type1 != var_type2:
            raise Exception(f'Cannot perform {self.value} with {var_type1} and {var_type2}')

        if var_type1 == 'INT':
            if self.value == '+':
                return self.left.evaluate(symbol_table)[0] + self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '-':
                return self.left.evaluate(symbol_table)[0] - self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '*':
                return self.left.evaluate(symbol_table)[0] * self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '/':
                return self.left.evaluate(symbol_table)[0] // self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '>':
                return self.left.evaluate(symbol_table)[0] > self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '<':
                return self.left.evaluate(symbol_table)[0] < self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '=':
                return self.left.evaluate(symbol_table)[0] == self.right.evaluate(symbol_table)[0], var_type1
        
        elif var_type1 == 'BOOLEAN':
            if self.value == 'AND':
                return self.left.evaluate(symbol_table)[0] and self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == 'OR':
                return self.left.evaluate(symbol_table)[0] or self.right.evaluate(symbol_table)[0], var_type1
            elif self.value == '=':
                return self.left.evaluate(symbol_table)[0] == self.right.evaluate(symbol_table)[0], var_type1
        
        else:
            raise Exception(f'Cannot perform {self.value} with {var_type1} and {var_type2}')

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        if self.value == '-':
            val, var_type = self.children.evaluate(symbol_table)
            if var_type != 'INT':
                raise Exception(f'Value {val} is not INT type')
            return - val, var_type

        elif self.value == '+':
            val, var_type = self.children.evaluate(symbol_table)
            if var_type != 'INT':
                raise Exception(f'Value {val} is not INT type')
            return  val, var_type

        elif self.value == 'NOT':
            val, var_type = self.children.evaluate(symbol_table)
            if var_type != 'BOOLEAN':
                raise Exception(f'Value {val} is not BOOLEAN type')
            return not val, var_type

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        return self.value, 'INT'

class NoOp(Node):
    def __init__(self, value ,children):
        self.children = children
        self.value = value
        pass
    def evaluate(self, symbol_table):
        return

class Id(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        return symbol_table.get_value(self.value)
        
class Statements(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)
        return

class Assigment(Node):
    def __init__(self, value, children):
        self.value = value
        self.left = children[0]
        self.right = children[1]
        self.children = children
    def evaluate(self, symbol_table):
        _, var_type = symbol_table.table[self.left.value]
        var_value, var_type2 = self.right.evaluate(symbol_table)
        if var_type != var_type2:
            raise Exception(f'Variable type ({var_type}) do not match with expression type ({var_type2})')
        symbol_table.set_value(self.left.value, var_value)
        return

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table)[0])
        return

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        i = int(input())
        return i, 'INT'

class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table)[0] == True:
            self.children[1].evaluate(symbol_table)
        return

class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table)[0] == True:
            self.children[1].evaluate(symbol_table)
        else:
            if len(self.children) == 3:
                self.children[2].evaluate(symbol_table)
        return
from SymbolTable import *

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        var_id = self.children[0].value
        var_type = self.children[1].evaluate(symbol_table)
        if var_id in symbol_table.table:
            raise Exception(f'Variable {var_id} already exists!')
        symbol_table.alloc(var_id, var_type)
        return
        
class Type(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        return self.value

class Boolean(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        return self.value, 'BOOLEAN'

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        symbol_table.alloc(self.value, 'FUNCTION')
        symbol_table.set_value(self.value, self)

class SubDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        symbol_table.alloc(self.value, 'SUB')
        symbol_table.set_value(self.value, self)

class FunCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        dec, dec_type = symbol_table.get_value_recursive(self.value)
        new_symbol_table = SymbolTable(symbol_table)
        begin = 0
        if dec_type == 'FUNCTION':
            ret_type = dec.children[0].evaluate(symbol_table)
            new_symbol_table.alloc(self.value, ret_type)
            begin = 1
        for i in range(begin, len(dec.children)-1):
            dec.children[i].evaluate(new_symbol_table)
            children_eval, child_eval_type = self.children[i-begin].evaluate(symbol_table)
            arg_type = dec.children[i].children[1].evaluate(symbol_table)
            if child_eval_type != arg_type:
                raise Exception(f'Variable type {arg_type} is not {child_eval_type} !')
            new_symbol_table.set_value(dec.children[i].children[0].value, children_eval)

        dec.children[len(dec.children)-1].evaluate(new_symbol_table)

        if dec_type == 'FUNCTION':
            return new_symbol_table.get_value(self.value)
        return

