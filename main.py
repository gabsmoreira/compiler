import Tokenizer
import Parser

file_path = 'program.txt'
with open(file_path, 'rb') as file:
    lines = []
    for i, line in enumerate(file.readlines()):
        lines.append(line.decode('utf-8'))

lines = lines[0]

a = Parser.Parser()
a.run(lines)
a = a.parse_expression()
# r = a.run(lines)
print(a)