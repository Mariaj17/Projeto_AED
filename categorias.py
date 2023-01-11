import os

def createDropCategory():
    options.clear()

    f=open(fcategoria, "r", encoding="utf-8")
    ficha=f.readlines()
    f.close()

    for linha in ficha:
        options.append(linha)

def insesirCategoria():
    f=open(fcategoria, "r", encoding="utf-8")
    ficha=f.readlines()
    f.close()

pasta='files'
fcategoria ='files/categorias.txt'

if not os.path.exists(pasta):
    os.mkdir(pasta)
f=open(fcategoria, "a", encoding="utf-8")
f.close()

# Dropdown Categorisas
options = []
