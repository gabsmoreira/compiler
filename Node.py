class Node:
    def evaluate():
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.left = children[0]
        self.right = children[1]
    def evaluate(self):
        if self.value == '+':
            return self.left.evaluate() + self.right.evaluate()
        elif self.value == '-':
            return self.left.evaluate() - self.right.evaluate()
        elif self.value == '*':
            return self.left.evaluate() * self.right.evaluate()
        elif self.value == '/':
            return self.left.evaluate() // self.right.evaluate()

class UnOp(Node):
    def __init__(self, value, child):
        self.value = value
        self.child = child
    def evaluate(self):
        if self.value == '-':
            return - self.child.evaluate()
        elif self.value == '+':
            return self.child.evaluate()


class IntVal(Node):
    def __init__(self, value):
        self.value = value
    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass
    def evaluate():
        return