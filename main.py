import re

# Dicionario com os simbolos do xml
XML_TOKEN_MAP = {
    '<': "&lt",
    '>': "&gt",
    '"': "&quot",
    '&': "&amp"
}

# Dicionario de expressoes regulares para encontrar os tokens
PATTERNS = {
    "keyword": r"\bclass\b|\bconstructor\b|\bfunction\b|\bmethod\b|\bfield\b|\bstatic\b|\bvar\b|\bint\b|\bchar\b|\bboolean\b|\bvoid\b|\btrue\b|\bfalse\b|\bnull\b|\bthis\b|\blet\b|\bdo\b|\bif\b|\belse\b|\bwhile\b|\breturn\b",
    "symbol": r"\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~",
    "integer": r"\b\d+\b",
    "string": r'"([A-Za-z0-9_\./\\-]*)"',
    "identifier": r"([A-Za-z_][A-Za-z0-9_]*)",
}

# Lista com as palavras chaves
KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

class JackTokenizer:

    def __init__(self, file_name):

        # Pega apenas o nome do arquivo
        self.file_name = file_name.split("/")[-1].replace(".jack", "")

        # Lê o texto do arquivo
        self.text = self.read_file(file_name)

        # Dicionario com os tokens
        self.tokens_dict = self.search_tokens(self.text)

        # Lista ordenada com as chaves dos tokens
        self.tokens_list = sorted(self.tokens_dict)

        # Token atual
        self.current_token = ""
    
    # Lê o arquivo e retorna o texto
    def read_file(self, file_name):

        with open(file_name, 'r') as file:
            
            text = file.read()

            return text

    # Procura os tokens no texto
    def search_tokens(self, text):

        # Remove os comentários
        text = self.remove_comments(text)

        tokens = {}

        # Aplica cada expressão regular no texto
        for token_class in PATTERNS.keys():

            pattern = PATTERNS[token_class]

            # Procura os tokens com o padrão selecionado
            new_tokens = self.find_tokens(text, pattern, token_class)

            # Armazena os tokens no dicionário
            tokens = {**tokens, **new_tokens}

        return tokens
    

    # Remove os comentários de um texto
    def remove_comments(self, text):

        # Expressão regular que encontra os dois tipos de comentários (// e /***/)
        pattern = r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/|(//.*)"

        new_text = text

        for m in re.finditer(pattern, text):
            
            # Pega a posição onde o comentário encontrado inicia
            start = m.start(0)

            # Pega a posição onde o comentário encontrado termina 
            end = m.end(0)

            # Pega o comentário no texto
            comment = text[start:end]

            # Substitui o comentário por vazio
            new_text = new_text.replace(comment, "")

        # Retorna o texto sem comentários
        return new_text
    
    # Procura os tokens em um texto dado um padrão
    def find_tokens(self, text, pattern, token_class):

        tokens = {}

        for m in re.finditer(pattern, text):
            
            # Pega a posição onde o token encontrado inicia
            start = m.start(0)

            # Pega a posição onde o token encontrado termina
            end = m.end(0)

            # Pega o token no texto
            token = text[start:end]

            # Verifica se o símbolo é símbolo do xml
            if token_class == "symbol":

                if token in XML_TOKEN_MAP.keys():
                    
                    token = XML_TOKEN_MAP[token]

            # Remove as aspas do token string
            if token_class == "string":

                token = token.replace('"', "")

            # Verifica se o token identifier é uma palavra-chave
            if token_class == "identifier":

                if token in KEYWORDS:

                    continue
            
            # Dicionario que armazena as informações do token
            aux = {
                "start": m.start(0),
                "end": m.end(0),
                "token": token,
                "token_class": token_class
            }

            # Armazena o dict anterior no dict principal 
            tokens[start] = aux

        return tokens


    def advance(self):

        if self.has_more_tokens():

            self.current_token = self.tokens_dict[self.tokens_list[0]]

            del self.tokens_list[0]
        
        else:

            raise Exception("Não há tokens!")
    
    
    def has_more_tokens(self):

        if len(self.tokens_list) > 0:

            return True
        
        return False


    def token_tye(self):

        return self.current_token["token_class"]
    

    def get_token(self):

        return self.current_token["token"]

    
    # Exporta em xml os tokens encontrados 
    def export_xml(self):

        with open(f"xml/{self.file_name}.xml", "w") as xml:
            
            xml.write("<tokens>\n")

            for key in self.tokens_list:

                token = self.tokens_dict[key]

                xml.write(f"<{token['token_class']}> {token['token']} </{token['token_class']}>\n")

            xml.write("</tokens>")


tknz = JackTokenizer("10/Square/Square.jack")
tknz.export_xml()
