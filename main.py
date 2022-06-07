import sys
from syntactic import Syntactic
from lexical import get_token

if sys.argv[1]:
    input_file = sys.argv[1]
else:
    raise Exception

file = open(input_file, 'r')
line = 1
pos = 0

syntactic = Syntactic(file)
syntactic.syntactic()
