class PrePro:
    def filter(code):
        index = 0
        nice = []
        # print(code)
        while index < len(code):
            if code[index] == "'":
                while code[index] != '\n' and index < len(code):    
                    # print(code[index])
                    index +=1
                # index+=1
            else:
                nice.append(code[index])
            index +=1
        # print(nice)
        return nice
