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
            currentUser.clear()
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
                currentUser.append(users[index].strip().split(";")[6])
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
    global categoryName, btnSubmitCathegory, btnAddTask
    try:
        cleanElements()
    except:
        pass
    categoryName = Entry(window)
    categoryName.grid(row=1, column=1)

    btnSubmitCathegory = Button(window, text="Submit", command=addTask)
    btnSubmitCathegory.grid(row=2, column=1)

    btnAddTask = Button(window, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=sendTask)
    btnAddTask.grid(row=1, column=3)

    

def addTask():
    categoryValue = categoryName.get()
    print(categoryValue)
    cleanElements()


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

#-----------------------------------Admin Menu---------------------------#
def addManageElements():
    global categoryLabel, categoryEntry, btnAddCathegory, categoryBoxLabel, categoryDropdown, userLabel, userDropdown, btnRemoveUser
    if currentUser == []:
        messagebox.showerror("No user is logged", "To view this you need to be logged in with an admin account!")
    elif currentUser[1] == "admin":
        try:
            cleanElements()
        except:
            pass
        categoryLabel = Label(window, text="What category do you wish to add?", bg="#a3d9ff")
        categoryLabel.grid(row=1, column=1, padx=(10,10))

        categoryEntry = Entry(window)
        categoryEntry.grid(row=2, column=1, padx=(10,10))

        btnAddCathegory = Button(window, text="Submit", command=addCategory)
        btnAddCathegory.grid(row=3, column=1, padx=(10,10))

        categoryBoxLabel = Label(window, text="All categories", bg="#a3d9ff")
        categoryBoxLabel.grid(row=1,column=2, padx=(10,10))

        categoryDropdown = ttk.Combobox(window)
        categoryDropdown.grid(row=2, column=2, padx=(10,10))
            
            #verificar se o ficheiro existe
        if os.path.exists("Files/category.txt"):
            with open("Files/category.txt", "r") as file:
                categories = file.readlines()
                    #list compreension que vai fazer com que cada valor do dropdown seja a lita formada pelas categorias do ficheiro --> equivalente a "for category in categories:  categoryDropdown['values'] = category.strip()"
                categoryDropdown['values'] = [category.strip() for category in categories]
                categoryDropdown.current(0)

        userLabel = Label(window, text="Select a user to remove:", bg="#a3d9ff")
        userLabel.grid(row=1, column=3, padx=(10,10))


        userDropdown = ttk.Combobox(window)
        userDropdown.grid(row=2, column=3, padx=(10,10))


        if os.path.exists("Files/users.txt"):
            with open("Files/users.txt", "r") as file:
                users = file.readlines()
                userDropdown['values'] = [user.strip().split(';')[2] for user in users]
                userDropdown.current(0)

        btnRemoveUser = Button(window, text="Remove User", command=removeUser)
        btnRemoveUser.grid(row=3, column=3, padx=(10,10))
        
    else:
        messagebox.showerror("Access Denied", "Your account does not have admin access!")

def addCategory():
    categoryValue = categoryEntry.get()
    if categoryValue.strip() == '':
        messagebox.showerror("Error", "Category value cannot be empty")
        return
    if os.path.exists("Files/category.txt"):
        with open("Files/category.txt", "r") as file:
            categories = file.readlines()
            for line in categories:
                if categoryValue.strip().lower() == line.strip().lower():
                    messagebox.showerror("Already exists", "The category you are trying to add already exists!")
                    return
            else:
                with open("Files/category.txt", "a") as file:
                    file.write(categoryValue.strip() + "\n")
                    messagebox.showinfo("Category Added", f"The category {categoryValue} was added!")
                    categoryEntry.delete(0, 'end')
    else:
        with open("Files/category.txt", "w") as file:
            file.write(categoryValue.strip() + "\n")
            messagebox.showinfo("Category Added", f"The category {categoryValue} was added!")
        

def removeUser():
    user = userDropdown.get()
    if user.strip() == '':
        messagebox.showerror("Error", "Please select a user to remove.")
        return
    if os.path.exists("Files/users.txt"):
        with open("Files/users.txt", "r") as file:
            users = file.readlines()
        with open("Files/users.txt", "w") as file:
            for line in users:
                    # se o user for difrente ao index dois da linha (ou seja ao username) entao vai escrever a linha. dessa forma escreve todos os users menos o selecionado e com isto remove o
                if user != line.split(";")[2]:
                    file.write(line)
            messagebox.showinfo("User removed", f"The user {user} was removed.")
            userDropdown.set("")
    else:
        messagebox.showerror("Error", "User file not found.")

#-----------------------------------Clean Tkinter elements------------------------#
    #esta função limpa os elementos tkinter de cada aba da pagina
def cleanElements():
    categoryName.destroy()
    btnSubmitCathegory.destroy()
    btnAddTask.destroy()
    searchName.destroy()
    btnSearch.destroy()
    categoryLabel.destroy()
    categoryEntry.destroy()
    btnAddCathegory.destroy()
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

btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised", command=addManageElements)
btnGerirCat.place(x=30, y=350)

ImgCanvas = Canvas(window, width = 600, height = 455, bd=0, bg='#a3d9ff', relief = "flat")
ImgCanvas.place(x=195, y=40)
#ImgCanvas.create_image(10,250, image = img)



window.mainloop()