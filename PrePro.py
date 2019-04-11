class PrePro:
    def filter(code):
        filtered = ""
        has_comment = False
        for c in code:
            if c == "\n":
                has_comment = False
            
            if has_comment == True:
                continue
                
            if c == "'":
                has_comment = True
                continue
            filtered += c.lower()

        return filtered