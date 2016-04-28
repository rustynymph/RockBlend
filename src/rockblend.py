import serialComm
import midiComm
import freestyleMode 
import practiceMode
from Tkinter import *
import Tkinter as ttk
import os, sys, serial, time, threading

# =========================================== #
			#Midi & blender stuff
# =========================================== #
try:
	initSerialConn(0) #initialize serial port, zero is default
except:
	serConnected = False
else:
	serConnected = True
	try:
		initPygame() #initialize connection with keyboard
	except:
		midiConnected = False
	else:
		midiConnected = True

# if we've connected to serial & midi initialize all worker threads
freestyleThread = threading.Thread(target=freestyleMode.freestyleListener, args=())
freestyleThread.daemon = True
freestyleThread.start()

practiceThread = threading.Thread(target=practiceMode.practiceListener, args=())
practiceThread.daemon = True
practiceThread.start()

startFBSthread = threading.Thread(target=freestyleMode.freestyleBlenderState, args=())
startFBSthread.daemon = True
startFBSthread.start()

startFBSthread = threading.Thread(target=practiceMode.practiceBlenderState, args=())
startFBSthread.daemon = True
startFBSthread.start()

#=========================================== #
			#Tkinter stuff
#=========================================== #

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

def chooseDifferentSerialPort():
	errorMsg.pack_forget()
	portOption.pack_forget()
	blenderState.pack_forget()
	selectPortButton.pack_forget()	
	errorMsg.pack()
	portOption.pack()
	selectPortButton.pack()

def midiError():
	errorMsg.pack_forget()
	portOption.pack_forget()
	blenderState.pack_forget()
	selectPortButton.pack_forget()	
	errorMsg.configure(text="Could not connect to MIDI device...\nis your keyboard plugged in\nand turned on?")
	errorMsg.pack()

def backToHomeScreen():
	freestyleMode.stopFreestyleMode()
	practiceMode.stopPracticeMode()
	selectModeText.pack()
	practiceButton.pack(side=RIGHT, padx=100)
	freestyleButton.pack(side=LEFT, padx=50)
	text.pack_forget()
	backHomeButton.pack_forget()
	keyOption.pack_forget()
	scaleOption.pack_forget()
	okButton.pack_forget()
	errorMsg.pack_forget()
	blenderState.pack_forget()
	portOption.pack_forget()
	selectPortButton.pack_forget()
	if practiceText:
		practiceText.pack_forget()
	optionsWidget.pack_forget()

def practiceModeScreen():
	practiceMode.stopPracticeMode()
	backToPracticeButton.pack_forget()
	selectModeText.pack_forget()
	freestyleButton.pack_forget()
	practiceButton.pack_forget()
	blenderState.pack_forget()
	if practiceText:
		practiceText.pack_forget()
	optionsWidget.pack(pady=50)
	keyOption.pack(side=LEFT)
	scaleOption.pack(side=RIGHT)
	backHomeButton.pack()
	okButton.pack()

def practiceModeNext():
	global practiceText
	key = selectedKey.get()
	scale = selectedScale.get()
	msg = "You've selected practice mode in the key of {0} {1}\nPlaying notes in key will turn the blender on!".format(key, scale)
	practiceText = ttk.Label(mainframe, text=msg, fg="#FFFFFF", bg="#000000", pady=30, font=("courier",25))
	keyOption.pack_forget()
	backHomeButton.pack_forget()
	scaleOption.pack_forget()
	okButton.pack_forget()
	blenderState.pack_forget()
	optionsWidget.pack_forget()
	practiceText.pack()
	blenderState.pack()
	backToPracticeButton.pack()
	initMidiScales(key.lower(), scale.lower())
	practiceMode.startPracticeMode()

def freestyleModeScreen():
	selectModeText.pack_forget()
	freestyleButton.pack_forget()
	practiceButton.pack_forget()
	blenderState.pack_forget()
	text.pack()
	blenderState.pack()
	backHomeButton.pack()
	freestyleMode.startFreestyleMode()

