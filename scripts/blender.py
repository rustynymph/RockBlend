from Tkinter import *
import Tkinter as ttk
winWidth = 1500
winHeight = 600
mainImageWidth = 447

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def freestyleHoverOn(arg):
	freestyleButton.configure(image = freestyleButtonPhotoHover)
	freestyleButton.image = freestyleButtonPhotoHover

def practiceHoverOn(arg):
	practiceButton.configure(image = practiceButtonPhotoHover)
	practiceButton.image = practiceButtonPhotoHover

def freestyleHoverOff(arg):
	freestyleButton.configure(image = freestyleButtonPhoto)
	freestyleButton.image = freestyleButtonPhoto

def practiceHoverOff(arg):
	practiceButton.configure(image = practiceButtonPhoto)
	practiceButton.image = practiceButtonPhoto	

def backToHomeScreen():
	practiceButton.pack(side=RIGHT, padx=100)
	freestyleButton.pack(side=LEFT, padx=50, pady=100)
	text.pack_forget()
	backHomeButton.pack_forget()
	keyOption.pack_forget()
	modeOption.pack_forget()
	okButton.pack_forget()
	practiceText.pack_forget()
	optionsWidget.pack_forget()

def practiceMode():
	freestyleButton.pack_forget()
	practiceButton.pack_forget()	
	optionsWidget.pack(pady=50)
	keyOption.pack(side=LEFT)
	modeOption.pack(side=RIGHT)
	backHomeButton.pack()
	okButton.pack()

def practiceModeNext():
	global practiceText
	msg = "You've selected practice mode in the key of {0} {1}\nPlaying notes in key will turn the blender on!".format(selectedKey.get(), selectedMode.get())
	practiceText = ttk.Label(mainframe, text=msg, fg="#FFFFFF", bg="#000000", pady=60, font=("courier",32))
	keyOption.pack_forget()
	modeOption.pack_forget()
	okButton.pack_forget()
	backHomeButton.pack_forget()
	optionsWidget.pack_forget()
	practiceText.pack()
	backHomeButton.pack()

def freestyleMode():
	freestyleButton.pack_forget()
	practiceButton.pack_forget()
	text.pack()
	backHomeButton.pack()

root = Tk()
root.title("Sports & Play")
root.configure(background="#000000")
root.maxsize(width=winWidth, height=winHeight)
root.minsize(width=winWidth, height=winHeight)
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.configure(background="#000000")

mainPhoto = ttk.PhotoImage(file="../images/rockblend.png")
pic = ttk.Label(mainframe, image=mainPhoto, fg="#000000", bg="#000000")
pic.pack(padx=(winWidth-mainImageWidth)/2)

# Buttons #
freestyleButtonPhoto = ttk.PhotoImage(file="../images/freestylehoverblack.png")
freestyleButtonPhotoHover = ttk.PhotoImage(file="../images/freestyleblack.png")
freestyleButton = ttk.Button(mainframe, image=freestyleButtonPhoto, fg="#000000", bg="#000000", command=freestyleMode)
freestyleButton.bind('<Enter>', freestyleHoverOn)
freestyleButton.bind('<Leave>', freestyleHoverOff)
freestyleButton.pack(side=LEFT, padx=50, pady=100)

practiceButtonPhoto = ttk.PhotoImage(file="../images/practicehoverblack.png")
practiceButtonPhotoHover = ttk.PhotoImage(file="../images/practiceblack.png")
practiceButton = ttk.Button(mainframe, image=practiceButtonPhoto, fg="#000000", bg="#000000", command=practiceMode)
practiceButton.bind('<Enter>', practiceHoverOn)
practiceButton.bind('<Leave>', practiceHoverOff)
practiceButton.pack(side=RIGHT, padx=100)

#Freestyle page stuff
backHomeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=backToHomeScreen)
text = ttk.Label(mainframe, text="Freestyle mode\nTime to melt some faces!", fg="#FFFFFF", bg="#000000", pady=60, font=("courier",32))

#Practice page stuff
optionsWidget = ttk.Canvas(mainframe)
optionsWidget.configure(background="#000000")
selectedKey = ttk.StringVar(mainframe)
selectedKey.set("C") # initial value
keyOption = ttk.OptionMenu(optionsWidget, selectedKey, "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
selectedMode = ttk.StringVar(mainframe)
selectedMode.set("Major") # initial value
modeOption = ttk.OptionMenu(optionsWidget, selectedMode, "Major", "Minor")
okButton = ttk.Button(mainframe, text="OK", fg="#FFFFFF", bg="#000000", command=practiceModeNext)
practiceText = None

center(root) #must be at bottom
root.bind('<Return>', practiceMode)
root.mainloop()


