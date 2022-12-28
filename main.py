from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
from PIL import ImageTk,Image
import os
from users import *

global window
window=Tk()

global screenHeight
global screenWidth
global appHeight, appWidth
global x, y

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

appWidth = 800                             
appHeight = 500
x = (screenWidth/2) - (appWidth/2)        
y = (screenHeight/2) - (appHeight/2)
window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))

# window.title("ToDoList")
# imgNot = ImageTk.PhotoImage(Image.open("img/notificacao.png"))

# #Botões de conta
# btnNotificacao = Button(window, width = 30, height= 30, bd=1, image = imgNot, compound=LEFT, relief = "raised")
# btnNotificacao.place(x=450, y=0)

btnInciarSessao = Button(window, width = 20, height= 2, text = "Iniciar Sessões", bd=1, fg='black', relief = "raised",command = login)
btnInciarSessao.place(x=500, y=0)

btnCriarConta = Button(window, width = 20, height= 2, text = "Criar Conta", bd=1, fg='black', relief = "raised",command = register)
btnCriarConta.place(x=650, y=0)


window.mainloop()