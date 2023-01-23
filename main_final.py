from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
""" from PIL import ImageTk,Image """
import os
""" from users import *
import """
""" from pesquisa import * """
from pip import *
from tkcalendar import Calendar
from datetime import date


global window
window=Tk()
window.title('ToDoList')

global screenHeight
global screenWidth
global appHeight, appWidth
global x, y

global currentUser

global userLabel

currentUser = []
#-----------------------------------Functions-----------------------------#

current_date = date.today()
ano = current_date.year
mes = current_date.month
dia = current_date.day

from tkinter import *
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import re
import os


def register_user():
    try:
        with open("Files/users.txt", "r") as file:
            print("File exists")
    except FileNotFoundError:
        with open("Files/users.txt", "w") as file:

            file.write(
                "0" + ";" +
                "0" + ";" +
                "admin" + ";" +
                "123" + ";" +
                "False" + ";" +
                "admin@gmail.com" + ";" +
                "admin" +
                "\n")

            messagebox.showinfo("Error, file does not exist!", "The file did not exist but we created one for you, try registering now!")
    else:
            if validateReg():
                pass


    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    emailEntry.delete(0,END)
    Label(screen1,text = "Registration Sucess").pack()
    screen1.destroy()


def saveUser():
    usernameInfo = username.get()
    passwordInfo = password.get()
    emailInfo    = email.get()

    with open("Files/users.txt", "a") as file:
        file.write(
                "0" + ";" +
                "0" + ";" +
                usernameInfo + ";" +
                passwordInfo + ";" +
                "False" + ";" +
                emailInfo + ";" +
                "normal" + 
                "\n")
        messagebox.showinfo("Account was successfully!", "Your new account has been created!")
        
def validateReg():

        userRegValidate = username.get()
        passRegValidate = password.get()
        emailRegValidate= email.get()
        validForm = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if len(userRegValidate) < 4:
            messagebox.showerror("Invalid Username!", "Username needs to be at least 4 characters long!")
            username.set("")
            password.set("")
            email.set("")


        if len(passRegValidate) < 6:
            messagebox.showerror("Invalid Password!", "Password should be at least 6 chatacters long!")
            username.set("")
            password.set("")
            email.set("")


        if (re.fullmatch(validForm, emailRegValidate)):
            saveUser()


        else:
            messagebox.showerror("Invalid E-Mail", "Your E-Mail must include the characters '@' and '.'")
            username.set("")
            password.set("")
            email.set("")


def register():
    global screen1
    screen1 = Toplevel()
    screen1.title("Register")
    screen1.geometry("300x250")
    global username
    global password
    global email
    global usernameEntry
    global passwordEntry
    global emailEntry

    username = StringVar()
    password = StringVar()
    email    = StringVar()
    Label(screen1,text="Please enter your information").pack()
    Label(screen1,text="").pack()
    Label(screen1,text="Username *(Min 4 char)").pack()
    usernameEntry = Entry(screen1,textvariable = username)
    usernameEntry.pack()
    Label(screen1,text="Password *(Min 6 char)").pack()
    passwordEntry = Entry(screen1,textvariable = password)

    passwordEntry = Entry(screen1,textvariable = password, show = "*")

    passwordEntry.pack()
    Label(screen1,text="E-mail *(Must include '@' and '.')").pack()
    emailEntry = Entry(screen1,textvariable = email)
    emailEntry.pack()

    Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()



def loginSuccess():
    messagebox.showinfo("Login was successfull!", "your credentials are correct!")

def logoutSucess():
    messagebox.showinfo("Logout was successfull!", "See you later!")

def invalidPassword():
    messagebox.showerror("Invalid password", "Your password is invalid!")

def userNotFound():
    messagebox.showerror("Invalid username", "The username does not exist!")


def taskValidation():
    index = 0
    with open("Files/users.txt", "r") as file:
        userList = file.readlines()
        #Obter o index de uma linha utilizando o username
        for i in range(len(userList)):
            if userChosen.get() in userList[i]:
                index = i
                #verifica as atividades do utilizador no momento em que vai fazer logout. este valor sera depois comparado com o total de atividades de forma a criar a notificação
                currentActivities = len(userList[index].split(";")[5:-1])
                #escrever a nova atividade no fim da linha do utilizador e separar por ";"    
        with open("Files/users.txt", "w") as file:
            line = userList[index].strip().split(";")
            line[1] = str(currentActivities)
            line.append(activityChosen.get())
            userList[index] = ";".join(line) + "\n"
            
            userList[index] = userList[index].replace(userList[index].split(";")[1], str(currentActivities))
            file.writelines(userList)
            messagebox.showinfo("Task sent!", f"The task you selected for {userChosen.get()} will be going their way!")
            screen3.destroy()


