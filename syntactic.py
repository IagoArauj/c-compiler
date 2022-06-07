from lexical import get_token
from util import errors


class Syntactic:
    def __init__(self, file):
        self.file = file
        self.ids = dict()
        self.line = 1
        self.pos = 0

    def check_id(self, identifier):
        if identifier in self.ids.keys():
            if self.ids[identifier]["value"] is not None:
                return 1
            return 0
        return -1

    def create_id(self, identifier, id_type):
        if identifier in self.ids.keys():
            return self.ids[identifier]
        else:
            self.ids[identifier] = {
                "declaredOnLine": self.line, "type": id_type, "initializedOnLine": None, "value": None
            }
            return 0

    def set_val_id(self, identifier, value):
        self.ids[identifier]['initializedOnLine'] = self.line
        self.ids[identifier]['value'] = value

    def get_val_id(self, identifier):
        return self.ids[identifier]['value']

    def expression(self, check_var=True):
        token = get_token(self.line, self.pos, self.file)
        self.line = token[2]
        self.pos = token[3]
        if token[1] in ["number", "id"]:
            if token[1] == "id":
                aux = self.check_id(token[0])
                if aux == 0 and check_var:
                    errors.not_initialized(self.line, token[0])
                elif aux == -1 and check_var:
                    errors.not_declared(self.line, token[0])
            return self.expression2()
        elif token[1] in ["string", "char"]:
            return self.expression2()
        elif token[0] == "(":
            self.expression()
            token = get_token(self.line, self.pos, self.file)
            self.line = token[2]
            self.pos = token[3]
            if token[0] == ")":
                return

            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
            return

        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
        return

    def expression2(self):
        token = get_token(self.line, self.pos, self.file)
        self.line = token[2]
        self.pos = token[3]
        if token[1] == "arith":
            return self.expression()
        elif token[1] == "log" and token[0] != '=':
            return self.expression()
        elif token[0] in [';', ")", "]", "}"]:
            return

        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
        return

    def dec(self, id_type):
        token = get_token(self.line, self.pos, self.file)
        self.line = token[2]
        self.pos = token[3]
        if token[1] == 'id':
            identifier = token[0]
            aux = self.create_id(identifier, id_type)
            if aux != 0:
                errors.already_declared(aux['declaredOnLine'], identifier)

            token = get_token(self.line, self.pos, self.file)
            self.line = token[2]
            self.pos = token[3]
            if token[0] == ";":
                return
            elif token[0] == '=':
                self.expression()
                self.set_val_id(identifier, 0)
                return
            elif token[0] == ',':
                return self.dec(id_type)

        errors.unexpected_token(self.line, token[0])

    def syntactic(self):
        def block2():
            while True:
                token = get_token(self.line, self.pos, self.file)
                self.line = token[2]
                self.pos = token[3]
                # EOF
                if token[0] == "$":
                    errors.unexpected_eof()
                    exit()
                elif token[0] == "}":
                    return
                # declaration
                elif token[0] in ["int", "char", "float"]:
                    self.dec(token[0])
                # attr
                elif token[1] == 'id':
                    identifier = token[0]
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == '=':
                        self.expression()
                        self.set_val_id(identifier, 0)
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                # for loop
                elif token[0] == "for":
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == "(":
                        token = get_token(self.line, self.pos, self.file)
                        self.line = token[2]
                        self.pos = token[3]
                        if token[1] == "id":

                            token = get_token(self.line, self.pos, self.file)
                            self.line = token[2]
                            self.pos = token[3]
                            if token[0] == "=":
                                self.expression(False)
                                # ";" taken in the self.expression before
                                self.expression(False)
                                # ";" taken in the self.expression before
                                token = get_token(self.line, self.pos, self.file)
                                self.line = token[2]
                                self.pos = token[3]
                                if token[1] == "id":
                                    token = get_token(self.line, self.pos, self.file)
                                    self.line = token[2]
                                    self.pos = token[3]
                                    if token[0] == "=":
                                        self.expression()
                                        # ")" taken in the self.expression before
                                        token = get_token(self.line, self.pos, self.file)
                                        self.line = token[2]
                                        self.pos = token[3]
                                        if token[0] == "{":
                                            block2()
                                        else:
                                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                    elif token[0] in ["++", "--"]:
                                        token = get_token(self.line, self.pos, self.file)
                                        self.line = token[2]
                                        self.pos = token[3]
                                        if token[0] == ")":
                                            token = get_token(self.line, self.pos, self.file)
                                            self.line = token[2]
                                            self.pos = token[3]
                                            if token[0] == "{":
                                                block2()
                                            else:
                                                errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                        else:
                                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                    else:
                                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                else:
                                    errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                            else:
                                errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                        else:
                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                elif token[0] == 'if':
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == "(":
                        self.expression()
                        # ")" taken in the self.expression before

                        token = get_token(self.line, self.pos, self.file)
                        self.line = token[2]
                        self.pos = token[3]
                        if token[0] == "{":
                            block2()

                            token = get_token(self.line, self.pos, self.file)
                            self.line = token[2]
                            self.pos = token[3]
                            if token[0] == "else":
                                token = get_token(self.line, self.pos, self.file)
                                self.line = token[2]
                                self.pos = token[3]
                                if token[0] == "{":
                                    block2()
                                else:
                                    errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()

                        else:
                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()

        def block():
            while True:
                token = get_token(self.line, self.pos, self.file)
                self.line = token[2]
                self.pos = token[3]
                # EOF
                if token[0] == "$":
                    exit()
                # declaration
                elif token[0] in ["int", "char", "float"]:
                    self.dec(token[0])
                # attr
                elif token[1] == 'id':
                    identifier = token[0]
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == '=':
                        self.expression()
                        self.set_val_id(identifier, 0)
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                # for loop
                elif token[0] == "for":
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == "(":
                        token = get_token(self.line, self.pos, self.file)
                        self.line = token[2]
                        self.pos = token[3]
                        if token[1] == "id":

                            token = get_token(self.line, self.pos, self.file)
                            self.line = token[2]
                            self.pos = token[3]
                            if token[0] == "=":
                                self.expression(False)
                                # ";" taken in the self.expression before
                                self.expression(False)
                                # ";" taken in the self.expression before
                                token = get_token(self.line, self.pos, self.file)
                                self.line = token[2]
                                self.pos = token[3]
                                if token[1] == "id":
                                    token = get_token(self.line, self.pos, self.file)
                                    self.line = token[2]
                                    self.pos = token[3]
                                    if token[0] == "=":
                                        self.expression()
                                        # ")" taken in the self.expression before
                                        token = get_token(self.line, self.pos, self.file)
                                        self.line = token[2]
                                        self.pos = token[3]
                                        if token[0] == "{":
                                            block2()
                                        else:
                                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                    elif token[0] in ["++", "--"]:
                                        token = get_token(self.line, self.pos, self.file)
                                        self.line = token[2]
                                        self.pos = token[3]
                                        if token[0] == ")":
                                            token = get_token(self.line, self.pos, self.file)
                                            self.line = token[2]
                                            self.pos = token[3]
                                            if token[0] == "{":
                                                block2()
                                            else:
                                                errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                        else:
                                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                    else:
                                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                                else:
                                    errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                            else:
                                errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                        else:
                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                elif token[0] == 'if':
                    token = get_token(self.line, self.pos, self.file)
                    self.line = token[2]
                    self.pos = token[3]
                    if token[0] == "(":
                        self.expression()
                        # ")" taken in the self.expression before

                        token = get_token(self.line, self.pos, self.file)
                        self.line = token[2]
                        self.pos = token[3]
                        if token[0] == "{":
                            block2()

                            token = get_token(self.line, self.pos, self.file)
                            self.line = token[2]
                            self.pos = token[3]
                            if token[0] == "else":
                                token = get_token(self.line, self.pos, self.file)
                                self.line = token[2]
                                self.pos = token[3]
                                if token[0] == "{":
                                    block2()
                                else:
                                    errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                            else:
                                self.file.seek(self.file.tell() - len(token[0]))
                        else:
                            errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
                    else:
                        errors.unexpected_token(self.line, token[0]) if token[0] != "$" else errors.unexpected_eof()
        block()
