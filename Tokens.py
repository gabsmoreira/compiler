class Tokens:

    def __init__(self, token):
        self.OPS = ['+', '-', '/', '*']
        self.TOKEN_TYPES = ['op', 'int', 'str']
        self.token = token
        self.type = self.define_type(token)

    def define_type(self, token):
        if(token in self.OPS):
            return 'op'
        elif(int(token) in list(range(0,10))):
            return 'int'
        else:
            return 'str'


