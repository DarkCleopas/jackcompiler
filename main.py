from JackTokenizer import *
from CompilationEngine import *

tknz = JackTokenizer("test2.jack")
tknz.export_xml()
tknz.advance()

ce = CompilationEngine(tknz)
ce.run()