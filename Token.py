class Token:
    def __init__(self, token):
        self.OPS = ['+', '-', '/', '*']
        self.TOKEN_TYPES = ['operation', 'int', 'str']
        self.value = token
        self.type = self.define_type(token)

    def define_type(self, token):
        if(token in self.OPS):
            return 'operation'
        elif(token.isdigit()):
            return 'int'
        else:
            return 'str'