def sendTask():
    messageShown = False
    with open("Files/users.txt", "r") as file:
        users = file.readlines()
        for user in users:
            if user.split(";")[4] == "True":
                global screen3
                global userChosen
                global activityChosen

                userChosen = StringVar()
                activityChosen = StringVar()

                screen3 = Toplevel()
                screen3.title("Adicionar tarefa")
                screen3.geometry("300x250")
                Label(screen3,text = "").pack()
                Label(screen3,text = "What user do you want to send an acitivity to?").pack()
                userSelectEntry = Entry(screen3, textvariable = userChosen)
                userSelectEntry.pack()
                Label(screen3,text = "").pack()
                Label(screen3,text="What activity would you like to send?").pack()
                activityEntry = Entry(screen3, textvariable = activityChosen)
                activityEntry.pack()
                Button(screen3,text = "Send activity", width = 10, height = 1,command = taskValidation).pack()   
                messageShown = True          

            if messageShown == False:
                messagebox.showerror("Not logged in!", "You cannot sed a new task to a user if you are not logged in!")
                messageShown = True




#-----------------------------------Functions User -----------------------#
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
                "0" + ";" +
                "0" + ";" +
                "admin" + ";" +
                "123" + ";" +
                "False" + ";" +
                "admin@gmail.com" + ";" +
                "admin" +
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
                        messagebox.showinfo("New tasks", f"Você tem {newTasksAmount} novas tarefas desponiveis que foram entregues enquanto estava offline! Essas tarefas são... {tasks}")
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
            if checkUserLogged(username1, users) == True:
                changeButton("Terminar sessão",logout)
            if checkUserLogged(username1, users) == False:
                changeButton("Iniciar Sessões" ,login)
            logoutSucess()
            currentUser.clear()
            print(currentUser)
            userLabel.config(text="")
            
def checkUserLogged(username, users):
        for user in users:
            if username in user and user.split(";")[4] == "True":
                return True
        return False
          



def loggedUser(usernameLogged, index):
    with open("Files/users.txt", "r") as file:
        users = file.readlines()
        for i in range(len(users)):
            if usernameLogged in users[i]:
                index = i
        with open("Files/users.txt", "w") as file:
            users[index] = users[index].replace(users[index].split(";")[4], "True")
            file.writelines(users)
            if checkUserLogged(usernameLogged, users) == True:
                changeButton("Terminar sessão",logout)
                currentUser.append(usernameLogged)
                currentUser.append(users[index].strip().split(";")[6])
            if checkUserLogged(usernameLogged, users) == False:
                changeButton("Iniciar Sessões" ,login)
        userLabel.config(text=usernameLogged)
                  

def loginValidation():
    global username1
    username1 = usernameValidation.get()
    password1 = passwordValidation.get()
    usernameEntry1.delete(0,END)
    passwordEntry1.delete(0,END)

    try:
        with open("Files/users.txt", "r") as file:
            print("FIle exists1")
    except FileNotFoundError:
        with open("Files/users.txt", "w") as file:
            messagebox.showerror("Error 404 file not found!", "A aplicação não tem utilizadores! Por favor crie uma na pag de registo")
            file.write(
                "0" + ";" +
                "0" + ";" +
                "admin" + ";" +
                "123" + ";" +
                "False" + ";" +
                "admin@gmail.com" + ";" +
                "admin"  +
                "\n")
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
                        print(currentUser)
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
    Label(screen2,text = "Por favor coloque a sua informação").pack()
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


#-----------------------------------Functions tasks -----------------------#
def limpar():
    nome_entry.delete(0, END)
    calendar.selection_clear()
    lbl_date.config(text = "")
    categorias.set("")
    estados.set("")


def limpar2():
    taskName.delete(0, END)
    taskDate.selection_clear()
    taskCategoryDropdown.set("")
    taskEstadoDropdown.set("")


