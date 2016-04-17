from Tkinter import *
import Tkinter as ttk
import os, sys, pygame, pygame.midi, serial, time, threading

# =========================================== #
			#Midi & blender stuff
# =========================================== #

ser = None
inp = None
notesPlayed = 0;
correctNotes = 0;
incorrectNotes = 0;
notes = []
practice = False
freestyle = False

def resetBlenderState():
	global notesPlayed
	global correctNotes
	global incorrectNotes
	notesPlayed = 0;
	correctNotes = 0;
	incorrectNotes = 0;
	serialWrite('0')

def freestyleBlenderState():
	global notesPlayed
	while 1:
		while freestyle == True and practice == False:
			avgCount = notesPlayed / 4
			if avgCount >= 2:
				serialWrite('1')
			else:
				serialWrite('0')
			notesPlayed = 0
			time.sleep(2.0)

def practiceBlenderState():
	global correctNotes
	global incorrectNotes
	while 1:
		while practice == True and freestyle == False:
			totalNotesPlayed = correctNotes + incorrectNotes
			if (totalNotesPlayed > 3):
				amountIncorrect = float(incorrectNotes) / float(totalNotesPlayed)
				if amountIncorrect < 0.2:
					serialWrite('1')
				else:
					serialWrite('0')
			else:
				serialWrite('0')
			correctNotes = 0	
			incorrectNotes = 0
			time.sleep(2.5)

def serialWrite(msg):
	global ser
	ser.write(msg)
	if msg == '0':
		state = 'off'
	else:
		state = 'on'
	blenderState.configure(text="Blender is: {0}".format(state))


def freestyleListener():
	global inp
	global notesPlayed
	global freestyle
	while 1:
		while freestyle == True and practice == False:
			if inp.poll():
				# no way to find number of messages in queue
				# so we just specify a high max value
				msg = inp.read(1000)
				if msg[0][0][2] == 100: #this is a note pressed event
					notesPlayed += 1
		

def practiceListener():
	global inp
	global notes
	global correctNotes
	global incorrectNotes
	global practice
	while 1:
		while practice == True and freestyle == False:
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

def phrygianDominantHelper(fifthNote):
	pitches = {'c':60, 'c#':61, 'd':62, 'd#':63, 'e':64, 'f':65, 'f#':66, 'g':67, 'g#':68, 'a':69, 'a#':70, 'b':71}
	for key,val in pitches.items():
		if ((val+7 == fifthNote) or (val+7 == fifthNote-12) or (val+7 == fifthNote+12)):
			return val


def initMidiScales(key, scale):
	global notes
	pitches = {'c':60, 'c#':61, 'd':62, 'd#':63, 'e':64, 'f':65, 'f#':66, 'g':67, 'g#':68, 'a':69, 'a#':70, 'b':71}
	middleNote = pitches[key]
	notes = []
	octaves = []
	# major = W-W-H-W-W-W-H
	majorScale = [middleNote, middleNote+2, middleNote+4, middleNote+5, middleNote+7, middleNote+9, middleNote+11]
	# minor = W-H-W-W-H-W-W
	minorScale = [middleNote, middleNote+2, middleNote+3, middleNote+5, middleNote+7, middleNote+8, middleNote+10]
	if scale == 'major':
		notes += majorScale
	elif scale == 'minor':
		notes += minorScale
	elif scale == 'major pentatonic': #1,2,3,5,6 of major scale
		notes += [majorScale[0], majorScale[1], majorScale[2], majorScale[4], majorScale[5]]
	elif scale == 'minor pentatonic': #1,3,4,5,7 of natural minor scale
		notes += [minorScale[0], minorScale[2], minorScale[3], minorScale[4], minorScale[6]]
	elif scale == 'harmonic minor': #same as minor scale but 7th is raised 1 semitone
		notes += minorScale
		notes[6] = notes[6] + 1
	elif scale == 'mixolydian mode': #same as major scale but 7th is lowered 1 semitone
		notes += majorScale
		notes[6] = notes[6] - 1
	elif scale == 'phrygian mode': #same as natural minor scale but 2nd is lowered 1 semitone
		notes += minorScale
		notes[1] = notes[1] - 1
	elif scale == 'phrygian dominant': #same as the harmonic minor of which this note is the fifth. ex) E phrygian dominant = A harmonic minor 
		note = phrygianDominantHelper(middleNote)
		harmonicMinorScale = [note, note+2, note+3, note+5, note+7, note+8, note+11]
		notes += harmonicMinorScale
	for note in notes:
		octaves += [note-12, note-24, note+12, note+24]

	notes += octaves


