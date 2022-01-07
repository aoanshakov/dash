import base64
import pandas as pd
import json as j

def loadUTF8(c):
    if c is not None and ',' in c:
        try:
            x=c.split(',')
            c=x[1]
            c = base64.b64decode(c)
            c=c.decode('utf-8')
        except:
            return ''
        return c
    else:
        return ''

def loadCSV(c,sep=',',decimal='.'):
    if c is not None and ',' in c:
        try:
            x=c.split(',')
            c=x[1]
            c = base64.b64decode(c)
            df=pd.read_csv(io.StringIO(c.decode('utf-8')),sep=sep,decimal=decimal)
        except:
            return pd.DataFrame()
        return df
    else:
        return pd.DataFrame()

def loadJSON(c):
    s=loadUTF8(c)
    d=j.loads(s)
    cont=j.dumps(d,indent=4)
    return d, cont