#------------------------------Criar Tarefa--------------------------#
def addTaskElements():
    global taskLabel, taskName, btnSubmitTask, btnAddTask, taskCategoryDropdown, taskEstadoDropdown, taskCategoryLabel, canvasAddTask, btnAlterarTask,btn_getDate,lbl_date, canvasTask, createtaskLabel,treeTaskCreate, taskDate
    try:
        cleanElements()
    except:
        pass
    #Canvas Add Task
    canvasAddTask = Canvas(window,  width = 650, height = 200, bg='#a3d9ff', bd=1, relief = "flat")
    canvasAddTask.place(x=200, y=50)

    lbl_data = Label(canvasAddTask, text="Data: ", bg='#a3d9ff', font=('Verdana', 8))
    lbl_data.place(x=10, y=10)

    taskDate = Calendar(canvasAddTask, selectmode = 'day',year =ano, month = mes,day = dia, locale='pt_br')
    taskDate.place(x=60, y=10)
    taskDate.selection_clear()

    # Nome
    taskLabel = Label(canvasAddTask, text="Nome: ", bg='#a3d9ff', font = ("Verdana",8))
    taskLabel.place(x=315, y=30)

    taskName = Entry(canvasAddTask)
    taskName.place(x=378, y=30)

    # Categoria
    taskCategoryLabel = Label(canvasAddTask, text="Categoria: ", bg='#a3d9ff', font = ("Verdana", 8))
    taskCategoryLabel.place(x=315, y=80)

    f = open("Files\category.txt", "r", encoding="utf-8")
    categ = f.readlines()
    f.close()

    taskCategoryDropdown = ttk.Combobox(canvasAddTask, values=categ, state="readonly")
    taskCategoryDropdown.place(x =378, y = 80)

    # Estado
    taskEstadoLabel = Label(canvasAddTask, text="Estado: ", bg='#a3d9ff', font = ("Verdana", 8))
    taskEstadoLabel.place(x=315, y=130)

    f = open("Files/estados.txt", "r", encoding="utf-8")
    est = f.readlines()
    f.close()

    taskEstadoDropdown = ttk.Combobox(canvasAddTask, values=est, state="readonly")
    taskEstadoDropdown.place(x =378, y = 130)


    # Botões Submeter e Remover
    btnSubmitTask = Button(canvasAddTask, text="Submeter", width = 12, height= 1, font=("Verdana", 10), command=addTask)
    btnSubmitTask.place(x=540,y=20)

    btnAlterarTask = Button(canvasAddTask, text="Alterar", width = 12, height= 1, font=("Verdana", 10), command=alterarDados)
    btnAlterarTask.place(x=540,y=70)

    btnRemoverTask = Button(canvasAddTask, text="Remover", width = 12, height= 1, font=("Verdana", 10), command=remover)
    btnRemoverTask.place(x=540,y=120)

    #Button Enviar Tarefa
    btnAddTask = Button(canvasAddTask, width = 12, height= 1, text = "Enviar Tarefa", font=("Verdana", 10), bd=1, fg='white', bg='#006BB8', relief = "raised",command=sendTask)
    btnAddTask.place(x=540,y=170)

    canvasTask = Canvas(window,  width = 645, height = 300, bg='#a3d9ff', bd=1, relief = "flat")
    canvasTask.place(x=200,y=250)

    treeTaskCreate = ttk.Treeview(canvasTask, height=14, column=("col1", "col2", "col3", "col4"))
    treeTaskCreate.heading("#0", text="")
    treeTaskCreate.heading("#1", text="Nome")
    treeTaskCreate.heading("#2", text="Data")
    treeTaskCreate.heading("#3", text="Categoria")
    treeTaskCreate.heading("#4", text="Estado")

    treeTaskCreate.column("#0", width=0)
    treeTaskCreate.column("#1", width=200)
    treeTaskCreate.column("#2", width=150)
    treeTaskCreate.column("#3", width=150)
    treeTaskCreate.column("#4", width=150)

    treeTaskCreate.place(x=0, y=0)

    f = open("Files/newTask.txt", "r", encoding="utf-8")
    addNewTaskTree = f.readlines()
    f.close()
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    for i in range (len(addNewTaskTree)):
        campos = addNewTaskTree[i].split(";")
        treeTaskCreate.insert("", "end", values=(campos[0],campos[1], campos[2], campos[3]))


def mostrar():
    treeTaskCreate.place(x=0, y=0)
    f = open("Files/newTask.txt", "r", encoding="utf-8")
    addNewTaskTree = f.readlines()
    f.close()
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    for i in range (len(addNewTaskTree)):
        campos = addNewTaskTree[i].split(";")
        treeTaskCreate.insert("", "end", values=(campos[0],campos[1], campos[2], campos[3]))


def addTask():
    if currentUser == []:
        messagebox.showerror("No user is logged in", "Por favor inicie a sessão para adicionar a tarefa.")
        return
    taskValue = taskName.get()
    categoryValue = taskCategoryDropdown.get()
    selectedDate = taskDate.get_date()
    estadoValue = taskEstadoDropdown.get()
    if taskValue == "" or categoryValue == "" or selectedDate == "" or estadoValue == "":
        messagebox.showerror("Preencha tudo!", "Preencha todos os dados da tarefa")
    else:
        newTask = taskValue + ";" + selectedDate + ";" + categoryValue[0:len(categoryValue)-1] + ";" + estadoValue[0:len(estadoValue)-1] + ";" + "\n"
    f = open("Files/newTask.txt", "a", encoding="utf-8")
    f.write(newTask)
    f.close()
    mostrar()
    limpar2()
    
#-----------------------------------pesquisa------------------------------#

def remover():
    taskSelection = treeTaskCreate.selection()[0]
    task = list(treeTaskCreate.item(taskSelection, "values"))
    task_join = task[0] + ";" + task[1] + ";" + task[2] + ";" + task[3] + ";" + "\n"
    print(task_join)

    f = open("Files/newTask.txt", "r+", encoding="utf-8")
    allTasks = f.readlines()
    f.close()
    f = open("Files/newTask.txt", "w", encoding="utf-8")
    for linha in allTasks:
        if task_join != linha:
            f.write(linha)
    f.close()
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    mostrar()
    messagebox.showinfo(title="Feito!", message="Tarefa removida com sucesso!")



