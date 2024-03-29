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


