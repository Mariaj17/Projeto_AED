from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
from PIL import ImageTk,Image
import os
from users import *
import utils



global window
window=Tk()

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
#-----------------------------------MainScreen----------------------------#


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

userLabel = Label(window, width = 5, height = 2, text = "")
userLabel.place(x= 0, y=0)

btnInciarSessao = Button(window, width = 20, height= 2, text = "Iniciar Sessões", bd=1, fg='black', relief = "raised",command = login)
btnInciarSessao.place(x=500, y=0)

btnCriarConta = Button(window, width = 20, height= 2, text = "Criar Conta", bd=1, fg='black', relief = "raised",command = register)
btnCriarConta.place(x=650, y=0)

btnAdicionarTarefa = Button(window, width = 20, height= 2, text= "Adicionar tarefa", bd=1, fg='black', relief = "raised", command=addTask)
btnAdicionarTarefa.place(x=350, y=0)

window.mainloop()