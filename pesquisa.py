from tkinter import *
from tkinter import ttk
from tkinter import messagebox
""" from tkcalendar import Calendar """
from datetime import date

window = Tk()
window.geometry=("1000x600")
window.title("Pesquisa")
window.configure(background="#1e3743")
window.resizable(True, True)
window.maxsize(width=1100, height=700)
window.minsize(width=1000, height=600)

# Pained window
window.panel_1 = PanedWindow(window)
window.panel_1.place(x=10 , y=10, width=980, height=230)
window.panel_2 = PanedWindow(window)
window.panel_2.place(x=10, y=250, width=980, height=340)

# Labels
lbl_filtro = Label(window.panel_1, text="Data: ", font=('Verdana', 10))
lbl_filtro.place(x=20, y=20)


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

# Button e Label get data
btn_getDate = Button(window.panel_1, text = "Ver dia selecionado", font=("Verdana", 9),command = grad_date)
btn_getDate.place(x=20, y= 50)
 
lbl_date = Label(window.panel_1, text = "", font = ("Verdana", 7))
lbl_date.place(x=10, y=90)

# Nome
lbl_nome = Label(window.panel_1, text="Nome: ", font = ("Verdana",10))
lbl_nome.place(x=450, y=20)

nome_entry = Entry(window.panel_1)
nome_entry.place(x=450, y=50, width=350, height=20)

# Categoria
lbl_categ = Label(window.panel_1, text="Categoria: ", font = ("Verdana", 10))
lbl_categ.place(x=450, y=80)

f = open("files\category.txt", "r", encoding="utf-8")
categ = f.readlines()
f.close()
categorias = ttk.Combobox(window.panel_1, values=categ, state="readonly")
categorias.place(x = 450, y = 110)

# Estado
lbl_estado = Label(window.panel_1, text="Estado: ", font = ("Verdana", 10))
lbl_estado.place(x=650, y= 80)

est = ['Feito', 'Por fazer', 'Fazendo']
estados = ttk.Combobox(window.panel_1, values=est, state="readonly")
estados.place(x = 650, y = 110)

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

    
            

# Button limpar
btn_limpar = Button(window.panel_1, text="Limpar", font=("Verdana", 10), command=limpar)
btn_limpar.place(x=515, y=160, width=80, height=50)

# Button filtrar
btn_filtrar = Button(window.panel_1, text="Filtrar", font=("Verdana", 10), command=filtrar)
btn_filtrar.place(x=630, y=160, width=80, height=50)

# Treeview
lista_tarefas = ttk.Treeview(window.panel_2, height=14, column=("col1", "col2", "col3", "col4"))
lista_tarefas.heading("#0", text="")
lista_tarefas.heading("#1", text="Nome")
lista_tarefas.heading("#2", text="Data")
lista_tarefas.heading("#3", text="Categoria")
lista_tarefas.heading("#4", text="Estado")

lista_tarefas.column("#0", width=1)
lista_tarefas.column("#1", width=400)
lista_tarefas.column("#2", width=180)
lista_tarefas.column("#3", width=180)
lista_tarefas.column("#4", width=180)

lista_tarefas.place(x=15, y=15)

window.mainloop()
