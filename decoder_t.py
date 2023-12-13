import urllib.parse
import pandas as pd

df = pd.read_csv('xssed.csv')

for index, row in df.iterrows():
    payload= row[0]
    p=urllib.parse.unquote(payload)
    print(p)
print("----- number of all payload: ",index)
