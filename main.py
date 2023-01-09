from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
from PIL import ImageTk,Image
import os
from users import *
import utils
from tarefas import *
from categorias import *

global window
window=Tk()
window.title('ToDoList')

global screenHeight
global screenWidth
global appHeight, appWidth
global x, y



#-----------------------------------Functions-----------------------------#

    #caso um utilizador logado desligue a pagina de forma forçada a aplicação ao inicializar vai colocar como falso o login de todos os users 
def init():
    try:
        with open("Files/users.txt", "r") as file:
            users = file.readlines()
            for i in range(len(users)):
                user = users[i]
                users[i] = user.replace(user.split(";")[4], "False")
        with open("Files/users.txt", "w") as file:
            file.writelines(users)
    except FileNotFoundError:
        with open("Files/users.txt", "w") as file:
            file.write(
                "totalActivities" + ";" +
                "currentActivities" + ";" +
                "admin" + ";" +
                "123" + ";" +
                "False" + ";" +
                "admin@gmail.com" + ";" +
                "admin" + ";" +
                "\n")       
        
init()


def notification(userFile, user):
    with open (userFile, "r") as file:
        lines = file.readlines()
        for line in lines:
            if user in line:
                # newActivities = lines[user].split(";")[6:-1]
                # print(newActivities)
                values = line.strip().split(";")
                try:
                    if int(values[1]) > int(values[0]):
                        newTasksAmount = int(values[1]) - int(values[0])
                        tasksList = values[7:]
                        tasks = " | ".join(tasksList)
                        messagebox.showinfo("New tasks", f"You have {newTasksAmount} new tasks available that were sent while you were offline! Those tasks are... {tasks}")
                except ValueError:
                    pass


def changeButton(text,command):
    btnInciarSessao.config(text=text, command=command)

def logout():
    global username1
    with open("Files/users.txt", "r") as file:
        users = file.readlines()
        for i in range(len(users)):
            if username1 in users[i]:
                index = i

        totalActivities = len(users[index].split(";")[6:-1])
        with open("Files/users.txt", "w") as file:       
            users[index] = users[index].replace(users[index].split(";")[4], "False")
            users[index] = users[index].replace(users[index].split(";")[0], str(totalActivities))
            file.writelines(users)
            if utils.checkUserLogged(username1, users) == True:
                changeButton("Terminar sessão",logout)
            if utils.checkUserLogged(username1, users) == False:
                changeButton("Iniciar Sessões" ,login)
            logoutSucess()
            userLabel.config(text="")



def loggedUser(usernameLogged, index):
    with open("Files/users.txt", "r") as file:
        users = file.readlines()
        for i in range(len(users)):
            if usernameLogged in users[i]:
                index = i
        with open("Files/users.txt", "w") as file:
            users[index] = users[index].replace(users[index].split(";")[4], "True")
            file.writelines(users)
            if utils.checkUserLogged(usernameLogged, users) == True:
                changeButton("Terminar sessão",logout)
            if utils.checkUserLogged(usernameLogged, users) == False:
                changeButton("Iniciar Sessões" ,login)
        userLabel.config(text=usernameLogged)
                  

def loginValidation():
    global username1
    username1 = usernameValidation.get()
    password1 = passwordValidation.get()
    usernameEntry1.delete(0,END)
    passwordEntry1.delete(0,END)

    #List_of_files = os.listdir()

    try:
        with open("Files/users.txt", "r") as file:
            print("FIle exists1")
    except FileNotFoundError:
        with open("Files/users.txt", "w") as file:
            messagebox.showerror("Error 404 file not found!", "The aplication has no users! please create one in the registration page")
            file.write("admin" + ";" + "123" + ";" + "admin@gmail.com" + ";" + "admin" + "\n")
            screen2.destroy()
    else:
        with open("Files/users.txt", "r") as file:
            loginValidation = file.readlines()
            user_found = False
            for user in loginValidation:
                Fields = user.split(";")
                if username1 == Fields[2]:
                    user_found = True
                    if password1 == Fields[3]:
                        screen2.destroy()
                        loginSuccess()
                        loggedUser(username1, Fields[0])  # devolve o nome to utilizador e o index da linha to ficheiro do utilizador
                        print("login done move to page")
                        notification("Files/users.txt", username1)
                        return
                    else:
                        invalidPassword()
            if not user_found:
                userNotFound()


