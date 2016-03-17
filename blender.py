from Tkinter import *
import Tkinter as ttk

def selectKey(*args):
	keylabel.pack_forget()
	keyoption.pack_forget()	
	selectMode.pack_forget()
	modeOption.pack_forget()
	modeButton.pack_forget()	
	goButton.pack_forget()
	backButton.pack_forget()
	cMajorLabel.pack_forget()

	keyChoice = str(key.get())
	if keyChoice == "C Major":
		cMajorLabel.pack()


def changeMode(*args):
	mode = str(var.get())
	keylabel.pack_forget()
	keyoption.pack_forget()	
	goButton.pack_forget()
	selectMode.pack_forget()
	modeOption.pack_forget()
	modeButton.pack_forget()
	cMajorLabel.pack_forget()

	if mode == "Practice":
		keylabel.pack()
		keyoption.pack()
		goButton.pack()

	backButton.pack()
	center(root) #must be at bottom

def goBack(*args):
	keylabel.pack_forget()
	keyoption.pack_forget()	
	selectMode.pack_forget()
	modeOption.pack_forget()
	modeButton.pack_forget()	
	goButton.pack_forget()
	selectMode.pack()
	modeOption.pack()
	modeButton.pack()	
	backButton.pack_forget()
	cMajorLabel.pack_forget()

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = Tk()
root.title("Sports & Play")

root.configure(background="#000000")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.configure(background="#000000")

photo = ttk.PhotoImage(file="images/piano.png")
pic = ttk.Label(mainframe, image=photo)
#pic.pack()

#Select mode widgets
selectMode = ttk.Label(mainframe, text="SELECT MODE:", fg="#a1dbcd", bg="#000000", font=("Century Gothic", 50))
selectMode.pack()
var = StringVar(mainframe)
var.set("Freestyle")
modeOption = OptionMenu(mainframe, var, "Freestyle", "Practice")
modeOption.configure(font=("Century Gothic", 20))
modeOption.pack()
modeButton = Button(mainframe, text="GO", command=changeMode, fg="#a1dbcd", bg="#383a39", font=("Century Gothic", 20))
modeButton.pack()

#Pracitce mode widgets
keylabel = ttk.Label(mainframe, text="SELECT KEY:", fg="#a1dbcd", bg="#000000", font=("Century Gothic", 50))
key = StringVar(mainframe)
key.set("C Major")
keyoption = OptionMenu(mainframe, key, "C Major", "E Major")
keyoption.configure(font=("Century Gothic", 20))
goButton = Button(mainframe, text="GO", command=selectKey, fg="#a1dbcd", bg="#383a39", font=("Century Gothic", 20))

backButton = Button(mainframe, text="GO BACK", command=goBack, fg="#a1dbcd", bg="#383a39", font=("Century Gothic", 20))

cMajor = "The C major scale consists of the \
pitches C, D, E, F, G, A, and B. Its key \
signature has no flats and no sharps. Its \
relative minor is A minor and its parallel \
minor is C minor."
cMajorLabel = ttk.Label(mainframe, text=cMajor, fg="#FFFFFF", bg="#000000", font=("Century Gothic", 10))

center(root) #must be at bottom

root.bind('<Return>', changeMode)

root.mainloop()