def alterarDados():
    global taskValue, selectedDate, categoryValue, estadoValue
    taskSelection = treeTaskCreate.selection()[0]
    task = list(treeTaskCreate.item(taskSelection, "values"))
    task_join = task[0] + ";" + task[1] + ";" + task[2] + ";" + task[3] + ";" + "\n"
    print(task_join)

    f = open("Files/newTask.txt", "r+", encoding="utf-8")
    allTasks = f.readlines()
    f.close()
    f = open("Files/newTask.txt", "w", encoding="utf-8")
    for linha in allTasks:
        if task_join == linha:
            if taskName.get() != "":
                taskValue = taskName.get()
            else:
                taskValue = task[0]
            if taskDate.get_date() != "":
                selectedDate = taskDate.get_date()
            else:
                selectedDate = task[1]
            if taskCategoryDropdown.get() != "":
                categoryValue = taskCategoryDropdown.get()
            else:
                categoryValue = task[2]
            if taskEstadoDropdown.get() != "":
                estadoValue = taskEstadoDropdown.get()
            else:
                estadoValue = task[3]
            newTask = taskValue + ";" + selectedDate + ";" + categoryValue[0:len(categoryValue)-1] + ";" + estadoValue[0:len(estadoValue)-1] + ";" + "\n"
            f.write(newTask)
        else:
            f.write(linha)
    f.close()
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    mostrar()
    messagebox.showinfo(title="Feito!", message="Dados alterados!")
    


def filtrar():
    if currentUser == []:
        messagebox.showerror("No user is logged in", "Por favor inicie a sessão para adicionar a tarefa.")
        return
    lista_tarefas.delete(*lista_tarefas.get_children())
    f = open("Files/newTask.txt", "r", encoding="utf-8")
    tarefas = f.readlines()
    f.close()
    tar = 0
    for i in range (len(tarefas)):
        campos = tarefas[i].split(";")
        if nome_entry.get().upper() == campos[0].upper() or nome_entry.get() == "":
            if calendar.get_date() == (campos[1].replace("-", "/")) or calendar.get_date() == "":
                if campos[2] in categorias.get() or categorias.get() == "":
                    if estados.get() == (campos[3]) or estados.get() == "": 
                        lista_tarefas.insert("", "end", values=(campos[0],campos[1], campos[2], campos[3]))
                        tar += 1
    if nome_entry.get() == "":
        if categorias.get() == "":
            if calendar.get_date() == "":
                if estados.get() == "":
                    messagebox.showinfo(title="Sem filtro", message="Nenhum filtro foi aplicado!")
    if tar == 0:
        messagebox.showinfo(title="Nenhuma tarefa encontrada", message="Nenhum tarefa encontrada com este filtro!")
    limpar()

def addSearchElements():
    global canvasSearch, lbl_filtro, btn_getDate, lbl_date, lbl_nome, nome_entry, lbl_categ, categorias, lbl_estado, estados, btn_limpar, btn_filtrar, lista_tarefas, canvaslista, calendar
    try:
        cleanElements()
    except:
        pass
    
    # Canvas Pesquisa
    canvasSearch = Canvas(window,  width = 650, height = 200, bg='#a3d9ff', bd=1, relief = "flat")
    canvasSearch.place(x=200, y=50)

    # Labels
    lbl_filtro = Label(canvasSearch, text="Data: ", bg='#a3d9ff', font=('Verdana', 8))
    lbl_filtro.place(x=10, y=10)

    # Calendar
    calendar = Calendar(canvasSearch, selectmode = 'day',year =ano, month = mes,day = dia, locale='pt_br')
    calendar.place(x=60, y=10)
    calendar.selection_clear()

    # Button e Label get data
    btn_getDate = Button(canvasSearch, text = "Ver dia selecionado", width = 17, height= 1, bd=1, fg='white', bg='#006BB8', relief = "raised", font=("Verdana", 10),command = grad_date)
    btn_getDate.place(x=315, y= 170)

    lbl_date = Label(canvasSearch, text = "",bg='#a3d9ff', font = ("Verdana", 7))
    lbl_date.place(x=465, y=175)

    # Nome
    lbl_nome = Label(canvasSearch, text="Nome: ", bg='#a3d9ff', font = ("Verdana",8))
    lbl_nome.place(x=315, y=30)

    nome_entry = Entry(canvasSearch)
    nome_entry.place(x=378, y=30)

    # Categoria
    lbl_categ = Label(canvasSearch, text="Categoria: ", bg='#a3d9ff', font = ("Verdana", 8))
    lbl_categ.place(x=315, y=80)

    f = open("Files\category.txt", "r", encoding="utf-8")
    categ = f.readlines()
    f.close()

    categorias = ttk.Combobox(canvasSearch, values=categ, state="readonly")
    categorias.place(x =378, y = 80)

    # Estado
    lbl_estado = Label(canvasSearch, text="Estado: ", bg='#a3d9ff', font = ("Verdana", 8))
    lbl_estado.place(x=315, y= 130)

    est = ['Feito', 'Por fazer', 'Fazendo']
    estados = ttk.Combobox(canvasSearch, values=est, state="readonly")
    estados.place(x = 378, y = 130)

    # Button limpar
    btn_limpar = Button(canvasSearch, text="Limpar", width = 12, height= 1, bd=1, fg='white', bg='#006BB8', relief = "raised", font=("Verdana", 10), command=limpar)
    btn_limpar.place(x=530, y=50)

    # Button filtrar
    btn_filtrar = Button(canvasSearch, text="Filtrar", width = 12, height= 1, bd=1, fg='white', bg='#006BB8', relief = "raised", font=("Verdana", 10), command=filtrar)
    btn_filtrar.place(x=530, y=120)

    #Canvas da treeview
    canvaslista = Canvas(window,  width = 645, height = 300, bg='#a3d9ff', bd=1, relief = "flat")
    canvaslista.place(x=200,y=270)

    # Treeview
    lista_tarefas = ttk.Treeview(canvaslista, height=14, column=("col1", "col2", "col3", "col4"))
    lista_tarefas.heading("#0", text="")
    lista_tarefas.heading("#1", text="Nome")
    lista_tarefas.heading("#2", text="Data")
    lista_tarefas.heading("#3", text="Categoria")
    lista_tarefas.heading("#4", text="Estado")

    lista_tarefas.column("#0", width=1)
    lista_tarefas.column("#1", width=200)
    lista_tarefas.column("#2", width=150)
    lista_tarefas.column("#3", width=150)
    lista_tarefas.column("#4", width=150)

    lista_tarefas.place(x=0, y=0)

