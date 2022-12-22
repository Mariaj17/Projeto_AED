from tkinter import *
from tkinter import ttk # treeview
from tkinter import messagebox 
from PIL import ImageTk,Image  
import os

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

window.title("")

window.mainloop()