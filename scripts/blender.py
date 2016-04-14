from Tkinter import *
import Tkinter as ttk
import os, sys, pygame, pygame.midi, serial, time, threading
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
	selectModeText.pack()
	practiceButton.pack(side=RIGHT, padx=100)
	freestyleButton.pack(side=LEFT, padx=50)
	text.pack_forget()
	backHomeButton.pack_forget()
	keyOption.pack_forget()
	modeOption.pack_forget()
	okButton.pack_forget()
	if practiceText:
		practiceText.pack_forget()
	optionsWidget.pack_forget()

def practiceMode():
	backToPracticeButton.pack_forget()
	selectModeText.pack_forget()
	freestyleButton.pack_forget()
	practiceButton.pack_forget()
	if practiceText:
		practiceText.pack_forget()
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
	backHomeButton.pack_forget()
	modeOption.pack_forget()
	okButton.pack_forget()
	optionsWidget.pack_forget()
	practiceText.pack()
	backToPracticeButton.pack()

def freestyleMode():
	selectModeText.pack_forget()
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
mainframe.configure(background="#000000", highlightthickness=0)

mainPhoto = ttk.PhotoImage(file="../images/rockblend.png")
pic = ttk.Label(mainframe, image=mainPhoto, fg="#000000", bg="#000000")
pic.pack(padx=(winWidth-mainImageWidth)/2)
selectModeText = ttk.Label(mainframe, text="Select mode:", fg="#FFFFFF", bg="#000000", pady=40, font=("courier",20))
selectModeText.pack()

# Buttons #
freestyleButtonPhoto = ttk.PhotoImage(file="../images/freestylehoverblack.png")
freestyleButtonPhotoHover = ttk.PhotoImage(file="../images/freestyleblack.png")
freestyleButton = ttk.Button(mainframe, image=freestyleButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, highlightthickness=0, command=freestyleMode)
freestyleButton.bind('<Enter>', freestyleHoverOn)
freestyleButton.bind('<Leave>', freestyleHoverOff)
freestyleButton.pack(side=LEFT, padx=50)

practiceButtonPhoto = ttk.PhotoImage(file="../images/practicehoverblack.png")
practiceButtonPhotoHover = ttk.PhotoImage(file="../images/practiceblack.png")
practiceButton = ttk.Button(mainframe, image=practiceButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, highlightthickness=0, command=practiceMode)
practiceButton.bind('<Enter>', practiceHoverOn)
practiceButton.bind('<Leave>', practiceHoverOff)
practiceButton.pack(side=RIGHT, padx=100)

#Freestyle page stuff
backHomeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=backToHomeScreen)
backToPracticeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=practiceMode)
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







# =========================================== #
			#Midi & blender stuff
# =========================================== #

ser = None
notesPlayed = 0;
correctNotes = 0;
incorrectNotes = 0;
notes = []

def freestyleBlenderState():
	global notesPlayed
	threading.Timer(2.0, freestyleBlenderState).start()
	avgCount = notesPlayed / 4
	if avgCount >= 1:
		#print "on"
		serialWrite('1')
	else:
		#print "off"
		serialWrite('0')
	notesPlayed = 0

def practiceBlenderState():
	global correctNotes
	global incorrectNotes
	threading.Timer(2.5, practiceBlenderState).start()
	totalNotesPlayed = correctNotes + incorrectNotes
	if (totalNotesPlayed > 0):
		amountIncorrect = float(incorrectNotes) / float(totalNotesPlayed)
		if amountIncorrect < 0.2:
			#print "on"
			serialWrite('1')
		else:
			#print "off"
			serialWrite('0')
	else:
		#print "off"
		serialWrite('0')
	correctNotes = 0	
	incorrectNotes = 0	

def serialWrite(msg):
	global ser
	ser.write(msg)

def freestyleListener(inp):
	global notesPlayed
	while True:
		if inp.poll():
			# no way to find number of messages in queue
			# so we just specify a high max value
			msg = inp.read(1000)
			if msg[0][0][2] == 100: #this is a note pressed event
				notesPlayed += 1

def practiceListener(inp):
	global notes
	global correctNotes
	global incorrectNotes
	while True:
		if inp.poll():
			# no way to find number of messages in queue
			# so we just specify a high max value
			msg = inp.read(1000)
			if msg[0][0][2] == 100: #this is a note pressed event
				notePressed = int(msg[0][0][1])
				if notePressed in notes:
					correctNotes += 1
				else:
					incorrectNotes += 1	

def initMidiScales(key, mode):
	global notes
	pitches = {'c':60, 'c#':61, 'd':62, 'd#':63, 'e':64, 'f':65, 'f#':66, 'g':67, 'g#':68, 'a':69, 'a#':70, 'b':71}
	middleNote = pitches[key]
	octaves = []
	# major = W-W-H-W-W-W-H
	# minor = W-H-W-W-H-W-W
	if mode == 'major':
		notes += [middleNote, middleNote+2, middleNote+4, middleNote+5, middleNote+7, middleNote+9, middleNote+11]
	else:
		notes += [middleNote, middleNote+2, middleNote+3, middleNote+5, middleNote+7, middleNote+8, middleNote+10]
		
	for note in notes:
		octaves += [note-12, note-24, note+12, note+24]

	notes += octaves


def initSerialConn():
	global ser
	serialPort = '/dev/ttyACM0'
	ser = serial.Serial(serialPort, 9600)

def initPygame():
	pygame.init()
	pygame.midi.init()
	# list all midi devices
	#for x in range( 0, pygame.midi.get_count() ):
	#	print pygame.midi.get_device_info(x)

	# open a specific midi device
	inp = pygame.midi.Input(3)	
	# wait 10ms - this is arbitrary, but wait(0) still resulted
	# in 100% cpu utilization
	pygame.time.wait(10)	

def startFreestyleMode():
	midiThread = threading.Thread(target=freestyleListener, args=(inp,))
	midiThread.daemon = True
	midiThread.start()
	freestyleBlenderState()

def startPracticeMode():
	initMidiScales(key, mode)
	midiThread = threading.Thread(target=practiceListener, args=(inp,))
	midiThread.daemon = True
	midiThread.start()
	practiceBlenderState()

		