def grad_date():
    lbl_date.config(text = "Dia selecionado: " + calendar.get_date())

def grad_date2():
    lbl_date.config(text = "Dia selecionado: " + taskDate.get_date())
    

#---------------------------------------- Personal Area------------------#
def addPersonalElements():
    global comentario, lbl_coment, treeComentario, treeTaskCreate
    try:
        cleanElements()
    except:
        pass
    print('sim')
    if currentUser == []:
        messagebox.showerror("No user is logged", "Para ver isto tem que iniciar a sessão e ter uma conta admin!")
        return

    #Canvas Add Task
    canvasAddComent = Canvas(window,  width = 650, height = 200, bg='#a3d9ff', bd=1, relief = "flat")
    canvasAddComent.place(x=200, y=50)

    comentario = Entry(window)
    comentario.place(x=220, y=70, width= 200, height=165)

    lbl_coment = Label(window, text="Comentário", font = ("Verdana",8))
    lbl_coment.place(x=280, y=75)

    treeComentario = ttk.Treeview(canvasAddComent, height=7, column=("col1"))
    treeComentario.heading("#0", text="")
    treeComentario.heading("#1", text="Comentário")

    treeComentario.column("#0", width=0)
    treeComentario.column("#1", width=200)

    treeComentario.place(x= 230, y=20)

    # Botões Alterar e Remover
    btn_Addcomentarios = Button(canvasAddComent, text="Adicionar comentário", width = 18, height= 1, bd=1, fg='white', bg='#006BB8', relief = "raised", font=("Verdana", 10), command=addComentario)
    btn_Addcomentarios.place(x=480, y=50)

    btn_Seecomentario = Button(canvasAddComent, text="Ver comentário", width = 18, height= 1, bd=1, fg='white', bg='#006BB8', relief = "raised", font=("Verdana", 10), command=verComentarios)
    btn_Seecomentario.place(x=480, y=100)

    canvasTask = Canvas(window,  width = 645, height = 300, bg='#a3d9ff', bd=1, relief = "flat")
    canvasTask.place(x=200,y=250)

    treeTaskCreate = ttk.Treeview(canvasTask, height=14, column=("col1", "col2", "col3", "col4"))
    treeTaskCreate.heading("#0", text="")
    treeTaskCreate.heading("#1", text="Nome")
    treeTaskCreate.heading("#2", text="Data")
    treeTaskCreate.heading("#3", text="Categoria")
    treeTaskCreate.heading("#4", text="Estado")

    treeTaskCreate.column("#0", width=0)
    treeTaskCreate.column("#1", width=200)
    treeTaskCreate.column("#2", width=150)
    treeTaskCreate.column("#3", width=150)
    treeTaskCreate.column("#4", width=150)

    treeTaskCreate.place(x=0, y=0)
    
    f = open("Files/newTask.txt", "r", encoding="utf-8")
    addNewTaskTree = f.readlines()
    f.close()
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    for i in range (len(addNewTaskTree)):
        campos = addNewTaskTree[i].split(";")
        treeTaskCreate.insert("", "end", values=(campos[0],campos[1], campos[2], campos[3]))