def login():
    global screen2
    global usernameEntry1
    global passwordEntry1
    global usernameValidation
    global passwordValidation
    
    screen2 = Toplevel()
    screen2.title("login")
    screen2.geometry("300x250")
    Label(screen2,text = "Please enter your information").pack()
    Label(screen2,text = "").pack()


    usernameValidation = StringVar()
    passwordValidation = StringVar()

    Label(screen2,text = "Username").pack()
    usernameEntry1 = Entry(screen2, textvariable = usernameValidation)
    usernameEntry1.pack()
    Label(screen2,text = "").pack()
    Label(screen2,text = "Password").pack()
    passwordEntry1 = Entry(screen2, textvariable = passwordValidation,show = "*")
    passwordEntry1.pack()
    Label(screen2,text = "").pack()
    Button(screen2, text = "Login", width = 10, height = 1,command = loginValidation).pack()


def PagTarefas():
    createDropCategory()

    windowTarefas = Toplevel()   # Objeto da classe Toplevel, janela principal
    windowTarefas.title("Criar Tarefas") 
    windowTarefas.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
    windowTarefas.focus_force()     # Força toda a interação com a janela atual (top window)
    windowTarefas.grab_set()
    windowTarefas.config(bg = '#a3d9ff')

    userLabel = Label(windowTarefas, width = 5, height = 2, text = "", fg="black")
    userLabel.place(x= 0, y=0)

    btnInciarSessao = Button(windowTarefas, width = 20, height= 2, text = "Iniciar Sessões", bd=1, fg='white', bg='#006BB8', relief = "raised",command = login)
    btnInciarSessao.place(x=500, y=0)

    btnCriarConta = Button(windowTarefas, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
    btnCriarConta.place(x=650, y=0)

    #Canvas com botões da esquerda
    btnCanvas = Canvas(windowTarefas, width = 205, height = 455, bd = 2, bg='#7e6b8f', relief = "flat")
    btnCanvas.place(x=-5, y=40)

    btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnCriarTaref.place(x=40, y=50)

    btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagPesquisa)
    btnPesquisa.place(x=40, y=150)

    btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnDashboard.place(x=40, y=250)

    btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnGerirCat.place(x=40, y=350)

    #Gerir Tarefas
    lblTarefa = Label(windowTarefas, text = "Tarefa", bg='#a3d9ff')
    lblTarefa.place(x=220, y=70)

    tarefa = StringVar()
    inputTarefa = Entry(windowTarefas, width=25, textvariable=tarefa)
    inputTarefa.place(x=270, y= 70) 

    lblData = Label(windowTarefas, text = "Data", bg='#a3d9ff')
    lblData.place(x=220, y=120)

    data = StringVar()
    entryData = Entry(windowTarefas, width=25, textvariable=data)
    entryData.place(x=270, y= 120) 

    categoria = StringVar()                     
    categoria.set("Estudos")
    dropCategoria = OptionMenu(windowTarefas, categoria ,*options)
    dropCategoria.pack()
    dropCategoria.place(x=230, y= 180)

    lblCategoria = Label(windowTarefas, text = " ")
    lblCategoria.place(x=230, y= 180)
    lblCategoria.pack()

    lblEstado = Label(windowTarefas, text = "Estado:", bg='#a3d9ff')
    lblEstado.place(x=350, y=170)

    estadoTarefa = StringVar()
    estadoTarefa.set("Por fazer")
    rd1 = Radiobutton(windowTarefas, text = "Por fazer", value = "Por fazer", variable= estadoTarefa, bg='#a3d9ff')
    rd2 = Radiobutton(windowTarefas, text = "A fazer", value = "A fazer",     variable= estadoTarefa, bg='#a3d9ff')
    rd3 = Radiobutton(windowTarefas, text = "Feito", value = "Feito",         variable= estadoTarefa, bg='#a3d9ff')
    rd1.place(x= 350, y= 200)
    rd2.place(x= 350, y= 230)
    rd3.place(x= 350, y= 260)

    lstTarefas = Listbox(windowTarefas, width = 50, height=12)
    lstTarefas.place(x= 470, y=70)

    listaTarefas= lerTarefas()
    refreshListboxTarefas(listaTarefas, lstTarefas)

    btnInserir = Button(windowTarefas, text='Inserir', width=10, height=3, bd=1, fg='white', bg='#006BB8', relief = "raised", 
        command= lambda: inserirTarefa(tarefa.get(), data.get(), categoria.get(), estadoTarefa.get(), lstTarefas))
    btnInserir.place(x=510, y= 300)
    
    btnRemover = Button(windowTarefas, text='Remover', width=10, height=3, bd=1, fg='white', bg='#006BB8', relief = "raised", command= removeTarefas)
    btnRemover.place(x=660, y= 300)

    btnEstado = Button(windowTarefas, text='Mudar Estado', width=10, height=3, bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnEstado.place(x=510, y= 400)

    btnAdicionarTarefa = Button(windowTarefas, width = 10, height= 3, text= "Redirecionar", bd=1, fg='white', bg='#006BB8', relief = "raised", command=addTask)
    btnAdicionarTarefa.place(x=660, y=400)

def PagPesquisa():
    createDropCategory()

    windowPesquisa = Toplevel()
    windowPesquisa.title("Criar Tarefas") 
    windowPesquisa.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
    windowPesquisa.focus_force()
    windowPesquisa.grab_set()
    windowPesquisa.config(bg = '#a3d9ff')

    userLabel = Label(windowPesquisa, width = 5, height = 2, text = "", bg='#a3d9ff', fg="black")
    userLabel.place(x= 0, y=0)

    btnInciarSessao = Button(windowPesquisa, width = 20, height= 2, text = "Iniciar Sessões", bd=1,fg='white', bg='#006BB8', relief = "raised",command = login)
    btnInciarSessao.place(x=500, y=0)

    btnCriarConta = Button(windowPesquisa, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
    btnCriarConta.place(x=650, y=0)

    #Canvas com botões da esquerda
    btnCanvas = Canvas(windowPesquisa, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
    btnCanvas.place(x=-5, y=40)

    btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagTarefas)
    btnCriarTaref.place(x=30, y=50)

    btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnPesquisa.place(x=30, y=150)

    btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnDashboard.place(x=30, y=250)

    btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnGerirCat.place(x=30, y=350)

    #Pesquisa
    lblPesquisa = Label(windowPesquisa, text = "Pesquisar por data:", bg='#a3d9ff', fg='black')
    lblPesquisa.place(x=210, y=70)

    pesquisa = StringVar()
    inputPesquisa = Entry(windowPesquisa, width=20, textvariable=pesquisa)
    inputPesquisa.place(x=330, y= 70)

    lblEstado = Label(windowPesquisa, text = "Estado", bg='#a3d9ff')
    lblEstado.place(x=210, y=120)

    estadoTarefa = StringVar()
    estadoTarefa.set("Por fazer")
    rd1 = Radiobutton(windowPesquisa, text = "Por fazer", value = "Por fazer", variable= estadoTarefa, bg='#a3d9ff')
    rd2 = Radiobutton(windowPesquisa, text = "A fazer", value = "A fazer",     variable= estadoTarefa, bg='#a3d9ff')
    rd3 = Radiobutton(windowPesquisa, text = "Feito", value = "Feito",         variable= estadoTarefa, bg='#a3d9ff')
    rd1.place(x= 210, y= 150)
    rd2.place(x= 210, y= 180)
    rd3.place(x= 210, y= 210)

    categoria = StringVar()                     
    categoria.set("Estudo")
    dropCategoria = OptionMenu(windowPesquisa, categoria ,*options)
    dropCategoria.pack()
    dropCategoria.place(x=300, y= 120)

    lblCategoria = Label(windowPesquisa, text = " ")
    lblCategoria.place(x=300, y= 120)
    lblCategoria.pack()

    lstTarefas = Listbox(windowPesquisa, width = 50, height=12)
    lstTarefas.place(x= 470, y=70)

def PagDashboard():
    windowDashboard = Toplevel()
    windowDashboard.title("Criar Tarefas") 
    windowDashboard.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
    windowDashboard.focus_force()
    windowDashboard.grab_set()
    windowDashboard.config(bg = '#a3d9ff')

    userLabel = Label(windowDashboard, width = 5, height = 2, text = "", bg='#a3d9ff', fg="black")
    userLabel.place(x= 0, y=0)

    btnInciarSessao = Button(windowDashboard, width = 20, height= 2, text = "Iniciar Sessões", bd=1,fg='white', bg='#006BB8', relief = "raised",command = login)
    btnInciarSessao.place(x=500, y=0)

    btnCriarConta = Button(windowDashboard, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
    btnCriarConta.place(x=650, y=0)

    #Canvas com botões da esquerda
    btnCanvas = Canvas(windowDashboard, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
    btnCanvas.place(x=-5, y=40)

    btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagTarefas)
    btnCriarTaref.place(x=30, y=50)

    btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnPesquisa.place(x=30, y=150)

    btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnDashboard.place(x=30, y=250)

    btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnGerirCat.place(x=30, y=350)

def PagGerir():
    windowGerir = Toplevel()
    windowGerir.title("Criar Tarefas") 
    windowGerir.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
    windowGerir.focus_force()
    windowGerir.grab_set()
    windowGerir.config(bg = '#a3d9ff')

    userLabel = Label(windowGerir, width = 5, height = 2, text = "", bg='#a3d9ff', fg="black")
    userLabel.place(x= 0, y=0)

    btnInciarSessao = Button(windowGerir, width = 20, height= 2, text = "Iniciar Sessões", bd=1,fg='white', bg='#006BB8', relief = "raised",command = login)
    btnInciarSessao.place(x=500, y=0)

    btnCriarConta = Button(windowGerir, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
    btnCriarConta.place(x=650, y=0)

    #Canvas com botões da esquerda
    btnCanvas = Canvas(windowGerir, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
    btnCanvas.place(x=-5, y=40)

    btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagTarefas)
    btnCriarTaref.place(x=30, y=50)

    btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnPesquisa.place(x=30, y=150)

    btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnDashboard.place(x=30, y=250)

    btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised")
    btnGerirCat.place(x=30, y=350)

#-----------------------------------MainScreen----------------------------#

window.config(bg = '#a3d9ff')
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

appWidth = 800                             
appHeight = 500
x = (screenWidth/2) - (appWidth/2)        
y = (screenHeight/2) - (appHeight/2)
window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))

#img = ImageTk.PhotoImage(Image.open("img\homepage.jpg"))

# #Botões de conta
# btnNotificacao = Button(window, width = 30, height= 30, bd=1, image = imgNot, compound=LEFT, relief = "raised")
# btnNotificacao.place(x=450, y=0)

# MainPage
userLabel = Label(window, width = 5, height = 2, text = "", bg='#a3d9ff', fg="black")
userLabel.place(x= 0, y=0)

btnInciarSessao = Button(window, width = 20, height= 2, text = "Iniciar Sessões", bd=1,fg='white', bg='#006BB8', relief = "raised",command = login)
btnInciarSessao.place(x=500, y=0)

btnCriarConta = Button(window, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
btnCriarConta.place(x=650, y=0)

#Canvas com botões da esquerda
btnCanvas = Canvas(window, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
btnCanvas.place(x=-5, y=40)

btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagTarefas)
btnCriarTaref.place(x=30, y=50)

btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagPesquisa)
btnPesquisa.place(x=30, y=150)

btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagDashboard)
btnDashboard.place(x=30, y=250)

btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised", command=PagGerir)
btnGerirCat.place(x=30, y=350)

ImgCanvas = Canvas(window, width = 600, height = 455, bd=0, bg='#a3d9ff', relief = "flat")
ImgCanvas.place(x=195, y=40)
#ImgCanvas.create_image(10,250, image = img)

window.mainloop()