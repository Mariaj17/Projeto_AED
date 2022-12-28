from tkinter import *
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import re
import os


def register_user():
    usernameInfo = username.get()
    passwordInfo = password.get()
    emailInfo    = email.get()

    try:
        with open("Files/users.txt", "r") as file:
            print("File exists")
    except FileNotFoundError:
        with open("Files/users.txt", "w") as file:

            file.write("admin" + ";" + "123" + ";" + "admin@gmail.com" + ";" + "admin" + "\n")

            file.write(
                usernameInfo + ";" + 
                passwordInfo + ";" + 
                emailInfo + ";" + 
                "normal" + "\n")

            messagebox.showinfo("Account was successfully!", "Your new account has been created!")
    else:
        with open("Files/users.txt", "a") as file:

            file.write(
                usernameInfo + ";" + 
                passwordInfo + ";" + 
                emailInfo + ";" + 
                "normal" + "\n")
            messagebox.showinfo("Account was successfully!", "Your new account has been created!")
        

    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    emailEntry.delete(0,END)
    Label(screen1,text = "Registration Sucess").pack()
    screen1.destroy()


def validateReg():
    while True:
        userRegValidate = username.get()
        passRegValidate = password.get()
        emailRegValidate= email.get()
        validForm = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        if len(userRegValidate) < 4:
            messagebox.showerror("Invalid Username!", "Username needs to be at least 4 characters long!")
            username.set("")
            password.set("")
            email.set("")
            break
        
        if len(passRegValidate) < 6:
            messagebox.showerror("Invalid Password!", "Password should be at least 6 chatacters long!")
            username.set("")
            password.set("")
            email.set("")
            break
        
        # if (re.fullmatch(validForm, emailRegValidate)):
        #     register_user()
        #     break
            
        # else:
        #     messagebox.showerror("Invalid E-Mail", "Your E-Mail must include the characters '@' and '.'")
        #     username.set("")
        #     password.set("")
        #     email.set("")
        
                                           
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

def invalidPassword():
    messagebox.showerror("Invalid password", "Your password is invalid!")

def userNotFound():
    messagebox.showerror("Invalid username", "The username does not exist!")



def loginValidation():
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
            for user in loginValidation:
                Fields = user.split(";")
                if username1 == Fields[0]:
                    if password1 == Fields[1]:
                        screen2.destroy()
                        loginSuccess()                   
                        print("login done move to page")
                    return
                else:
                    invalidPassword()
            else: userNotFound()
    

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

