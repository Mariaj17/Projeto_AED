from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
card = {}
dataDict = {}
selectedLanguage = "French"
#--------------------------------Get words from file--------------------#
try:
    knownData = pandas.read_csv(f"Day31- Flash card app\data/{selectedLanguage}wordsToLearn.csv")
except FileNotFoundError:
    data = pandas.read_csv(f"Day31- Flash card app\data/Words.csv")
    dataDict = data.to_dict(orient="records")
else:
    dataDict = knownData.to_dict(orient="records")

#--------------------------------Show words on card---------------------#
def listbox_used(event):
    global selectedLanguage
    # Gets current selection from listbox
    selectedLanguage = listbox.get(listbox.curselection())
    randomWord()

def randomWord():
    global card, flipCardTimer
    window.after_cancel(flipCardTimer)
    card = random.choice(dataDict)
    canvas.itemconfig(title, text= f"{selectedLanguage}", fill="black")
    canvas.itemconfig(word, text=card[f"{selectedLanguage}"], fill="black")
    canvas.itemconfig(cardBackground, image=cardFrontImage)
    flipCardTimer = window.after(3000, func=timerCard) 

def timerCard():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=card["English"], fill="white")
    canvas.itemconfig(cardBackground, image=cardBackImage)

def knownWord():
    dataDict.remove(card)
    print(len(dataDict))
    data = pandas.DataFrame(dataDict)
    data.to_csv(f"Day31- Flash card app\data/{selectedLanguage}wordsToLearn.csv", index=False)
    randomWord()
#--------------------------------App UI---------------------------------#

window = Tk()
window.title("Flash card App")
window.config(background=BACKGROUND_COLOR, width=1000, height=700, padx=50, pady=50)

flipCardTimer = window.after(3000, func=timerCard)

canvas = Canvas(width=900, height=600, background=BACKGROUND_COLOR, highlightthickness=0)
cardFrontImage = PhotoImage(file="Day31- Flash card app\images/card_front.png")
cardBackImage = PhotoImage(file="Day31- Flash card app\images/card_back.png")
cardBackground = canvas.create_image(450, 300, image=cardFrontImage)
title = canvas.create_text(450, 150, text="Title", font=("Arial", 25, "italic"))
word = canvas.create_text(450, 250, text="Word", font=("Arial", 35, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

#Buttons
wrongImage = PhotoImage(file="Day31- Flash card app\images/wrong.png")
wrongBtn = Button(image=wrongImage, highlightthickness=0, relief="flat", background=BACKGROUND_COLOR, command=randomWord)
wrongBtn.grid(row=1, column=0)

rightImage = PhotoImage(file="Day31- Flash card app\images/right.png")
rightBtn = Button(image=rightImage, highlightthickness=0, relief="flat", background=BACKGROUND_COLOR, command=knownWord)
rightBtn.grid(row=1,column=1)



randomWord()



listbox = Listbox(height=4)
languages = ["Afrikaans", "Arabic", "Bulgarian", "Czech", "Welsh", "Danish", "German", "Greek", "Finnish", "French", "Hebrew", "Hindi", "Icelandic", "Korean", "Maori", "Polish", "Russian", "Swedish", "Thai", "Turkish", "Vietnamese", "Chinese", "Japanese","Spanish", "Italian"]
for item in languages:
    listbox.insert(languages.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)

listbox.grid(row=2, column=0)

window.mainloop()
