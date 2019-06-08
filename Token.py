RESERVED = ['PRINT', 'BEGIN', 'END', 'WHILE', 'IF', 'WEND', 'THEN', 'ELSE', 'INPUT', 'DIM','INTEGER', 'BOOLEAN', 'AS', 'SUB', 'TRUE', 'FALSE', 'FUNCTION', 'CALL', 'AND', 'OR']

class Token:
    def __init__(self, token):
        self.OPS = ['+', '-', '/', '*']
        # self.TOKEN_TYPES = ['OP', 'INT', 'VAR', 'PRINT']
        self.value = token
        self.type = self.define_type(token)

    def define_type(self, token):
        if token == '/':
            return 'DIV'
        elif token == '*':
            return 'MULT'
        if token == '+':
            return 'PLUS'
        elif token == '-':
            return 'MINUS'
        elif token.isdigit():
            return 'INT'
        elif token == ',':
            return 'COMMA'
        elif token.upper() in RESERVED:
            return token.upper()
        elif token == 'EOF':
            return token
        elif token.isalpha():
            return 'VAR'
        elif token == '=':
            return 'EQUAL'
        elif token == '\n':
            return 'BL'
        elif token == '(':
            return 'OPENPAR'
        elif token == ')':
            return 'CLOSEPAR'
        elif token == '<':
            return 'SMALLER'
        elif token == '>':
            return 'BIGGER'
        else:
            return 'NONE'


