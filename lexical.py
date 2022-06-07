import re
from util.errors import invalid_token

ARITH_OPERATORS = {
    "regex": re.compile(r"\B(\+|\-|\*|\/|>|<|%)(>|<|\+|-\*)?"),
    "tokens": ["+", "-", "*", "/", ">>", "<<", "%", "--", "++"]
}

LOG_OPERATORS = {
    "regex": re.compile(r"\B(=|<|>|!|&|\|)(=|&|\\|\|)?"),
    "tokens": ["=", "==", ">=", "<=", "!", "!=", "&&", "||", "&", "|"]
}

STRING = {
    "regex": re.compile(r'"[^"]*"')
}

CHAR = {
    "regex": re.compile(r"'((\\['\"\\nrtbfv0])?|([^'\\])?)'")
}

NUMBER = {
    "regex": re.compile(r"\d+(\.\d+)?")
}

SEP = {
    "regex": re.compile(r"(\s|\n|\t)")
}

BLOCK_SEP = {
    "regex": re.compile(r"(\[|]|{|}|\(|\)|;|,)")
}

COMMENT = {
    "regex": re.compile(r"(\/\/.*(\\n)?)|(\/\*[\s\S]*\*\/)")
}

IDENTIFIER = {
    "regex": re.compile(r"\b_?([a-zA-Z])+([a-zA-Z0-9])*")
}

RESERVED_KEYWORDS = ["int", "float", "char", "if", "else", "for", "while"]


def get_token(line, pos, file):
    char = file.read(1)
    pos += 1

    if not char:
        return ['$', "eof", line, pos]
    else:
        if re.search(SEP['regex'], char):
            if char == "\n":
                line += 1
                pos = 0
            return get_token(line, pos, file)
        elif re.search(BLOCK_SEP['regex'], char):
            return [char, "block_sep", line, pos]

        token = char

        while True:
            char = file.read(1)

            if not char:
                file.seek(file.tell() - 1)
                break
            elif re.search(SEP['regex'], char) or re.search(BLOCK_SEP['regex'], char):
                if re.search(COMMENT['regex'], token):
                    if char == "\n":
                        line += 1
                        pos = 0
                else:
                    file.seek(file.tell() - 1)
                    break
            elif re.search(ARITH_OPERATORS['regex'], char) or re.search(LOG_OPERATORS['regex'], char):
                if re.search(IDENTIFIER['regex'], token) or re.search(NUMBER['regex'], token):
                    file.seek(file.tell() - 1)
                    break
                elif re.search(ARITH_OPERATORS['regex'], token) or re.search(LOG_OPERATORS["regex"], token):
                    if len(token) == 2 and token in ARITH_OPERATORS['tokens']:
                        file.seek(file.tell() - 1)
                        break
                    else:
                        arith_flag = True

            token += char
            pos += 1

        if token in RESERVED_KEYWORDS:
            return [token, "rk", line, pos]
        elif re.search(COMMENT['regex'], token):
            return get_token(line, pos, file)
        elif re.search(ARITH_OPERATORS["regex"], token) and token in ARITH_OPERATORS["tokens"]:
            return [token, "arith", line, pos]
        elif re.search(LOG_OPERATORS["regex"], token) and token in LOG_OPERATORS["tokens"]:
            return [token, "log", line, pos]
        elif re.search(STRING["regex"], token):
            return [token, "string", line, pos]
        elif re.search(CHAR["regex"], token):
            return [token, "char", line, pos]
        elif re.search(NUMBER["regex"], token):
            return [token, "number", line, pos]
        elif re.search(IDENTIFIER["regex"], token):
            return [token, "id", line, pos]
        else:
            invalid_token(line, token)
            return [token, "invalid token", line, pos]