def addComentario():
    if currentUser == []:
        messagebox.showerror("No user is logged", "Para ver isto tem que iniciar a sessão e ter uma conta admin!")
        return
    global i_TarefaComentario
    treeComentario.delete(*treeComentario.get_children())
    if comentario.get() == "":
        messagebox.showerror("Escreva algo!", "Escreva um comentário!")
    else:
        taskSelection = treeTaskCreate.selection()[0]
        task = list(treeTaskCreate.item(taskSelection, "values"))
        task_join = task[0] + ";" + task[1] + ";" + task[2] + ";" + task[3] + ";" + "\n"
        print(task_join)

        f = open("Files/newTask.txt", "r+", encoding="utf-8")
        allTasks = f.readlines()
        f.close()
        for i in range(len(allTasks)):
            for c in range(len(allTasks[i])):
                if task_join == allTasks[i]:
                    i_TarefaComentario = i  #index do tarefa associada ao comentario

        f = open("Files/comenarios.txt", "r", encoding="utf-8")
        coments = f.readlines()
        f.close()
        print(coments)
        if coments != []:
            for i in range(len(coments)):
                campos = coments[i].split(";")
                if str(i_TarefaComentario) == campos[1]:
                    messagebox.showerror("Erro!", "Está tarefa já tem um comentário associado!")
                else:
                    f = open("Files/comenarios.txt", "a", encoding="utf-8")
                    coment = comentario.get()
                    f.write(coment + ";" + str(i_TarefaComentario) + ";" + "\n")
                    f.close()
                    comentario.delete(0, END)
                    messagebox.showinfo("Sucesso!", "Comentário adicionado!")
        else:
            f = open("Files/comenarios.txt", "a", encoding="utf-8")
            coment = comentario.get()
            f.write(coment + ";" + str(i_TarefaComentario) + ";" + "\n")
            f.close()
            comentario.delete(0, END)
            messagebox.showinfo("Sucesso!", "Comentário adicionado!")


def verComentarios():
    if currentUser == []:
        messagebox.showerror("No user is logged", "Para ver isto tem que iniciar a sessão e ter uma conta admin!")
        return
    treeComentario.delete(*treeComentario.get_children())
    taskSelection = treeTaskCreate.selection()[0]
    task = list(treeTaskCreate.item(taskSelection, "values"))
    task_join = task[0] + ";" + task[1] + ";" + task[2] + ";" + task[3] + ";" + "\n"
    print(task_join)

    f = open("Files/newTask.txt", "r+", encoding="utf-8")
    allTasks = f.readlines()
    f.close()
    for i in range(len(allTasks)):
        for c in range(len(allTasks[i])):
            if task_join == allTasks[i]:
                i_TarefaComentario = i  #index do tarefa associada ao comentario
    f = open("Files/comenarios.txt", "r", encoding="utf-8")
    coments = f.readlines()
    for i in range(len(coments)):
        campos = coments[i].split(";")
        if str(i_TarefaComentario) == campos[1]:
            treeComentario.insert("", "end", values=(campos[0]))
        else:
            messagebox.showerror("Erro!", "Não há comentários para esta tarefa!")
    f.close()


#-----------------------------------Admin Menu---------------------------#
def addManageElements():
    global categoryLabel, categoryEntry, btnAddCategory, categoryBoxLabel, categoryDropdown, btnRemoveCategory, userLabel, userDropdown, btnRemoveUser, addUserLabel, usernameLabel, usernameEntry, passwordLabel, passwordEntry, emailLabel, emailEntry, userTypeLabel, userType, adminAddBtn, canvasAddCategory, canvasaddUser, canvasRemoveUser,catLabel
    if currentUser == []:
        messagebox.showerror("No user is logged", "Para ver isto tem que iniciar a sessão e ter uma conta admin!")
    elif currentUser[1] == "admin":
        try:
            cleanElements()
        except:
            pass
        #Canvas Add Category
        canvasAddCategory = Canvas(window,  width = 650, height = 150, bg='#a3d9ff', bd=1, relief = "flat")
        canvasAddCategory.place(x=200, y=50)

        catLabel= Label(canvasAddCategory, text="Categorias", bg="#a3d9ff",font=("Verdana", 14))
        catLabel.place(x=10,y=10)

        categoryLabel = Label(canvasAddCategory, text="Que categoria pretendes adicionar?", bg="#a3d9ff",font=("Verdana", 11))
        categoryLabel.place(x=10,y=60)

        categoryEntry = Entry(canvasAddCategory)
        categoryEntry.place(x=280,y=60)

        btnAddCategory = Button(canvasAddCategory, text="Submeter",font=("Verdana", 10), command=addCategory)
        btnAddCategory.place(x=430,y=55)

        categoryBoxLabel = Label(canvasAddCategory, text="Todas as Categorias", bg="#a3d9ff",font=("Verdana", 11))
        categoryBoxLabel.place(x=10,y=110)

        categoryDropdown = ttk.Combobox(canvasAddCategory)
        categoryDropdown.place(x=180,y=110)

        btnRemoveCategory = Button(canvasAddCategory, text="Remover Categoria",font=("Verdana", 10), command=removeCategory)
        btnRemoveCategory.place(x=430,y=105)

        #Canvas Add User
        canvasaddUser = Canvas(window, width = 650, height = 150, bg='#a3d9ff', bd=1, relief = "flat")
        canvasaddUser.place(x=200, y=255)

        addUserLabel = Label(canvasaddUser, text="Adicionar novo utilizador:", bg="#a3d9ff",font=("Verdana", 14))
        addUserLabel.place(x=10,y=10)

        usernameLabel = Label(canvasaddUser, text="Username:", bg="#a3d9ff",font=("Verdana", 11))
        usernameLabel.place(x=10,y=40)

        usernameEntry = Entry(canvasaddUser)
        usernameEntry.place(x=110,y=40)

        passwordLabel = Label(canvasaddUser, text="Password:", bg="#a3d9ff",font=("Verdana", 11))
        passwordLabel.place(x=310,y=40)

        passwordEntry = Entry(canvasaddUser, show="*")
        passwordEntry.place(x=410,y=40)

        emailLabel = Label(canvasaddUser, text="Email:", bg="#a3d9ff",font=("Verdana", 11))
        emailLabel.place(x=10,y=80)

        emailEntry = Entry(canvasaddUser)
        emailEntry.place(x=110,y=80)

        userTypeLabel = Label(canvasaddUser, text="Tipo de utilizador:", bg="#a3d9ff",font=("Verdana", 11))
        userTypeLabel.place(x=310,y=80)

        userType = ttk.Combobox(canvasaddUser, values=["normal", "admin"])
        userType.place(x=410,y=80)
        userType.current(0)

        adminAddBtn = Button(canvasaddUser, text="Adicionar utilizador",font=("Verdana", 10), command=addUser)
        adminAddBtn.place(x=520,y=115)
            
            #verificar se o ficheiro existe
        if os.path.exists("Files/category.txt"):
            with open("Files/category.txt", "r") as file:
                categories = file.readlines()
                    #list compreension que vai fazer com que cada valor do dropdown seja a lita formada pelas categorias do ficheiro --> equivalente a "for category in categories:  categoryDropdown['values'] = category.strip()"
                categoryDropdown['values'] = [category.strip() for category in categories]
                categoryDropdown.current(0)
        
        canvasRemoveUser = Canvas(window, width = 650, height = 120, bg='#a3d9ff', bd=1, relief = "flat")
        canvasRemoveUser.place(x=200, y=450)

        userLabel = Label(canvasRemoveUser, text="Selecionar utilizador para remover:", bg="#a3d9ff",font=("Verdana", 14))
        userLabel.place(x=10, y=10)

        userDropdown = ttk.Combobox(canvasRemoveUser)
        userDropdown.place(x=10, y=70)


        if os.path.exists("Files/users.txt"):
            with open("Files/users.txt", "r") as file:
                users = file.readlines()
                userDropdown['values'] = [user.strip().split(';')[2] for user in users]
                userDropdown.current(0)

        btnRemoveUser = Button(canvasRemoveUser, text="Remover Utilizador",font=("Verdana", 10))
        btnRemoveUser.place(x=200, y=65)
        
    else:
        messagebox.showerror("Access Denied", "A sua conta não tem acesso admin!")

    




