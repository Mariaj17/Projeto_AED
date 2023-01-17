from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
from PIL import ImageTk,Image
import os
from users import *
import utils
from tarefas import *
from categorias import *
from tkcalendar import Calendar


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
    global taskLabel, taskName, btnSubmitTask, btnAddTask, taskCategoryDropdown, taskCategoryLabel, taskDate
    try:
        cleanElements()
    except:
        pass
    taskLabel= Label(window, text="What task do you wish to add?", bg="#a3d9ff")
    taskLabel.grid(row=1, column=1, padx=(10,10))

    taskName = Entry(window)
    taskName.grid(row=2, column=1,padx=(10,10))

    btnSubmitTask = Button(window, text="Submit", command=addTask)
    btnSubmitTask.grid(row=3, column=1,padx=(10,10))

    taskCategoryLabel = Label(window, text="Select a Category", bg="#a3d9ff")
    taskCategoryLabel.grid(row=1, column=2, padx=(10,10))

    taskCategoryDropdown = ttk.Combobox(window)
    taskCategoryDropdown.grid(row=2, column=2, padx=(10,10))

    btnAddTask = Button(window, width = 20, height= 2, text = "Enviar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=sendTask)
    btnAddTask.grid(row=1, column=3,padx=(10,10))


    taskDate = Calendar(window, selectmode = "day",year=2022,month=1,date=1)
    taskDate.grid(row=4, column=1, padx=(10,10))


    if os.path.exists("Files/category.txt"):
            with open("Files/category.txt", "r") as file:
                categories = file.readlines()
                    #list compreension que vai fazer com que cada valor do dropdown seja a lita formada pelas categorias do ficheiro --> equivalente a "for category in categories:  categoryDropdown['values'] = category.strip()"
                taskCategoryDropdown['values'] = [category.strip() for category in categories]
                taskCategoryDropdown.current(0)

def addTask():
    taskValue = taskName.get()
    categoryValue = taskCategoryDropdown.get()
    selectedDate = taskDate.get_date()
    if currentUser == []:
        messagebox.showerror("No user is logged in", "Please log in to add a task.")
        return
    if not os.path.exists("Files/tasksNotDone.txt"):
        open("Files/tasksNotDone.txt", "w").close()
    with open("Files/tasksNotDone.txt", "r") as file:
        tasks = file.readlines()
        for i, line in enumerate(tasks):
            if currentUser[0] in line:
                if taskValue in line:
                    messagebox.showerror("Task already exists", "The task you are trying to add already exists.")
                    return
                tasks[i] = line.rstrip() + f";[{taskValue},{selectedDate}]\n"
                with open("Files/tasksNotDone.txt", "w") as file:
                    file.writelines(tasks)
                return
    with open("Files/tasksNotDone.txt", "a") as file:
        file.write(f"{currentUser[0]};{categoryValue};[{taskValue},{selectedDate}]\n")





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
#---------------------------------------- Personal Area------------------#
def addPersonalElements():
    global taskButtons
    taskButtons = []
    try:
        cleanElements()
    except:
        pass
    if currentUser == []:
        messagebox.showerror("No user is logged", "To view this you need to be logged in and have an admin account!")
        return
    if os.path.exists("Files/tasksNotDone.txt"):
        i = 1
        with open("Files/tasksNotDone.txt", "r") as file:
            for line in file:
                userTask = line.strip().split(";")
                if currentUser[0] == userTask[0]:
                    task_list = userTask[2:]
                    for j, task in enumerate(task_list):
                        taskButton = Button(window, text=task[1:-1])
                        taskButton.grid(row=i+j, column=1)
                        taskButtons.append(taskButton)
    else:
        messagebox.showerror("No task", "There are no tasks")




#-----------------------------------Admin Menu---------------------------#
def addManageElements():
    global categoryLabel, categoryEntry, btnAddCategory, categoryBoxLabel, categoryDropdown, btnRemoveCategory, userLabel, userDropdown, btnRemoveUser, addUserLabel, usernameLabel, usernameEntry, passwordLabel, passwordEntry, emailLabel, emailEntry, userTypeLabel, userType, adminAddBtn
    if currentUser == []:
        messagebox.showerror("No user is logged", "To view this you need to be logged in and have an admin account!")
    elif currentUser[1] == "admin":
        try:
            cleanElements()
        except:
            pass
        categoryLabel = Label(window, text="What category do you wish to add?", bg="#a3d9ff")
        categoryLabel.grid(row=1, column=1, padx=(10,10))

        categoryEntry = Entry(window)
        categoryEntry.grid(row=2, column=1, padx=(10,10))

        btnAddCategory = Button(window, text="Submit", command=addCategory)
        btnAddCategory.grid(row=3, column=1, padx=(10,10))

        categoryBoxLabel = Label(window, text="All categories", bg="#a3d9ff")
        categoryBoxLabel.grid(row=1,column=2, padx=(10,10))

        categoryDropdown = ttk.Combobox(window)
        categoryDropdown.grid(row=2, column=2, padx=(10,10))

        btnRemoveCategory = Button(window, text="Remove Category", command=removeCategory)
        btnRemoveCategory.grid(row=3, column=2, padx=(10,10))

        addUserLabel = Label(window, text="Add a new user:", bg="#a3d9ff")
        addUserLabel.grid(row=4, column=1, padx=(10,10), pady=(10,10))

        usernameLabel = Label(window, text="Username:", bg="#a3d9ff")
        usernameLabel.grid(row=5, column=1, padx=(10,10))

        usernameEntry = Entry(window)
        usernameEntry.grid(row=6, column=1, padx=(10,10))

        passwordLabel = Label(window, text="Password:", bg="#a3d9ff")
        passwordLabel.grid(row=7, column=1, padx=(10,10))

        passwordEntry = Entry(window, show="*")
        passwordEntry.grid(row=8, column=1, padx=(10,10))

        emailLabel = Label(window, text="Email:", bg="#a3d9ff")
        emailLabel.grid(row=9, column=1, padx=(10,10))

        emailEntry = Entry(window)
        emailEntry.grid(row=10, column=1, padx=(10,10))

        userTypeLabel = Label(window, text="User Type:", bg="#a3d9ff")
        userTypeLabel.grid(row=11, column=1, padx=(10,10))

        userType = ttk.Combobox(window, values=["normal", "admin"])
        userType.grid(row=12, column=1, padx=(10,10))
        userType.current(0)

        adminAddBtn = Button(window, text="Add User", command=addUser)
        adminAddBtn.grid(row=13, column=1, padx=(10,10))
            
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


def removeCategory():
    selected_category = categoryDropdown.get()
    if selected_category == "":
        messagebox.showerror("Error", "No category selected")
    else:
        with open("Files/category.txt", "r") as file:
            categories = file.readlines()
        with open("Files/category.txt", "w") as file:
            for category in categories:
                if category.strip() != selected_category:
                    file.write(category)
        messagebox.showinfo("Category removed", f"The category {selected_category} was removed.")
        categoryDropdown['values'] = [category.strip() for category in categories if category.strip() != selected_category]
        categoryDropdown.current(0)    

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
            userDropdown.current(0)
    else:
        messagebox.showerror("Error", "User file not found.")
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
                    messagebox.showerror("Error", "Username already exists.")
                    return
    else:
        messagebox.showerror("Error", "User file not found.")
        return
    # add the user to the file
    with open("Files/users.txt", "a") as file:
        file.write(f"0;0;{username};{password};False;{email};{user_type}\n")
    messagebox.showinfo("Success", "User added successfully.")
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
    taskDate.destroy()
    btnAddTask.destroy()
    searchName.destroy()
    btnSearch.destroy()
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

btnClearScreen = Button(window, width = 20, height=2, text = "Clear Screen", bd=1,fg='white', bg='#006BB8', relief = "raised",command = cleanElements)
btnClearScreen.grid(row=0,column=3)
#Canvas com botões da esquerda
btnCanvas = Canvas(window, width = 200, height = 460, bg='#7e6b8f', bd=0, relief = "flat")
btnCanvas.grid(row=1, column=0, rowspan=40)

btnCriarTaref = Button(btnCanvas, width = 20, height= 5, text = "Criar Tarefa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=addTaskElements)
btnCriarTaref.place(x=30, y=50)

btnPesquisa = Button(btnCanvas, width = 20, height= 5, text = "Pesquisa", bd=1, fg='white', bg='#006BB8', relief = "raised",command=addSearchElements )
btnPesquisa.place(x=30, y=150)

btnDashboard = Button(btnCanvas, width = 20, height= 5, text = "Área Pessoal", bd=1, fg='white', bg='#006BB8', relief = "raised", command=addPersonalElements)
btnDashboard.place(x=30, y=250)

btnGerirCat = Button(btnCanvas, width = 20, height= 5, text = "Gerir", bd=1, fg='white', bg='#006BB8', relief = "raised", command=addManageElements)
btnGerirCat.place(x=30, y=350)

ImgCanvas = Canvas(window, width = 600, height = 455, bd=0, bg='#a3d9ff', relief = "flat")
ImgCanvas.place(x=195, y=40)
#ImgCanvas.create_image(10,250, image = img)



window.mainloop()