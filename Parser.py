import Tokenizer


class Parser:
    def parse_term():
        result = 0
        if Parser.tokens.actual.type == 'int':
            result += int(Parser.tokens.actual.value)
            Parser.tokens.select_next()
            while Parser.tokens.actual.value in ['*', '/']:
                if Parser.tokens.actual.value == '*':
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.type == 'int':
                        result *= int(Parser.tokens.actual.value)
                    else:
                        raise Exception(f"Expected int type after operation, instead got {Parser.tokens.actual.type} ({Parser.tokens.actual.value})")
                elif Parser.tokens.actual.value == '/':
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.type == 'int':
                        result //= int(Parser.tokens.actual.value)
                    else:
                        raise Exception(f"Expected int type after operation, instead got {Parser.tokens.actual.type} ({Parser.tokens.actual.value})")
                else:
                    raise Exception(f"Expected * or / operation, instead got {Parser.tokens.actual.type} ({Parser.tokens.actual.value})")
                Parser.tokens.select_next()
        else:
            raise Exception(f"Expected int type, instead got {Parser.tokens.actual.type} ({Parser.tokens.actual.value})")
        return result
    
    def parse_expression():
        result = Parser.parse_term()
        while Parser.tokens.actual.value in ['+', '-']:
            if Parser.tokens.actual.value == '+':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result += int(new_term)

            elif Parser.tokens.actual.value == '-':
                Parser.tokens.select_next()
                new_term = Parser.parse_term()
                result -= int(new_term)
        return result


    def run(code):
        Parser.tokens = Tokenizer.Tokenizer(code)
        Parser.tokens.select_next()
        r = Parser.parse_expression()
        if Parser.tokens.actual.value == 'EOF':
            return r
            # raise Exception(f'Expected EOF instead got {Parser.tokens.actual.value}')
        else:
            return r