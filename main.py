import Tokenizer
from Parser import Parser
from PrePro import PrePro


lines = input()
# file_path = 'program.txt'
# with open(file_path, 'rb') as file:
#     lines = []
#     for i, line in enumerate(file.readlines()):
#         lines.append(line.decode('utf-8'))
# lines = lines[0]


lines = PrePro.filter(lines)
# print(lines)
a = Parser.run(lines)
print(a)