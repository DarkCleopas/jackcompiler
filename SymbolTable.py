STATIC = "STATIC"
FIELD  = "FIELD"
ARG    = "ARG"
VAR    = "VAR"


Symbol = {
    "name": "",
    "type": "",
    "scope": "",
    "index": ""
}        


class SymbolTable:

    def __init__(self):

        self.classScope = {}
        self.subRoutineScope = {}
        self.numDefinitions = {
            "STATIC":   0,
            "FIELD":    0,
            "ARG":      0,
            "VAR":      0
        }

    def lookup(self, name):

        has_sub = self.has_sub(name)
        
        if has_sub:
            sym = self.subRoutineScope[name]
            return sym, has_sub
        else:
            has_class = self.has_class(name)
            if has_class:
                sym = self.classScope[name]
                return sym, has_class
            else:
                return "", has_class
	

    def has_sub(self, name):
        return name in self.subRoutineScope
    
    def has_class(self, name):
        return name in self.classScope

    def resolve(self, name):
        sym, has_defined = self.lookup(name)

        if not has_defined:
            raise Exception(f"Identificador '{name}' não está definido\n")
        
        return sym

    def start_subroutine(self):

        self.subRoutineScope = {}
        self.numDefinitions["ARG"] = 0
        self.numDefinitions["VAR"] = 0

    def define(self, name, ttype, scope):

        if scope == STATIC or scope == FIELD:
            symbol = {"name": name, "type": ttype, "scope": scope, "index": self.numDefinitions[scope]}
            self.classScope[name] = symbol
        else:
            symbol = {"name": name, "type": ttype, "scope": scope, "index": self.numDefinitions[scope]}
            self.subRoutineScope[name] = symbol

        self.numDefinitions[scope] += 1

        # print(self.classScope)
        # print(self.subRoutineScope)
        # print("\n")

    def var_count(self, scope):
        return self.numDefinitions[scope]


if __name__ == "__main__":

    st = SymbolTable()
    print(st.numDefinitions)