def tryReconnectingSerialConn(portNum):
	global midiConnected
	try:
		initSerialConn(portNum)
	except:
		errorMsg.pack_forget()
		portOption.pack_forget()
		selectPortButton.pack_forget()	
		blenderState.pack_forget()
		errorMsg.config(text="Serial port /dev/ttyACM{} not found\ntry selecting another port OR\n double check your Arduino is plugged in".format(portNum))
		chooseDifferentSerialPort()
	else:
		if (midiConnected == False):
			midiError()
		else:
			backToHomeScreen()

def initSerialConn(portNum):
	global ser
	serialPort = '/dev/ttyACM{0}'.format(portNum)
	ser = serial.Serial(serialPort, 9600)

def initPygame():
	global inp
	pygame.init()
	pygame.midi.init()
	inp = pygame.midi.Input(3)	
	pygame.time.wait(10)	


def startPracticeMode():
	global practice
	stopFreestyleMode()
	practice = True

def startFreestyleMode():
	global freestyle
	stopPracticeMode()
	freestyle = True

def stopPracticeMode():
	global practice
	resetBlenderState()
	practice = False

def stopFreestyleMode():
	global freestyle
	resetBlenderState()
	freestyle = False


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
		freestyleThread = threading.Thread(target=freestyleListener, args=())
		freestyleThread.daemon = True
		freestyleThread.start()

		practiceThread = threading.Thread(target=practiceListener, args=())
		practiceThread.daemon = True
		practiceThread.start()

		startFBSthread = threading.Thread(target=freestyleBlenderState, args=())
		startFBSthread.daemon = True
		startFBSthread.start()

		startFBSthread = threading.Thread(target=practiceBlenderState, args=())
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
	stopFreestyleMode()
	stopPracticeMode()
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

def practiceMode():
	stopPracticeMode()
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
	startPracticeMode()

def freestyleMode():
	selectModeText.pack_forget()
	freestyleButton.pack_forget()
	practiceButton.pack_forget()
	blenderState.pack_forget()
	text.pack()
	blenderState.pack()
	backHomeButton.pack()
	startFreestyleMode()

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

mainPhoto = ttk.PhotoImage(file="images/rockblend.png")
pic = ttk.Label(mainframe, image=mainPhoto, fg="#000000", bg="#000000")
pic.pack(padx=(winWidth-mainImageWidth)/2)
selectModeText = ttk.Label(mainframe, text="Select mode:", fg="#FFFFFF", bg="#000000", pady=40, font=("courier",20))

# Buttons #
freestyleButtonPhoto = ttk.PhotoImage(file="images/freestylehoverblack.png")
freestyleButtonPhotoHover = ttk.PhotoImage(file="images/freestyleblack.png")
freestyleButton = ttk.Button(mainframe, image=freestyleButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, \
	highlightthickness=0, highlightcolor="#000000", highlightbackground="#000000", command=freestyleMode)
freestyleButton.bind('<Enter>', freestyleHoverOn)
freestyleButton.bind('<Leave>', freestyleHoverOff)

practiceButtonPhoto = ttk.PhotoImage(file="images/practicehoverblack.png")
practiceButtonPhotoHover = ttk.PhotoImage(file="images/practiceblack.png")
practiceButton = ttk.Button(mainframe, image=practiceButtonPhoto, fg="#000000", bg="#000000", borderwidth=0, \
	highlightthickness=0, highlightcolor="#000000", highlightbackground="#000000", command=practiceMode)
practiceButton.bind('<Enter>', practiceHoverOn)
practiceButton.bind('<Leave>', practiceHoverOff)

#Freestyle page stuff
backHomeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=backToHomeScreen)
backToPracticeButton = ttk.Button(mainframe, text="Go back", fg="#FFFFFF", bg="#000000", command=practiceMode)
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
	global inp
	global ser
	root.destroy()
	if inp:
		inp.close()
	if ser:
		ser.close()
	exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<Return>', practiceMode)
root.mainloop()




