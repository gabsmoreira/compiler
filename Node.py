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
        if self.value == '+':
            return self.left.evaluate(symbol_table) + self.right.evaluate(symbol_table)
        elif self.value == '-':
            return self.left.evaluate(symbol_table) - self.right.evaluate(symbol_table)
        elif self.value == '*':
            return self.left.evaluate(symbol_table) * self.right.evaluate(symbol_table)
        elif self.value == '/':
            return self.left.evaluate(symbol_table) // self.right.evaluate(symbol_table)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        if self.value == '-':
            return - self.children.evaluate(symbol_table)
        elif self.value == '+':
            return self.children.evaluate(symbol_table)


class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass
    def evaluate(self):
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
        symbol_table.set_value(self.left.value, self.right.evaluate(symbol_table))
        return

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table):
        print(self.children.evaluate(symbol_table))
        return
