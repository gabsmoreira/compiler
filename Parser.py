import Tokenizer
from Node import *

class Parser:

    def parse_statements():
        if Parser.tokens.actual.type != 'BEGIN':
            raise Exception(f'Missing Begin in column {Parser.tokens.position}')

        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'BL':
            raise Exception(f'Expected break line in column {Parser.tokens.position}')

        Parser.tokens.select_next()
        children = []

        while Parser.tokens.actual.type != 'END':
            new_child = Parser.parse_statement()
            children.append(new_child)
            if Parser.tokens.actual.type == 'BL':
                Parser.tokens.select_next()
            else:
                raise Exception(f'Expected break line in column {Parser.tokens.position}')

        Parser.tokens.select_next()
        return Statements('X', children) 
      
    def parse_statement():
        if Parser.tokens.actual.type == 'VAR':
            var = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            if Parser.tokens.actual.type == 'EQUAL':
                Parser.tokens.select_next()
                new_value = Parser.parse_expression()
                assigment = Assigment("=", [var, new_value])
                return assigment
            else:
                raise Exception(f'Unexpected token in column {Parser.tokens.position}')
        elif Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.select_next()
            value = Parser.parse_expression()
            print_value = Print('PRINT',value)
            return print_value

        elif Parser.tokens.actual.type == 'BEGIN':
            return Parser.parse_statements()
        else:
            return NoOp()


    def parse_term():
        result = Parser.parse_factor()
        while Parser.tokens.actual.value in ['*', '/']:
            if Parser.tokens.actual.value == '*':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                result = BinOp('*', [result, new_term])

            elif Parser.tokens.actual.value == '/':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                result = BinOp('/', [result, new_term])
        return result
    
    def parse_expression():
        result = Parser.parse_term()
        while Parser.tokens.actual.value in ['+', '-']:
            if Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('+', [result, new_term])

            elif Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('-', [result, new_term])
        return result
    
    def parse_factor():
        result = 0
        if Parser.tokens.actual.type == 'INT':
            result = int(Parser.tokens.actual.value)
            int_val = IntVal(int(Parser.tokens.actual.value), [])
            Parser.tokens.select_next()
            return int_val
            
        elif Parser.tokens.actual.type == 'VAR':
            identifier = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            return identifier

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            new_term = Parser.parse_expression()
            result = new_term
            if Parser.tokens.actual.value != ')':
                raise Exception(f"Invalid token in column {Parser.tokens.position}")
            else:
                Parser.tokens.select_next()

        elif Parser.tokens.actual.value in ['+', '-']:
            if Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                un_op = UnOp('-', new_term)
                return un_op
            
            elif Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                un_op = UnOp('+', new_term)
                return un_op
        else:
            raise Exception(f"Unexpected token in column {Parser.tokens.position}")
        return result

    def run(code):
        Parser.tokens = Tokenizer.Tokenizer(code)
        Parser.tokens.select_next()
        r = Parser.parse_statements()
        if Parser.tokens.actual.value == 'EOF':
            return r
        else:
            # raise Exception(f'Expected EOF instead got {Parser.tokens.actual.value}')
            return r
