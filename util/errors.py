from util.term_colors import TermColors


def unexpected_token(line, token):
    print(f"{TermColors.FAIL}Unexpected token '{token}' on line {line}.{TermColors.END_C}")


def unexpected_eof():
    print(f"{TermColors.FAIL}Unexpected end of file.")


def already_declared(line, token):
    print(f"{TermColors.FAIL}Identifier '{token}' already declared on line {line}.{TermColors.END_C}")


def not_declared(line, token):
    print(f"{TermColors.FAIL}Identifier '{token}' on line {line} not declared.{TermColors.END_C}")


def not_initialized(line, token):
    print(f"{TermColors.WARNING}Identifier '{token}' on line {line} not initialized.{TermColors.END_C}")


def invalid_token(line, token):
    print(f"{TermColors.FAIL}Invalid token '{token}' on line {line}.{TermColors.END_C}")