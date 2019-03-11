import Token



class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = Token.Token(self.origin[self.position])
        self.OPS = ['+','-', '*', '/']
    
    def select_next(self):
        index = self.position
        if(index == len(self.origin)):
            self.actual = Token.Token('EOF')
            return      

        while self.origin[index] == ' ':
            index += 1
        token = ''
        while self.origin[index].isdigit():
            token +=str(self.origin[index])
            index+=1
            if(index == len(self.origin)):
                self.actual = Token.Token('EOF')
                break

        if token == '':
            self.actual = Token.Token(self.origin[index])
            self.position = index + 1
        else:
            self.actual = Token.Token(token)
            self.position = index
        
        

