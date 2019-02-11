from Tokens import Tokens

file_path = 'program.txt'
with open(file_path, 'rb') as file:
    clean_lines = []
    for i, line in enumerate(file.readlines()):
        clean_lines.append(line.decode('utf-8'))

for line in clean_lines:
    token_list = []
    line_split = list(line.strip().split(' '))
    for obj in line_split:
        tokens = list(obj)
        for token in tokens:
            token_list.append(Tokens(token))
        # [print(token.token, '-', token.type) for token in token_list]

sep = []
index = -1
# [print(token.token) for token in token_list]
for i, token in enumerate(token_list):
    if(i != 0):
        if(token_list[i-1].type == 'int' and token_list[i].type == 'int'):
            try:
                sep[index] = str(sep[index]) + str(token.token)
            except Exception as e:
                sep.append(str(token.token))
        elif(token.type == 'int'):
            sep.append(str(token.token))
            index +=1
        else:
            index +=1
            sep.append(str(token.token))
    else:
        if(token.type == 'int'):
            sep.append(str(token.token))
            index+=1
        else:
            sep.append(str(token.token))

def is_op(token):
    try:
        a = type(int(token))
    except ValueError as e:
        return True
    return False

nice = []
for i, token in enumerate(sep):
    try:
        if(is_op(sep[i-1]) and is_op(sep[i]) != True):
            nice.append(str(sep[i-1]) + token)
        else:
            if(is_op(token) != True):
                nice.append(token)
    except IndexError:
        pass

total = 0
for number in nice:
    total += int(number)
print(total)
