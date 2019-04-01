import Tokenizer
from Parser import Parser
from PrePro import PrePro
from SymbolTable import SymbolTable


file_path = 'program.vbs'
with open(file_path, 'rb') as file:
    content = file.read().decode('utf-8')
    prepro = PrePro.filter(content)
    print(prepro)
    symbol_table = SymbolTable()
    a = Parser.run(prepro)
    a.evaluate(symbol_table)
