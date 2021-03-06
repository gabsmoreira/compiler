import Tokenizer
from Parser import Parser
from PrePro import PrePro
from SymbolTable import SymbolTable
import sys
from Translator import Translator

file_name = sys.argv[1]
# file_name = 'program.vbs'


with open(file_name, 'rb') as file:
    content = file.read().decode('utf-8')
    prepro = PrePro.filter(content)
    tokens = Tokenizer.Tokenizer(prepro)
    # tokens.select_next()
    # for i in range(100):
    #     print(tokens.actual.type)
    #     tokens.select_next()
    symbol_table = SymbolTable()
    a = Parser.run(prepro)
    a.evaluate(symbol_table)
    print(''.join(Translator.code))

with open('program.asm', 'w+') as file:
    file.write(''.join(Translator.code))
    

def nodes (n):
    if n != None:
        for child in n.children:
            nodes(child)
            print(child.value)

# nodes(a)
