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

global currentUser

global userLabel

currentUser = []
#-----------------------------------Functions-----------------------------#


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
            currentUser.pop()
            print(currentUser)
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
                currentUser.append(usernameLogged)
            if utils.checkUserLogged(usernameLogged, users) == False:
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
            messagebox.showerror("Error 404 file not found!", "The aplication has no users! please create one in the registration page")
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


#-----------------------------------Functions tasks -----------------------#

#-----------------------------------Criar Tarefa--------------------------#
def addTaskElements():
    global cathegoryName, btnSubmitCathegory, btnAddTask
    try:
        cleanElements()
    except:
        pass
    cathegoryName = Entry(window)
    cathegoryName.grid(row=1, column=1)

    btnSubmitCathegory = Button(window, text="Submit", command=addTask)
    btnSubmitCathegory.grid(row=3, column=1)

    btnAddTask = Button(window, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=sendTask)
    btnAddTask.grid(row=1, column=3)

    

def addTask():
    cathegoryValue = cathegoryName.get()
    print(cathegoryValue)
    cleanElements()

def cleanElements():
    cathegoryName.destroy()
    btnSubmitCathegory.destroy()
    btnAddTask.destroy()
    searchName.destroy()
    btnSearch.destroy()

#-----------------------------------pesquisa------------------------------#
def addSearchElements():
    global searchName, btnSearch
    try:
        cleanElements()
    except:
        pass
    searchName = Entry(window)
    searchName.grid(row=1, column=1)

    btnSearch = Button(window, text="Submit", command=searchTask)
    btnSearch.grid(row=2, column=1)

def searchTask():
    searchValue = searchName.get()
    print(searchValue)
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
userLabel.grid(row=0, column=0)

btnInciarSessao = Button(window, width = 20, height= 2, text = "Iniciar Sessões", bd=1,fg='white', bg='#006BB8', relief = "raised",command = login)
btnInciarSessao.grid(row=0, column=1)

btnCriarConta = Button(window, width = 20, height= 2, text = "Criar Conta", bd=1, fg='white', bg='#006BB8', relief = "raised",command = register)
btnCriarConta.grid(row=0, column=2)

#Canvas com botões da esquerda
btnCanvas = Canvas(window, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
btnCanvas.grid(row=1, column=0, rowspan=40)

btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=addTaskElements)
btnCriarTaref.place(x=30, y=50)

btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=addSearchElements )
btnPesquisa.place(x=30, y=150)

btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised", )
btnDashboard.place(x=30, y=250)

btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised", )
btnGerirCat.place(x=30, y=350)

ImgCanvas = Canvas(window, width = 600, height = 455, bd=0, bg='#a3d9ff', relief = "flat")
ImgCanvas.place(x=195, y=40)
#ImgCanvas.create_image(10,250, image = img)



window.mainloop()