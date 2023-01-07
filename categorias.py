import os

def createDropCategory():
    f=open(fcategoria, "r", encoding="utf-8")
    ficha=f.readlines()
    f.close()

    for linha in ficha:
        options.append(linha)

pasta='files'
fcategoria ='files/categorias.txt'

if not os.path.exists(pasta):
    os.mkdir(pasta)
f=open(fcategoria, "a", encoding="utf-8")
f.close()

# Dropdown Categorisas
options = []
