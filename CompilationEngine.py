from os import write
from os.path import exists

OP_TERMS = ['+', '-', '*', '/', '&amp', '|', '&lt', '&gt', '=']

class CompilationEngine:


    def __init__(self, tknz):
        self.tknz = tknz
        self.file_name = tknz.file_name
        self.begin = True


    def compile_statements(self):

        self.write_xml_line("<statements>")

        token = self.tknz.get_token()

        if token == "if":

            self.compile_if_statements()
        
        elif token == "while":

            self.compile_while_statements()
        
        elif token == "let":

            self.compile_let_statements()

        elif token == "class":

            self.compile_class_statements()

        self.write_xml_line("</statements>")


    def compile_class_statements(self):

        self.write_xml_line("<classStatement>")

        self.engine_advance()

        self.engine_advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.engine_advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.engine_advance(token_advance=False)
        
        self.write_xml_line("</classStatement>")  
    

    def compile_if_statements(self):

        self.write_xml_line("<ifStatement>")

        self.engine_advance()

        if self.tknz.get_token() != "(":
            raise Exception("Expected '('")

        self.engine_advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ")":
            raise Exception("Expected ')'")

        self.engine_advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.engine_advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.engine_advance(token_advance=False)
        
        self.write_xml_line("</ifStatement>")
    

    def compile_while_statements(self):

        self.write_xml_line("<whileStatement>")

        self.engine_advance()

        if self.tknz.get_token() != "(":
            raise Exception("Expected '('")

        self.engine_advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ")":
            raise Exception("Expected ')'")

        self.engine_advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.engine_advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.engine_advance(token_advance=False)
        
        self.write_xml_line("</whileStatement>")


    def compile_let_statements(self):

        self.write_xml_line("<letStatement>")

        self.engine_advance()

        self.engine_advance()

        if self.tknz.get_token() != "=":
            raise Exception("Expected '='")

        self.engine_advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ";":
            raise Exception("Expected ';'")

        self.engine_advance()

        self.write_xml_line("</letStatement>")


    def compile_expression(self):

        self.write_xml_line("<expression>")

        self.compile_term()

        self.tknz.advance()

        token = self.tknz.get_token()

        if token in OP_TERMS:

            self.compile_op()

            self.tknz.advance()
        
            self.compile_term()
        
        self.write_xml_line("</expression>")


    def compile_term(self):

        self.write_xml_line("<term>")

        self.engine_advance(token_advance=False)

        self.write_xml_line("</term>")


    def compile_var_name(self):
        pass


    def compile_constant(self):
        pass


    def compile_op(self):
        
        self.engine_advance(token_advance=False)
    

    def write_xml_line(self, line):

        xml_file_path = f'xml/{self.file_name}T.xml'

        if exists(xml_file_path) and self.begin:

            with open(xml_file_path, 'w') as xml:

                xml.write(f'{line}\n')
            
            self.begin = False
        
        elif not exists(xml_file_path):

            with open(xml_file_path, 'w') as xml:

                xml.write(f'{line}\n')

        else:

            with open(xml_file_path, 'a') as xml:

                xml.write(f'{line}\n')
          
    

    def engine_advance(self, token_advance=True):

        token = self.tknz.get_token()
        token_tye = self.tknz.token_tye()

        line = f'<{token_tye}> {token} </{token_tye}>'

        self.write_xml_line(line)

        if token_advance:

            self.tknz.advance()


    def run(self):
        
        self.compile_statements()
