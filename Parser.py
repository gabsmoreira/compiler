import Tokenizer


class Parser:
    
    def parse_expression(self):
        result = 0
        Parser.tokens.select_next()
        if Parser.tokens.actual.type == 'int':
            result = int(Parser.tokens.actual.value)
            Parser.tokens.select_next()
            while Parser.tokens.actual.value != 'EOF':
                if Parser.tokens.actual.value == '+':
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.type == 'int':
                        result += int(Parser.tokens.actual.value)
                    else:
                        print(f"Expected int after operation, instead got {Parser.tokens.actual.value}")
                        raise(ValueError)

                elif Parser.tokens.actual.value == '-':
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.type == 'int':
                        result -= int(Parser.tokens.actual.value)
                    else:
                        print(f"Expected int after operation, instead got {Parser.tokens.actual.value}")
                        raise(ValueError)
                else:
                    print(f"Expected + or - operation, instead got {Parser.tokens.actual.value}")
                    raise(ValueError)
                
                Parser.tokens.select_next()
        else:
            print(f"Expected int type, instead got {Parser.tokens.actual.type}")
            raise(ValueError)
        return result




    def run(self, code):
        Parser.tokens = Tokenizer.Tokenizer(code)