def addCategory():
    categoryValue = categoryEntry.get()
    if categoryValue.strip() == '':
        messagebox.showerror("Error", "O valor da categoria não pode estar vazio!")
        return
    if os.path.exists("Files/category.txt"):
        with open("Files/category.txt", "r") as file:
            categories = file.readlines()
            for line in categories:
                if categoryValue.strip().lower() == line.strip().lower():
                    messagebox.showerror("Already exists", "Esta categoria já existe!")
                    return
            else:
                with open("Files/category.txt", "a") as file:
                    file.write(categoryValue.strip() + "\n")
                    messagebox.showinfo("Category Added", f"A categoria {categoryValue} foi adicionada!")
                    categoryEntry.delete(0, 'end')
    else:
        with open("Files/category.txt", "w") as file:
            file.write(categoryValue.strip() + "\n")
            messagebox.showinfo("Category Added", f"TA categoria {categoryValue} foi adicionada!")


def removeCategory():
    selected_category = categoryDropdown.get()
    if selected_category == "":
        messagebox.showerror("Error", "Nenhuma categoria adicionada")
    else:
        with open("Files/category.txt", "r") as file:
            categories = file.readlines()
        with open("Files/category.txt", "w") as file:
            for category in categories:
                if category.strip() != selected_category:
                    file.write(category)
        messagebox.showinfo("Category removed", f"A categoria {selected_category} foi removida.")
        categoryDropdown['values'] = [category.strip() for category in categories if category.strip() != selected_category]
        categoryDropdown.current(0)    

def removeUser():
    user = userDropdown.get()
    if user.strip() == '':
        messagebox.showerror("Error", "Por favor selecione um utilizador para remover.")
        return
    if os.path.exists("Files/users.txt"):
        with open("Files/users.txt", "r") as file:
            users = file.readlines()
        with open("Files/users.txt", "w") as file:
            for line in users:
                    # se o user for difrente ao index dois da linha (ou seja ao username) entao vai escrever a linha. dessa forma escreve todos os users menos o selecionado e com isto remove o
                if user != line.split(";")[2]:
                    file.write(line)
            messagebox.showinfo("User removed", f"O utilizador {user} foi removido.")
            userDropdown.current(0)
    else:
        messagebox.showerror("Error", "Não encontrada ficha do utilizador.")
    addManageElements()


