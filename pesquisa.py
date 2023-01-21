from tkinter import *
from tkinter import ttk
from tkinter import messagebox
""" from tkcalendar import Calendar """
from datetime import date
from main import *


# Calendário
current_date = date.today()
ano = current_date.year
mes = current_date.month
dia = current_date.day

""" calendar = Calendar(window.panel_1, selectmode = 'day',year =ano, month = mes,day = dia, locale='pt_br')
calendar.place(x=170, y=20)
calendar.selection_clear()
  """
def grad_date():
    lbl_date.config(text = "Dia selecionado: " + calendar.get_date())


def limpar():
    nome_entry.delete(0, END)
    calendar.selection_clear()
    lbl_date.config(text = "")
    categorias.set("")
    estados.set("")
    


def filtrar():
    lista_tarefas.delete(*lista_tarefas.get_children())
    f = open("tarefas.txt", "r", encoding="utf-8")
    tarefas = f.readlines()
    f.close()
    tar = 0
    for i in range (len(tarefas)):
        campos = tarefas[i].split(";")
        if nome_entry.get().upper() == campos[0].upper() or nome_entry.get() == "":
            if calendar.get_date() == (campos[1].replace("-", "/")) or calendar.get_date() == "":
                if campos[2] in categorias.get() or categorias.get() == "": 
                    if estados.get() in campos[3] or estados.get() == "":
                        lista_tarefas.insert("", "end", values=(campos[0],campos[1], campos[2], campos[3]))
                        tar += 1
    if tar == 0:
        messagebox.showerror(title="Erro!", message="Não há tarefas com este filtro!")
    if nome_entry.get() == "":
        if calendar.get_date() == "":
            if categorias.get() == "":
                if estados.get() == "":
                    messagebox.showinfo(title="Sem filtro", message="Nenhum filtro foi aplicado!")


    limpar()


