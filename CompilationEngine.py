from os import write
from os.path import exists
from JackTokenizer import *
import VMWriter 
import SymbolTable
from token import *

OP_TERMS = ['+', '-', '*', '/', '&amp', '|', '&lt', '&gt', '=']

class CompilationEngine:


    def __init__(self, file_name):
        self.file_name = file_name.split("/")[-1].replace(".jack", "")
        self.tknz = JackTokenizer(self.file_name)
        self.current_token = self.tknz.current_token
        self.peek_token = self.tknz.current_token
        self.vm = VMWriter.VMWriter(self.file_name)
        self.st = SymbolTable.SymbolTable()
        self.if_label_num = 0
        self.while_label_num = 0
        self.class_name = ""
        self.begin = True


    def compile(self):

        self.compile_class()
    

    def compile_class(self):

        self.expect_peek(TOKEN_CLASS)

        self.expect_peek(TOKEN_IDENT, token_class=True)
        self.class_name = self.current_token["token"]

        self.expect_peek("{")

        while (self.peek_token_is(TOKEN_STATIC) or self.peek_token_is(TOKEN_FIELD)):
    
            self.compile_class_var_dec()
    

        while (self.peek_token_is(TOKEN_FUNCTION) or self.peek_token_is(TOKEN_CONSTRUCTOR) or self.peek_token_is(TOKEN_METHOD)):
        
            self.compile_subroutine()
    

        self.expect_peek("}")


    def compile_class_var_dec(self):

        if self.peek_token_is(TOKEN_FIELD):
            self.expect_peek(TOKEN_FIELD)
            scope = SymbolTable.FIELD
	    
        else:
            self.expect_peek(TOKEN_STATIC)
            scope = SymbolTable.STATIC
        
        self.compile_type()

        token_type = self.current_token["token"]

        self.expect_peek(TOKEN_IDENT, token_class=True)

        name = self.current_token["token"]

        self.st.define(name, token_type, scope)

        while self.peek_token_is(","):

            self.expect_peek(",")
            self.expect_peek(TOKEN_IDENT, token_class=True)

            name = self.current_token["token"]
            self.st.define(name, token_type, scope)

        self.expect_peek(";")

    
    def compile_subroutine(self):

        self.st.start_subroutine()
        self.ifLabelNum = 0
        self.while_label_num = 0

        if self.peek_token_is(TOKEN_CONSTRUCTOR):
            self.expect_peek(TOKEN_CONSTRUCTOR)

        elif self.peek_token_is(TOKEN_FUNCTION):
            self.expect_peek(TOKEN_FUNCTION)

        else:
            self.expect_peek(TOKEN_METHOD)
            self.st.define("this", self.class_name, SymbolTable.ARG)

        subroutine_type = self.current_token["token"]

        if self.peek_token_is(TOKEN_VOID):
            self.expect_peek(TOKEN_VOID)

        else:
            self.compile_type()
        
        self.expect_peek(TOKEN_IDENT, token_class=True)

        function_name = self.class_name + "." + self.current_token["token"]

        self.expect_peek("(")

        if not self.peek_token_is(")"):
            self.compile_parameter_list()
        
        self.expect_peek(")")

        self.compile_subroutine_body(function_name, subroutine_type)


    def compile_subroutine_body(self, function_name, subroutine_type):

        self.expect_peek("{")

        while self.peek_token_is(TOKEN_VAR):
            self.compile_var_dec()

        n_locals = self.st.var_count(SymbolTable.VAR)

        self.vm.write_function(function_name, n_locals)

        if subroutine_type == TOKEN_CONSTRUCTOR:
            self.vm.write_push(VMWriter.CONST, self.st.VarCount(SymbolTable.FIELD))
            self.vm.write_call("Memory.alloc", 1)
            self.vm.write_pop(VMWriter.POINTER, 0)

        elif subroutine_type == TOKEN_METHOD:
            self.vm.write_push(VMWriter.ARG, 0)
            self.vm.write_pop(VMWriter.POINTER, 0)
        
        self.compile_statements()

        self.expect_peek("}")


    def compile_subroutine_call(self):

        ident = self.current_token["token"]
        num_args = 0
        if self.peek_token_is("("):
            self.expect_peek("(")
            self.vm.write_push(VMWriter.POINTER, 0)
            num_args = self.compile_expression_list()

            self.expect_peek(")")

            ident = self.class_name + "." + ident
            num_args += 1
            self.vm.write_call(ident, num_args)

        else:
            self.expect_peek(".")
            sym, has = self.st.lookup(ident)

            if has:
                self.vm.write_push(self.scope_to_segment(sym["scope"]), sym["index"])
                self.expect_peek(TOKEN_IDENT, token_class=True)
                ident = sym["type"] + "." + self.current_token["token"]
                self.expect_peek("(")

                num_args = self.compile_expression_list()
                num_args += 1
            else:
                self.expect_peek(TOKEN_IDENT, token_class=True)
                ident = ident + "." + self.current_token["token"]
                self.expect_peek("(")

                num_args = self.compile_expression_list()

            self.expect_peek(")")
            self.vm.write_call(ident, num_args)


    def compile_var_dec(self):

        self.expect_peek(TOKEN_VAR)

        scope = SymbolTable.VAR

        self.compile_type()

        token_type = self.current_token["token"]

        self.expect_peek(TOKEN_IDENT, token_class=True)

        name = self.current_token["token"]

        self.st.define(name, token_type, scope)

        while self.peek_token_is(","):
            self.expect_peek(",")

            self.expect_peek(TOKEN_IDENT, token_class=True)
            name = self.current_token["token"]

            self.st.define(name, token_type, scope)
        
        self.expect_peek(";")


    def compile_parameter_list(self):

        scope = SymbolTable.ARG

        self.compile_type()
        token_type = self.current_token["token"]

        self.expect_peek(TOKEN_IDENT, token_class=True)
        name = self.current_token["token"]

        self.st.define(name, token_type, scope)

        while self.peek_token_is(","):
            self.expect_peek(",")

            self.compile_type()
            token_type = self.current_token["token"]

            self.expect_peek(TOKEN_IDENT, token_class=True)

            name = self.current_token["token"]
            self.st.define(name, token_type, scope)


    def compile_type(self):

        if self.peek_token["token"] == TOKEN_INT:
            self.expect_peek(TOKEN_INT)

        elif self.peek_token["token"] == TOKEN_CHAR:
            self.expect_peek(TOKEN_CHAR)

        elif self.peek_token["token"] == TOKEN_BOOLEAN:
            self.expect_peek(TOKEN_BOOLEAN)

        elif self.peek_token["token_class"] == TOKEN_IDENT:
            self.expect_peek(TOKEN_IDENT, token_class=True)


    def compile_expression_list(self):

        num_args = 0

        if not self.peek_token_is(")"):
            self.compile_expression()
            num_args += 1

        while self.peek_token_is(","):

            self.expect_peek(",")

            self.compile_expression()
            num_args += 1
        
        return num_args


    def compile_keyword_const(self, k):

        if k == TOKEN_TRUE:
            self.expect_peek(TOKEN_TRUE)
            self.vm.write_push(VMWriter.CONST, 0)
            self.vm.write_arithmetic(VMWriter.NOT)
        
        elif k == TOKEN_FALSE or k == TOKEN_NULL:
            self.next_token()
            self.vm.write_push(VMWriter.CONST, 0)

        elif k == TOKEN_THIS:
            self.expect_peek(TOKEN_THIS)
            self.vm.write_push(VMWriter.POINTER, 0)


    def compile_statements(self):

        self.compile_statement()

    def compile_statement(self):

        self.write_xml_line("<statements>")

        token = self.peek_token["token"]

        if token == "if":

            self.compile_if()
            self.compile_statement()
        
        elif token == "while":

            self.compile_while()
            self.compile_statement()
        
        elif token == "let":

            self.compile_let()
            self.compile_statement()
        
        elif token == "do":

            self.compile_do()
            self.compile_statement()

        elif token == "class":

            self.compile_class()
            self.compile_statement()
        
        elif token == "return":

            self.compile_return()
            self.compile_statement()
        
        elif token == "EOF":
            pass

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
    

    def compile_if(self):

        self.write_xml_line("<ifStatement>")

        label_true = f"IF_TRUE{self.if_label_num}"
        label_false = f"IF_FALSE{self.if_label_num}"
        label_end = f"IF_END{self.if_label_num}"
        self.if_label_num += 1

        self.expect_peek(TOKEN_IF)
        self.expect_peek("(")
        self.compile_expression()
        self.expect_peek(")")

        self.vm.write_if(label_true)
        self.vm.write_goto(label_false)
        self.vm.write_label(label_true)

        self.expect_peek("{")

        self.compile_statements()

        self.expect_peek("}")

        if self.peek_token_is(TOKEN_ELSE):
            self.vm.write_goto(label_end)
        

        self.vm.write_label(label_false)

        if self.peek_token_is(TOKEN_ELSE):
            self.expect_peek(TOKEN_ELSE)

            self.expect_peek("{")

            self.compile_statements()

            self.expect_peek("}")
            self.vm.write_label(label_end)
        
        self.write_xml_line("</ifStatement>")
    

    def compile_while(self):

        self.write_xml_line("<whileStatement>")

        label_while_exp = f"WHILE_EXP{self.while_label_num}"
        label_while_end = f"WHILE_END{self.while_label_num}"
        self.while_label_num += 1

        self.vm.write_label(label_while_exp)
        self.expect_peek(TOKEN_WHILE)

        self.expect_peek("(")

        self.compile_expression()
        self.vm.write_arithmetic(VMWriter.NOT)
        self.vm.write_if(label_while_end)

        self.expect_peek(")")

        self.expect_peek("{")

        self.compile_statements()

        self.vm.write_goto(label_while_exp)
        self.vm.write_label(label_while_end)

        self.expect_peek("}")
        
        self.write_xml_line("</whileStatement>")


    def compile_let(self):

        self.write_xml_line("<letStatement>")

        isArray = False

        self.expect_peek(TOKEN_LET)

        self.expect_peek(TOKEN_IDENT, token_class=True)

        var_name = self.current_token["token"]
        sym = self.st.resolve(var_name)

        if self.peek_token_is("["):
            self.expect_peek("[")

            self.compile_expression()
            self.vm.write_push(self.scope_to_segment(sym["scope"]), sym["index"])

            self.vm.write_arithmetic(VMWriter.ADD)
            self.expect_peek("]")
            isArray = True
        

        self.expect_peek("=")

        self.compile_expression()

        if isArray:
            self.vm.write_pop(VMWriter.TEMP, 0)
            self.vm.write_pop(VMWriter.POINTER, 1)
            self.vm.write_push(VMWriter.TEMP, 0)
            self.vm.write_pop(VMWriter.THAT, 0)
        else:
            self.vm.write_pop(self.scope_to_segment(sym["scope"]), sym["index"])
    

        self.expect_peek(";")

        self.write_xml_line("</letStatement>")


    def compile_do(self):

        self.expect_peek(TOKEN_DO)

        self.expect_peek(TOKEN_IDENT, token_class=True)

        self.compile_subroutine_call()
        self.expect_peek(";")
        self.vm.write_pop(VMWriter.TEMP, 0)


    def compile_expression(self):

        self.write_xml_line("<expression>")

        self.compile_term()

        while (not self.peek_token_is(TOKEN_EOF)) and (self.peek_token["token"] in OP_TERMS):

            self.next_token()

            op = self.current_token["token"]

            self.compile_term()

            self.compile_operators(op)

        
        self.write_xml_line("</expression>")


    def compile_term(self):

        self.write_xml_line("<term>")

        self.compile_factor()

        # while not self.peek_token_is(TOKEN_EOF) and (p)

        # self.engine_advance(token_advance=False)

        self.write_xml_line("</term>")


    def compile_factor(self):

        token = self.peek_token

        if token["token_class"] == "integer":
            self.next_token()
            self.vm.write_push(VMWriter.CONST, token["token"])

        elif token["token"] == TOKEN_TRUE or token["token"] == TOKEN_FALSE or token["token"] == TOKEN_NULL or token["token"] == TOKEN_THIS:
            self.compile_keyword_const(self.peek_token["token"])

        elif token["token_class"] == "string":

            self.expect_peek("string", token_class=True)

            string = self.current_token["token"]
            self.vm.write_push(VMWriter.CONST, len(string))
            self.vm.write_call("String.new", 1)

            for i in range(len(string)):
                self.vm.write_push(VMWriter.CONST, ord(string[i]))
                self.vm.write_call("String.appendChar", 2)

        elif token["token_class"] == TOKEN_IDENT:

            self.expect_peek(TOKEN_IDENT, token_class=True)
            identifier_name = self.current_token["token"]

            if self.peek_token["token"] == "[":
                self.expect_peek("[")

                self.compile_expression()

                sym = self.st.resolve(identifier_name)
                self.vm.write_push(self.scope_to_segment(sym["scope"]), sym["index"])
                self.vm.write_arithmetic(VMWriter.ADD)

                self.expect_peek("]")
                self.vm.write_pop(VMWriter.POINTER, 1)
                self.vm.write_push(VMWriter.THAT, 0)

            elif self.peek_token["token"] == "(" or self.peek_token["token"] == TOKEN_DOT:
                self.compile_subroutine_call()

            else: 
                sym = self.st.resolve(identifier_name)
                self.vm.write_push(self.scope_to_segment(sym["scope"]), sym["index"])

        elif token["token"] == "(":
            self.expect_peek("(")

            self.compile_expression()

            self.expect_peek(")")
        
        elif token["token"] == TOKEN_MINUS or token["token"] == TOKEN_NOT:

            self.next_token()
            op = self.current_token["token"]

            self.compile_term()
            if op == TOKEN_MINUS:
                self.vm.write_arithmetic(VMWriter.NEG)
            else:
                self.vm.write_arithmetic(VMWriter.NOT)

        else:
            raise Exception("Operador não reconhecido: ", token["token"])


    def compile_var_name(self):
        pass


    def compile_constant(self):
        pass


    def compile_operators(self, op):
        
        if op == TOKEN_PLUS:
            self.vm.write_arithmetic(VMWriter.ADD)
        elif op == TOKEN_MINUS:
            self.vm.write_arithmetic(VMWriter.SUB)
        elif op == TOKEN_ASTERISK:
            self.vm.write_call("Math.multiply", 2)
        elif op == TOKEN_SLASH:
            self.vm.write_call("Math.divide", 2)
        elif op == TOKEN_AND:
            self.vm.write_arithmetic(VMWriter.AND)
        elif op == TOKEN_OR:
            self.vm.write_arithmetic(VMWriter.OR)
        elif op == TOKEN_LT:
            self.vm.write_arithmetic(VMWriter.LT)
        elif op == TOKEN_GT:
            self.vm.write_arithmetic(VMWriter.GT)
        elif op == TOKEN_EQ:
            self.vm.write_arithmetic(VMWriter.EQ)
        elif op == TOKEN_NOT:
            self.vm.write_arithmetic(VMWriter.NOT)

    
    def compile_return(self):

        self.expect_peek(TOKEN_RETURN)

        if not self.peek_token_is(";"):
            self.compile_expression()
            self.vm.write_return()
        else:
            self.vm.write_push(VMWriter.CONST, 0)
            self.vm.write_return()
        

        self.expect_peek(";")


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
          

    # def engine_advance(self, token_advance=True):

    #     token = self.tknz.get_token()
    #     token_tye = self.tknz.token_tye()

    #     line = f'<{token_tye}> {token} </{token_tye}>'

    #     self.write_xml_line(line)

    #     if token_advance:

    #         self.tknz.advance()


    def scope_to_segment(self, scope):

        if scope == SymbolTable.STATIC:
            return VMWriter.STATIC
        elif scope == SymbolTable.FIELD:
            return VMWriter.THIS
        elif scope == SymbolTable.VAR:
            return VMWriter.LOCAL
        elif scope == SymbolTable.ARG:
            return VMWriter.ARG
        else:
            raise Exception("Escopo indefinido")


    def next_token(self):
        self.current_token = self.peek_token
        try:
            self.tknz.advance()
            self.peek_token = self.tknz.current_token
        except:
            self.peek_token = {
                "token": "EOF",
                "token_class": "keyword"
            }


    def expect_peek(self, token_type, token_class=False):

        # print(self.peek_token)

        if token_class:

            if self.peek_token["token_class"] == token_type:

                self.next_token()

            else:
                self.peek_error(self.peek_token["start"], token_type, self.peek_token["token_class"])
        else:

            if self.peek_token["token"] == token_type:

                self.next_token()

            else:
                self.peek_error(self.peek_token["start"], token_type, self.peek_token["token"])


    def peek_token_is(self, token):
        return self.peek_token["token"] == token


    def peek_error(self, line, expected, real):

        raise Exception(f"{line}: expected next token to be {expected}, got {real} instead")

    def print_table(self, table):

        for key in table.keys():
            print("------------------")
            print("Name: ", table[key]["name"])
            print("Type: ", table[key]["type"])
            print("Scope: ", table[key]["scope"])
            print("Index: ", table[key]["index"])


    def run(self):

        self.tknz.export_xml()

        self.tknz.advance()
        
        self.compile()

        print("*** SYMBOL TABLE ***\n")
        print("Class Scope:")
        self.print_table(self.st.classScope)
        print("\n")
        print("Subroutine Scope:")
        self.print_table(self.st.subRoutineScope)
        