def addUser():
    username = usernameEntry.get()
    password = passwordEntry.get()
    email = emailEntry.get()
    user_type = userType.get()

    if os.path.exists("Files/users.txt"):
        with open("Files/users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                if username == user.strip().split(';')[2]:
                    messagebox.showerror("Error", "Nome de utilizador já usado.")
                    return
    else:
        messagebox.showerror("Error", "Não encontrada ficha do utilizador")
        return
    # add the user to the file
    with open("Files/users.txt", "a") as file:
        file.write(f"0;0;{username};{password};False;{email};{user_type}\n")
    messagebox.showinfo("Success", "O utilizador foi adicionado com sucesso.")
    userDropdown['values'] = [user.strip().split(';')[2] for user in users] + [username]
    userDropdown.current(len(userDropdown['values']) - 1)


#-----------------------------------Clean Tkinter elements------------------------#
    #esta função limpa os elementos tkinter de cada aba da pagina
def cleanElements():
    for button in taskButtons:
        button.destroy()
    taskLabel.destroy()
    taskName.destroy()
    btnSubmitTask.destroy()
    taskCategoryDropdown.destroy()
    taskCategoryLabel.destroy()
    #taskDate.destroy()
    btnAddTask.destroy()
    categoryLabel.destroy()
    categoryEntry.destroy()
    btnAddCategory.destroy()
    categoryBoxLabel.destroy() 
    categoryDropdown.destroy() 
    btnRemoveCategory.destroy() 
    userLabel.destroy() 
    userDropdown.destroy() 
    btnRemoveUser.destroy() 
    addUserLabel.destroy() 
    usernameLabel.destroy() 
    usernameEntry.destroy() 
    passwordLabel.destroy() 
    passwordEntry.destroy() 
    emailLabel.destroy() 
    emailEntry.destroy() 
    userTypeLabel.destroy() 
    userType.destroy() 
    adminAddBtn.destroy()
    canvasAddCategory.destroy()
    canvasRemoveUser.destroy()
    canvasaddUser.destroy()
    catLabel.destroy()
    btnAlterarTask.destroy()
    canvasTask.destroy()
    createtaskLabel.destroy()
    treeTaskCreate.destroy()
    canvasSearch.destroy()
    lbl_filtro.destroy()
    btn_getDate.destroy()
    lbl_date.destroy()
    lbl_nome.destroy()
    nome_entry.destroy()
    lbl_categ.destroy()
    categorias.destroy()
    lbl_estado.destroy()
    estados.destroy()
    btn_limpar.destroy()
    btn_filtrar.destroy()
    lista_tarefas.destroy()
    canvaslista.destroy()
    #calendar.destroy()

#-----------------------------------MainScreen----------------------------#

window.config(bg = '#FDF4E3')
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

appWidth = 900                             
appHeight = 600
x = (screenWidth/2) - (appWidth/2)        
y = (screenHeight/2) - (appHeight/2)
window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
window.minsize(900, 600)
window.maxsize(900, 600)

#img = ImageTk.PhotoImage(Image.open("img\homepage.jpg"))

# #Botões de conta
# btnNotificacao = Button(window, width = 30, height= 30, bd=1, image = imgNot, compound=LEFT, relief = "raised")
# btnNotificacao.place(x=450, y=0)

# MainPage
userLabel = Label(window, width = 5, height = 2, text = "", bg='#FDF4E3', fg="black", font=("Verdana", 10))
userLabel.place(x=20, y=10)

btnInciarSessao = Button(window, width = 15, height= 2, text = "Iniciar Sessão", bd=1,fg='white', bg='#006BB8',font=("Verdana", 10), relief = "raised",command = login)
btnInciarSessao.place(x=644, y=0)

btnCriarConta = Button(window, width = 15, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8',font=("Verdana", 10), relief = "raised",command = register)
btnCriarConta.place(x=772, y=0)

btnClearScreen = Button(window, width = 15, height=2, text = "Limpar tela", bd=1,fg='white', bg='#006BB8',font=("Verdana", 10), relief = "raised",command = cleanElements)
btnClearScreen.place(x=300, y=0)

#Canvas com botões da esquerda
btnCanvas = Canvas(window, width = 155, height = 610, bg='#FDF4E3', bd=1, relief = "flat",highlightthickness=2, highlightbackground="#00008B")
btnCanvas.place(x=0, y=40)

btnCriarTaref = Button(btnCanvas, width = 15, height= 3, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8',font=("Verdana", 12),highlightthickness=2, highlightbackground="#00008B" , relief = "raised",command=addTaskElements)
btnCriarTaref.place(x=1, y=2)

btnPesquisa = Button(btnCanvas, width = 15, height= 3, text = "Pesquisa", bd=1, fg='white', bg='#006BB8',font=("Verdana", 12), relief = "raised",command=addSearchElements )
btnPesquisa.place(x=1, y=68)

btnDashboard = Button(btnCanvas, width = 15, height= 3, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8',font=("Verdana", 12), relief = "raised", command=addPersonalElements)
btnDashboard.place(x=1, y=134)

btnGerirCat = Button(btnCanvas, width = 15, height= 3, text = "Gerir", bd=1, fg='white', bg='#006BB8',font=("Verdana", 12), relief = "raised", command=addManageElements)
btnGerirCat.place(x=1, y=200)

""" ImgCanvas = Canvas(window, width = 600, height = 455, bd=0, bg='#a3d9ff', relief = "flat")
ImgCanvas.place(x=195, y=40) """
#ImgCanvas.create_image(10,250, image = '')



window.mainloop()
