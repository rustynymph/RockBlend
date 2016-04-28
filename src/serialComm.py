ser = None

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

def serialWrite(msg):
	global ser
	ser.write(msg)
	if msg == '0':
		state = 'off'
	else:
		state = 'on'
	blenderState.configure(text="Blender is: {0}".format(state))

def resetBlenderState():
	global notesPlayed
	global correctNotes
	global incorrectNotes
	notesPlayed = 0;
	correctNotes = 0;
	incorrectNotes = 0;
	serialWrite('0')
