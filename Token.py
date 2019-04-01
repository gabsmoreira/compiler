RESERVED = ['PRINT', 'BEGIN', 'END', 'PRINT']

class Token:
    def __init__(self, token):
        self.OPS = ['+', '-', '/', '*']
        self.TOKEN_TYPES = ['OP', 'INT', 'VAR', 'PRINT']
        self.value = token
        self.type = self.define_type(token)

    def define_type(self, token):
        if token in self.OPS:
            return 'OP'
        elif token.isdigit():
            return 'INT'
        elif token.upper() in RESERVED:
            return token.upper()
        elif token == 'EOF':
            return token
        elif token.isalpha():
            return 'VAR'
        elif token == '=':
            return 'EQUAL'
        else:
            return 'BL'


