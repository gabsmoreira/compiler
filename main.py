import Tokenizer
from Parser import Parser
from PrePro import PrePro
from SymbolTable import SymbolTable
import sys

file_name = sys.argv[1]
# file_name = 'program.vbs'


# file_path = 'program.vbs'
with open(file_name, 'rb') as file:
    content = file.read().decode('utf-8')
    prepro = PrePro.filter(content)
    tokens = Tokenizer.Tokenizer(prepro)
    symbol_table = SymbolTable()
    a = Parser.run(prepro)
    a.evaluate(symbol_table)
