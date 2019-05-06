import Tokenizer
from Node import *

class Parser:

    def parse_program():
        if Parser.tokens.actual.type != 'SUB':
            raise Exception(f'Expected SUB in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'MAIN':
            raise Exception(f'Expected MAIN in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'OPENPAR':
            raise Exception(f'Expected ( in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'CLOSEPAR':
            raise Exception(f'Expected ) in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'BL':
            raise Exception(f'Expected break line in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.line +=1
        Parser.tokens.select_next()

        statements = []
        while Parser.tokens.actual.type != 'END':
            statement = Parser.parse_statement()
            statements.append(statement)
            if Parser.tokens.actual.type == 'BL':
                Parser.tokens.line +=1
                Parser.tokens.select_next()
            else:
                raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'SUB':
            raise Exception(f'Expected SUB in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        return Statements('X', statements) 


    def parse_type():
        if Parser.tokens.actual.type in ['INTEGER', 'BOOLEAN']:
            if Parser.tokens.actual.type == 'INTEGER':
                ret_val = Type('INT', [])
                Parser.tokens.select_next()
                return ret_val
            ret_val = Type(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            return ret_val
      
    def parse_statement():
        if Parser.tokens.actual.type == 'VAR':
            var = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            if Parser.tokens.actual.type == 'EQUAL':
                Parser.tokens.select_next()
                new_value = Parser.parse_rel_expression()
                return Assigment("=", [var, new_value])
            else:
                raise Exception(f'Unexpected token got {Parser.tokens.actual.value}')
        
        elif Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.select_next()
            value = Parser.parse_rel_expression()
            return Print('PRINT',[value])

        elif Parser.tokens.actual.type == 'WHILE':
            Parser.tokens.select_next()
            rel_expression = Parser.parse_rel_expression()
            if Parser.tokens.actual.type != 'BL':
                raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')
            Parser.tokens.line +=1
            Parser.tokens.select_next()
            children = []
            while Parser.tokens.actual.type !='WEND':
                statement = Parser.parse_statement()
                children.append(statement)
                if Parser.tokens.actual.type == 'BL':
                    Parser.tokens.line +=1
                    Parser.tokens.select_next()
                else:
                    raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')

            Parser.tokens.select_next()
            
            return While('while', [rel_expression, Statements('statements', children)])

        elif Parser.tokens.actual.type == 'DIM':
            Parser.tokens.select_next()
            var_id = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            if Parser.tokens.actual.type != 'AS':
                raise Exception(f'Expected AS after variable declaration {var_id.value} in line {Parser.tokens.line}')
            
            Parser.tokens.select_next()
            var_type = Parser.parse_type()
            return VarDec('value', [var_id, var_type])

        
        elif Parser.tokens.actual.type == 'IF':
            children_if = []
            Parser.tokens.select_next()
            rel_expression = Parser.parse_rel_expression()
            children_if.append(rel_expression)
            if Parser.tokens.actual.type != 'THEN':
                raise Exception(f'Expected THEN inside IF, instead got {Parser.tokens.actual.value}')
            Parser.tokens.select_next()
            if Parser.tokens.actual.type != 'BL':
                raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')

            Parser.tokens.line +=1
            Parser.tokens.select_next()

            children_statements = []
            while Parser.tokens.actual.type not in ['ELSE', 'END']:
                statement = Parser.parse_statement()
                children_statements.append(statement)
                if Parser.tokens.actual.type == 'BL':
                    Parser.tokens.line +=1
                    Parser.tokens.select_next()
                else:
                    raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')

            children_if.append(Statements('statements', children_statements))



            if Parser.tokens.actual.type == 'ELSE':
                Parser.tokens.select_next()
                if Parser.tokens.actual.type != 'BL':
                    raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')

                Parser.tokens.line +=1
                Parser.tokens.select_next()
                children_else = []

                while Parser.tokens.actual.type != 'END':
                    statement = Parser.parse_statement()
                    children_else.append(statement)
                    if Parser.tokens.actual.type == 'BL':
                        Parser.tokens.line +=1
                        Parser.tokens.select_next()
                    else:
                        raise Exception(f'Expected break line {Parser.tokens.line} {Parser.tokens.actual.value}')

                children_if.append(Statements('statements', children_else))

            
            if Parser.tokens.actual.type != 'END':
                raise Exception(f'Expected END, instead got {Parser.tokens.actual.value}') 

            Parser.tokens.select_next()
            if Parser.tokens.actual.type != 'IF':
                raise Exception(f'Expected IF after END, instead got {Parser.tokens.actual.value}')
            Parser.tokens.select_next()

            return If('if', children_if)
            
        else:
            return NoOp('x', [])

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
    
    def parse_rel_expression():
        result = Parser.parse_expression()
        if Parser.tokens.actual.value == '=':
            Parser.tokens.select_next()
            new_term = Parser.parse_expression()
            result = BinOp('=', [result, new_term])

        elif Parser.tokens.actual.value == '<':
            Parser.tokens.select_next()
            new_term = Parser.parse_expression()
            result = BinOp('<', [result, new_term])
        
        elif Parser.tokens.actual.value == '>':
            Parser.tokens.select_next()
            new_term = Parser.parse_expression()
            result = BinOp('>', [result, new_term])
        
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
            
        elif Parser.tokens.actual.type in ['TRUE', 'FALSE']:
            boolean = Boolean(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            return boolean

        elif Parser.tokens.actual.type == 'VAR':
            identifier = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()
            return identifier

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            new_term = Parser.parse_rel_expression()
            result = new_term
            if Parser.tokens.actual.value != ')':
                raise Exception(f"Invalid token {Parser.tokens.actual.value} in line {Parser.tokens.line}")
            else:
                Parser.tokens.select_next()

        elif Parser.tokens.actual.value in ['+', '-'] or Parser.tokens.actual.type == 'NOT':
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
            
            elif Parser.tokens.actual.type == 'NOT':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                un_op = UnOp('NOT', new_term)
                return un_op
            
        elif Parser.tokens.actual.type == 'INPUT':
            Parser.tokens.select_next()
            inp = Input('INPUT', [])
            # new_term = Parser.parse_factor()
            # un_op = UnOp('NOT', new_term)
            return inp

        else:
            raise Exception(f"Unexpected token {Parser.tokens.actual.type}")
        return result

    def run(code):
        Parser.tokens = Tokenizer.Tokenizer(code)
        Parser.tokens.select_next()
        r = Parser.parse_program()
        if Parser.tokens.actual.value == 'EOF':
            return r
        else:
            raise Exception(f'Expected EOF instead got {Parser.tokens.actual.value}')
            # return r
