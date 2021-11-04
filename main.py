import re

def get_keywords(text):

    pattern = r"\bclass\b|\bconstructor\b|\bfunction\b|\bmethod\b|\bfield\b|\bstatic\b|\bvar\b|\bint\b|\bchar\b|\bboolean\b|\bvoid\b|\btrue\b|\bfalse\b|\bnull\b|\bthis\b|\blet\b|\bdo\b|\bif\b|\belse\b|\bwhile\b|\breturn\b"
  
    output = {}

    for m in re.finditer(pattern, text):
        
        start = m.start(0)

        end = m.end(0)

        aux = {
            "start": m.start(0),
            "end": m.end(0),
            "token": text[start:end],
            "type": "keyword"
        }

        output[start] = aux

    return output
  
    # regex = re.compile(pattern)
    # return regex.findall(text) 

def get_symbols(text):

    pattern = r"\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~"

    output = {}

    for m in re.finditer(pattern, text):

        start = m.start(0)

        end = m.end(0)

        aux = {
            "start": m.start(0),
            "end": m.end(0),
            "token": text[start:end],
            "type": "symbol"
        }

        output[start] = aux

    return output

    # regex = re.compile(pattern)
    # return regex.findall(text) 

def print_xml(d):

    print("<tokens>")

    for key in sorted(d):

        token = d[key]

        if token['type'] == 'keyword':

            print(f"<keyword> {token['token']} </keyword>")

        elif token['type'] == 'symbol':

            if token['token'] == '<':
                aux = "&lt"
            elif token['token'] == '>':
                aux = "&gt"
            elif token['token'] == '"':
                aux = "&quot"
            elif token['token'] == '&':
                aux = "&amp"
            else:
                aux = token['token']
            
            print(f"<symbol> {aux} </symbol>")

    print("</tokens>")


text = '''if (x < 0) {
// prints the sign
let sign = "negative";
}
'''

scan = {**get_keywords(text), **get_symbols(text)}
print_xml(scan)
