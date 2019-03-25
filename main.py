import Tokenizer
from Parser import Parser
from PrePro import PrePro


# lines = input()
file_path = 'program.txt'
with open(file_path, 'rb') as file:
    for line in file.readlines():
        # lines.append(line.decode('utf-8'))
        readable_line = line.decode('utf-8')
        prepro = PrePro.filter(readable_line)
        # print(lines)
        a = Parser.run(prepro)
        print(a.evaluate())
        