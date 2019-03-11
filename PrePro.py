class PrePro:
    def filter(code):
        index = 0
        nice = []
        while index < len(code):
            if code[index] == "'":
                break
            else:
                if code[index] == ' ':
                    index +=1
                    continue
                else:
                    nice.append(code[index])
            index +=1
        return nice
