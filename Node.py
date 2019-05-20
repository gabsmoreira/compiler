from Translator import Translator

class Node:
    i = 0
    def evaluate():
        pass
    @staticmethod
    def get_new_id():
        Node.i+=1
        return Node.i


class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.left = children[0]
        self.right = children[1]
        self.id = Node.get_new_id()
    def evaluate(self, symbol_table):
        val1, var_type1 = self.left.evaluate(symbol_table)
        Translator.insert('PUSH EBX; \n')
        val2, var_type2 = self.right.evaluate(symbol_table)
        Translator.insert('POP EAX; \n')

        if var_type1 != var_type2:
            raise Exception(f'Cannot perform {self.value} with {var_type1} and {var_type2}')

        if var_type1 == 'INT':
            if self.value == '+':
                Translator.insert('ADD EAX, EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 + val2, var_type1
            elif self.value == '-':
                Translator.insert('SUB EAX, EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 - val2, var_type1
            elif self.value == '*':
                Translator.insert('IMUL EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 * val2, var_type1
            elif self.value == '/':
                Translator.insert('IDIV EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 //val2, var_type1
            elif self.value == '>':
                Translator.insert('CMP EAX, EBX; \n')
                Translator.insert('CALL binop_jg; \n')
                return val1 > val2, var_type1
            elif self.value == '<':
                Translator.insert('CMP EAX, EBX; \n')
                Translator.insert('CALL binop_jl; \n')
                return val1 < val2, var_type1
            elif self.value == '=':
                Translator.insert('CMP EAX, EBX; \n')
                Translator.insert('CALL binop_je; \n')
                return val1 == val2, var_type1
        
        elif var_type1 == 'BOOLEAN':
            if self.value == 'AND':
                Translator.insert('AND EAX, EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 and val2, var_type1
            elif self.value == 'OR':
                Translator.insert('OR EAX, EBX; \n')
                Translator.insert('MOV EBX, EAX; \n')
                return val1 or val2, var_type1
            elif self.value == '=':
                Translator.insert('CMP EAX, EBX; \n')
                Translator.insert('CALL binop_je; \n')
                return val1 == val2, var_type1
        
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
        self.id = Node.get_new_id()
    def evaluate(self, symbol_table):
        Translator.insert(f'MOV EBX, {self.value}; \n')
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
        disp = symbol_table.table[self.value][2]
        Translator.insert(f'MOV EBX, [EBP {disp}]; \n')
        
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
        _, var_type, displac = symbol_table.table[self.left.value]
        var_value, var_type2 = self.right.evaluate(symbol_table)
        if var_type != var_type2:
            raise Exception(f'Variable type ({var_type}) do not match with expression type ({var_type2})')
        disp = symbol_table.table[self.left.value][2]
        Translator.insert(f'MOV [EBP {disp}], EBX; \n')
        symbol_table.set_value(self.left.value, var_value)
        return

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table)[0])
        Translator.insert('PUSH EBX; \n')
        Translator.insert('CALL print; \n')
        Translator.insert('POP EBX; \n')
        # print(''.join(Translator.code))
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
        self.id = Node.get_new_id()
    def evaluate(self, symbol_table):
        Translator.insert(f'LOOP_{self.id}; \n')
        self.children[0].evaluate(symbol_table)
        Translator.insert('CMP EBX, False; \n')
        Translator.insert(f'JE EXIT_{self.id}; \n')
        self.children[1].evaluate(symbol_table)
        Translator.insert(f'JMP LOOP_{self.id}; \n')
        Translator.insert(f'EXIT_{self.id}; \n')
        # while self.children[0].evaluate(symbol_table)[0] == True:
        #     self.children[1].evaluate(symbol_table)
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

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        var_id = self.children[0].value
        var_type = self.children[1].evaluate(symbol_table)
        if var_id in symbol_table.table:
            raise Exception(f'Variable {var_id} already exists!')
        Translator.insert('PUSH DWORD 0; \n')
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
        Translator.insert(f'MOV EBX, {self.value.capitalize()}; \n')
        return self.value, 'BOOLEAN'
