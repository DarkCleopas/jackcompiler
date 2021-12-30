from os.path import exists

# Command
ADD  = "add"
SUB = "sub"
NEG = "neg"
EQ  = "eq"
GT  = "gt"
LT  = "lt"
AND = "and"
OR  = "or"
NOT = "not"

# Segment
STATIC  = "static"
ARG     = "argument"
LOCAL   = "local"
CONST   = "constant"
THIS    = "this"
THAT    = "that"
POINTER = "pointer"
TEMP    = "temp"


class VMWriter:

    def __init__(self, file_name):

        self.file_name = f"{file_name}.vm"

        with open(self.file_name, "w") as f:
            f.write("")



    def write_push(self, segment, index):

        s = f"push {segment} {index}\n"
        self.write_file(s)


    def write_pop(self, segment, index):

        s = f"pop {segment} {index}\n"
        self.write_file(s)


    def write_arithmetic(self, command):

        s = f"{command}\n"
        self.write_file(s)


    def write_call(self, name, n_args):

        s = f"call {name} {n_args}\n"
        self.write_file(s)
    

    def write_function(self, name, n_locals):

        s = f"function {name} {n_locals}\n"
        self.write_file(s)


    def write_return(self):

        s = f"return\n"
        self.write_file(s)

    
    def write_label(self, label):

        s = f"label {label}\n"
        self.write_file(s)


    def write_goto(self, label):

        s = f"goto {label}\n"
        self.write_file(s)


    def write_if(self, label):

        s = f"if-goto {label}\n"
        self.write_file(s)


    def write_file(self, s):

        with open(self.file_name, "a") as f:
            f.write(s)
