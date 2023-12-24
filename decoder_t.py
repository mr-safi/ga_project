import urllib.parse
import pandas as pd
from htmlparser import *
df = pd.read_csv('xssed.csv')
list_p = []
for index, row in df.iterrows():
    payload= row[0]
    p=urllib.parse.unquote(payload)
    # print(len(p))
    list_p.append(p)

print("----- number of all payload: ",len(list_p))

for i in range(53,59):
    lex = Lexer(list_p[i])
    lex.tokenise()
    toktype = lex.get_tokens_type()
    tokValue = lex.get_tokens_value()
    print(list_p[i])
    print(toktype)
    print(tokValue)
    print("--------------------------------------")

# # lex = Lexer('<script > alert(1) </script>')
# lex.tokenise()
# toktype = lex.get_tokens_type()
# tokValue = lex.get_tokens_value()

# print(toktype)
# print(tokValue)