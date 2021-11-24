
OP_TERMS = ['+', '-', '*', '/', '&amp', '|', '&lt', '&gt', '=']

class CompilationEngine:


    def __init__(self, tknz):
        self.tknz = tknz
        pass


    def compile_statements(self):

        print("<statements>")

        token = self.tknz.get_token()

        if token == "if":

            self.compile_if_statements()
        
        elif token == "while":

            self.compile_while_statements()
        
        elif token == "let":

            self.compile_let_statements()

        elif token == "class":

            self.compile_class_statements()

        print("</statements>")


    def compile_class_statements(self):

        print("<classStatement>")

        self.print_line()
        
        self.tknz.advance()

        self.print_line()

        self.tknz.advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.print_line()
        
        self.tknz.advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.print_line()
        
        print("</classStatement>")  
    

    def compile_if_statements(self):

        print("<ifStatement>")

        self.print_line()

        self.tknz.advance()

        if self.tknz.get_token() != "(":
            raise Exception("Expected '('")

        self.print_line()
        
        self.tknz.advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ")":
            raise Exception("Expected ')'")

        self.print_line()
        
        self.tknz.advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.print_line()
        
        self.tknz.advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.print_line()
        
        print("</ifStatement>")
    

    def compile_while_statements(self):

        print("<whileStatement>")

        self.print_line()

        self.tknz.advance()

        if self.tknz.get_token() != "(":
            raise Exception("Expected '('")

        self.print_line()
        
        self.tknz.advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ")":
            raise Exception("Expected ')'")

        self.print_line()
        
        self.tknz.advance()

        if self.tknz.get_token() != "{":
            raise Exception("Expected '{'")

        self.print_line()
        
        self.tknz.advance()

        self.compile_statements()

        if self.tknz.get_token() != "}":
            raise Exception("Expected '}'")

        self.print_line()
        
        print("</whileStatement>")


    def compile_let_statements(self):

        print("<letStatement>")

        self.print_line()

        self.tknz.advance()

        self.print_line()
        
        self.tknz.advance()

        if self.tknz.get_token() != "=":
            raise Exception("Expected '='")

        self.print_line()

        self.tknz.advance()

        self.compile_expression()

        self.tknz.advance()

        if self.tknz.get_token() != ";":
            raise Exception("Expected ';'")

        self.print_line()

        self.tknz.advance()

        print("</letStatement>")


    def compile_expression(self):

        print("<expression>")

        self.compile_term()

        self.tknz.advance()

        token = self.tknz.get_token()

        if token in OP_TERMS:

            self.compile_op()

            self.tknz.advance()
        
            self.compile_term()
        
        print("</expression>")


    def compile_term(self):

        print("<term>")

        self.print_line()

        print("</term>")


    def compile_var_name(self):
        pass


    def compile_constant(self):
        pass


    def compile_op(self):
        
        self.print_line()

    
    def print_line(self):

        token = self.tknz.get_token()
        token_tye = self.tknz.token_tye()

        print(f"<{token_tye}> {token} </{token_tye}>")


    def run(self):
        
        self.compile_statements()


if __name__ == "__main__":

    from JackTokenizer import *

    tknz = JackTokenizer("test2.jack")
    tknz.export_xml()
    tknz.advance()


    ce = CompilationEngine(tknz)

    ce.run()
