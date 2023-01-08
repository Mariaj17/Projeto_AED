from tkinter import *
import os
from tkinter import messagebox

pasta='files'
fTarefas ='files/tarefas.txt'

listaTree=[[]]

if not os.path.exists(pasta):
    os.mkdir(pasta)
f=open(fTarefas, "a", encoding="utf-8")
f.close()

def inserirTarefa(tarefa, data, categoria, estadoTarefa, lstTarefas):
    fileTarefa=open(fTarefas, "a", encoding="utf-8")
    linha = tarefa + ";" + data + ";" + categoria + ";" + estadoTarefa + "\n" 
    fileTarefa.write(linha)
    fileTarefa.close()
    
    lista = lerTarefas()
    refreshListboxTarefas(lista, lstTarefas)

def lerTarefas():
    fileTarefas=open(fTarefas, "r", encoding="utf-8")
    lista = fileTarefas.readlines()
    fileTarefas.close()
    return lista

def refreshListboxTarefas(listaTarefas, lstTarefas):
    lstTarefas.delete(0, END)
    for item in listaTarefas:
        item = item.replace(";", "  ")
        lstTarefas.insert(END, item)