root = Tk()
root.title("RockBlend")
root.configure(background="#000000")
root.maxsize(width=winWidth, height=winHeight)
root.minsize(width=winWidth, height=winHeight)
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.configure(background="#000000", highlightthickness=0)

mainPhoto = ttk.PhotoImage(file="../images/rockblend.png")
pic = ttk.Label(mainframe, image=mainPhoto, fg="#000000", bg="#000000")
pic.pack(padx=(winWidth-mainImageWidth)/2)
selectModeText = ttk.Label(mainframe, text="Select mode:", fg="#FFFFFF", bg="#000000", pady=40, font=("courier",20))

# Buttons #
freestyleButtonPhoto = ttk.PhotoImage(file="../images/freestylehoverblack.png")
freestyleButtonPhotoHover = ttk.PhotoImage(file="../images/freestyleblack.png")
freestyleButton = ttk.Button(mainframe, image=freestyleButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, \
	highlightthickness=0, highlightcolor="#000000", highlightbackground="#000000", command=freestyleModeScreen)
freestyleButton.bind('<Enter>', freestyleHoverOn)
freestyleButton.bind('<Leave>', freestyleHoverOff)

practiceButtonPhoto = ttk.PhotoImage(file="../images/practicehoverblack.png")
practiceButtonPhotoHover = ttk.PhotoImage(file="../images/practiceblack.png")
practiceButton = ttk.Button(mainframe, image=practiceButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, \
	highlightthickness=0, highlightcolor="#000000", highlightbackground="#000000", command=practiceModeScreen)
practiceButton.bind('<Enter>', practiceHoverOn)
practiceButton.bind('<Leave>', practiceHoverOff)

#Freestyle page stuff
backHomeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=backToHomeScreen)
backToPracticeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=practiceModeScreen)
text = ttk.Label(mainframe, text="Freestyle mode\nTime to melt some faces!", fg="#FFFFFF", bg="#000000", pady=30, font=("courier",32))

#Practice page stuff
optionsWidget = ttk.Canvas(mainframe)
optionsWidget.configure(background="#000000")
selectedKey = ttk.StringVar(mainframe)
selectedKey.set("C") # initial value
keyOption = ttk.OptionMenu(optionsWidget, selectedKey, "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
selectedScale = ttk.StringVar(mainframe)
selectedScale.set("Major") # initial value
scaleOption = ttk.OptionMenu(optionsWidget, selectedScale, "Major", "Minor", "Major Pentatonic", "Minor Pentatonic", "Harmonic Minor", "Mixolydian Mode", "Phrygian Mode", "Phrygian Dominant")
okButton = ttk.Button(mainframe, text="OK", fg="#FFFFFF", bg="#000000", command=practiceModeNext)
practiceText = None

#Blender state label
blenderState = ttk.Label(mainframe, text="Blender is: off", fg="#FFFFFF", bg="#000000", font=("courier",32))

#Settings page
errorMsg = ttk.Label(mainframe, text="Serial port /dev/ttyACM0 not found\ntry selecting another port OR\n double check your Arduino is plugged in", fg="#FFFFFF", bg="#000000", pady=60, font=("courier",25))
selectedPort = ttk.StringVar(mainframe)
selectedPort.set("ttyACM0") # initial value
portOption = ttk.OptionMenu(mainframe, selectedPort, "ttyACM0", "ttyACM1", "ttyACM2", "ttyACM3", "ttyACM4", "ttyACM5", "ttyACM6", "ttyACM7", "ttyACM8", "ttyACM9")
selectPortButton = ttk.Button(mainframe, text="select port", fg="#FFFFFF", bg="#000000", command=lambda: tryReconnectingSerialConn(selectedPort.get()[-1]))

if(serConnected == False):
	chooseDifferentSerialPort()
else:
	if(midiConnected == False):
		midiError()
	else:
		backToHomeScreen()
		
center(root) #must be at bottom

def on_closing():
	root.destroy()
	if midiComm.inp:
		midiComm.inp.close()
	if serialComm.ser:
		serialComm.ser.close()
	exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()




