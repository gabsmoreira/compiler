import Tokenizer
from Node import *

class Parser:
    def parse_term():
        result = Parser.parse_factor()
        while Parser.tokens.actual.value in ['*', '/']:
            if Parser.tokens.actual.value == '*':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                # result *= int(new_term)
                result = BinOp('*', [result, new_term])
                # return result

            elif Parser.tokens.actual.value == '/':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                # result //= int(new_term)
                result = BinOp('/', [result, new_term])
                # return result
        return result
    
    def parse_expression():
        result = Parser.parse_term()
        while Parser.tokens.actual.value in ['+', '-']:
            if Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('+', [result, new_term])
                # result += int(new_term)
                # return result

            elif Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('-', [result, new_term])
                # result += int(new_term)
                # return result
        return result
    
    def parse_factor():
        result = 0
        if Parser.tokens.actual.type == 'int':
            result = int(Parser.tokens.actual.value)
            int_val = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.select_next()
            return int_val
            

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            new_term = Parser.parse_expression()
            result = int(new_term)
            if Parser.tokens.actual.value != ')':
                raise Exception(f"Invalid token in column {Parser.tokens.position}")
            else:
                Parser.tokens.select_next()

        elif Parser.tokens.actual.value in ['+', '-']:
            if Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                un_op = UnOp('-', new_term)
                # result = -int(new_term)
                return un_op
            
            elif Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                un_op = UnOp('+', new_term)
                # result = int(new_term)
                return un_op
        else:
            raise Exception(f"Unexpected token in column {Parser.tokens.position}")
        return result

    def run(code):
        Parser.tokens = Tokenizer.Tokenizer(code)
        Parser.tokens.select_next()
        r = Parser.parse_expression()
        if Parser.tokens.actual.value == 'EOF':
            return r
        else:
            raise Exception(f'Expected EOF instead got {Parser.tokens.actual.value}')
            # return r
