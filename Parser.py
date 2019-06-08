import Tokenizer
from Node import *

class Parser:

    def parse_program():
        funcs_or_subs = []

        while Parser.tokens.actual.type != 'EOF':
            if Parser.tokens.actual.type == 'SUB':
                sub_dec = Parser.parse_sub_dec()
                funcs_or_subs.append(sub_dec)

            elif Parser.tokens.actual.type == 'FUNCTION':
                func_dec = Parser.parse_func_dec()
                funcs_or_subs.append(func_dec)

            elif Parser.tokens.actual.type == 'BL':
                Parser.tokens.line +=1
                Parser.tokens.select_next()

            else:
                raise Exception(f'Expected FUNC or SUB in line {Parser.tokens.line} {Parser.tokens.actual.value}')

        call_main = FunCall('main',[])
        funcs_or_subs.append(call_main)
                
        return Statements('X', funcs_or_subs)

    def parse_sub_dec():
        if Parser.tokens.actual.type != 'SUB':
            raise Exception(f'Expected SUB in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'VAR':
            raise Exception(f'Expected identifier in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        sub_name = Parser.tokens.actual.value
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'OPENPAR':
            raise Exception(f'Expected ( in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        var_decs = []
        # print(Parser.tokens.actual.value)
        while True: 
            if Parser.tokens.actual.type == 'CLOSEPAR':
                Parser.tokens.select_next()
                break
            
            if Parser.tokens.actual.type != 'VAR':
                raise Exception(f'Expected identifier in line {Parser.tokens.line} {Parser.tokens.actual.value}')
                
            var_id = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()

            if Parser.tokens.actual.type != 'AS':
                raise Exception(f'Expected AS in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
            Parser.tokens.select_next()

            var_type = Parser.parse_type()
            
            var_decs.append(VarDec('value', [var_id, var_type]))

            if Parser.tokens.actual.type == 'CLOSEPAR':
                Parser.tokens.select_next()
                break

            elif Parser.tokens.actual.type == 'COMMA':
                Parser.tokens.select_next()
                continue
            Exception(f'Expected , after argument in line {Parser.tokens.line} {Parser.tokens.actual.value}')
            
        if Parser.tokens.actual.type != 'BL':
            raise Exception(f'Expected BREAKLINE in line {Parser.tokens.line} {Parser.tokens.actual.value}')

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
        statements = Statements('X', statements)
        var_decs.append(statements)
        return SubDec(sub_name, var_decs)


    def parse_func_dec():
        if Parser.tokens.actual.type != 'FUNCTION':
            raise Exception(f'Expected FUNCTION in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'VAR':
            raise Exception(f'Expected identifier in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        func_name = Parser.tokens.actual.value
        Parser.tokens.select_next()

        if Parser.tokens.actual.type != 'OPENPAR':
            raise Exception(f'Expected ( in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()


        var_decs = []
        while True: 
            if Parser.tokens.actual.type == 'CLOSEPAR':
                Parser.tokens.select_next()
                break

            if Parser.tokens.actual.type != 'VAR':
                raise Exception(f'Expected identifier in line {Parser.tokens.line} {Parser.tokens.actual.value}')

            var_id = Id(Parser.tokens.actual.value, [])
            Parser.tokens.select_next()

            if Parser.tokens.actual.type != 'AS':
                raise Exception(f'Expected AS in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
            Parser.tokens.select_next()

            var_type = Parser.parse_type()
            
            var_decs.append(VarDec('value', [var_id, var_type]))

            if Parser.tokens.actual.type == 'CLOSEPAR':
                Parser.tokens.select_next()
                break

            elif Parser.tokens.actual.type == 'COMMA':
                Parser.tokens.select_next()
                continue
            Exception(f'Expected , after argument in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        if Parser.tokens.actual.type != 'AS':
            raise Exception(f'Expected AS in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()
        var_type = Parser.parse_type()
        var_decs.insert(0, var_type)


        if Parser.tokens.actual.type != 'BL':
            raise Exception(f'Expected BREAKLINE in line {Parser.tokens.line} {Parser.tokens.actual.value}')

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

        if Parser.tokens.actual.type != 'FUNCTION':
            raise Exception(f'Expected FUNCTION in line {Parser.tokens.line} {Parser.tokens.actual.value}')
        
        Parser.tokens.select_next()
        statements = Statements('func', statements)
        var_decs.append(statements)

        return FuncDec(func_name, var_decs)



    def parse_type():
        if Parser.tokens.actual.type in ['INTEGER', 'BOOLEAN']:
            if Parser.tokens.actual.type == 'INTEGER':
                ret_val = Type('INT', [])
                Parser.tokens.select_next()
                return ret_val
            ret_val = Type(Parser.tokens.actual.value.upper(), [])
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

        elif Parser.tokens.actual.type == 'CALL':
            Parser.tokens.select_next()

            if Parser.tokens.actual.type != 'VAR':
                raise Exception(f'Expected identifier after CALL in line {Parser.tokens.line}')
            identifier = Parser.tokens.actual.value
            Parser.tokens.select_next()

            if Parser.tokens.actual.type != 'OPENPAR':
                raise Exception(f'Expected OPENPAR after CALL in line {Parser.tokens.line}')
            Parser.tokens.select_next()

            rel_express = []
            one_arg = True
            while Parser.tokens.actual.type != 'CLOSEPAR':
                if one_arg == False:
                    if Parser.tokens.actual.type != 'COMMA':
                        raise Exception(f'Expected COMMA after CALL in line {Parser.tokens.line}')
                    Parser.tokens.select_next()

                rel_express.append(Parser.parse_rel_expression())

                one_arg = False
                        
            Parser.tokens.select_next()
            return FunCall(identifier, rel_express)
        
        elif Parser.tokens.actual.type == 'IF':
            children_if = []
            Parser.tokens.select_next()
            rel_expression = Parser.parse_rel_expression()
            children_if.append(rel_expression)

            if Parser.tokens.actual.type != 'THEN':
                raise Exception(f'Expected THEN inside IF, instead got {Parser.tokens.actual.type}')
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
            
            # sera?
            # Parser.tokens.select_next()
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
        while Parser.tokens.actual.type in ['MULT', 'DIV', 'AND']:
            if Parser.tokens.actual.value == '*':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                result = BinOp('*', [result, new_term])

            elif Parser.tokens.actual.value == '/':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                result = BinOp('/', [result, new_term])
            
            elif Parser.tokens.actual.type == 'AND':
                Parser.tokens.select_next()
                new_term = Parser.parse_factor()
                result = BinOp('AND', [result, new_term])
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
        while Parser.tokens.actual.type in ['PLUS', 'MINUS', 'OR']:
            if Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('+', [result, new_term])

            elif Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('-', [result, new_term])

            elif Parser.tokens.actual.value == 'OR':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result = BinOp('OR', [result, new_term])
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
            if Parser.tokens.actual.type != 'OPENPAR':
                return identifier
            else:
                Parser.tokens.select_next()
                rel_express = []
                while Parser.tokens.actual.type != 'CLOSEPAR':
                    rel_express.append(Parser.parse_rel_expression())
                    if Parser.tokens.actual.type == 'COMMA':
                        Parser.tokens.select_next()
                        continue
                    else:
                        break
                Parser.tokens.select_next()
                return FunCall(identifier.value, rel_express)


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
