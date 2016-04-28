import scales
import serialComm
import midiComm
import freestyleMode

practice = False
correctNotes = 0;
incorrectNotes = 0;
notes = []

def practiceListener():
	global notes
	global correctNotes
	global incorrectNotes
	global practice
	while 1:
		while practice == True and freestyle == False:
			if midiComm.inp.poll():
				# no way to find number of messages in queue
				# so we just specify a high max value
				msg = midiComm.inp.read(1000)
				if msg[0][0][2] == 100: #this is a note pressed event
					notePressed = int(msg[0][0][1])
					if notePressed in notes:
						correctNotes += 1
					else:
						incorrectNotes += 1	

def practiceBlenderState():
	global correctNotes
	global incorrectNotes
	while 1:
		while practice == True and freestyle == False:
			totalNotesPlayed = correctNotes + incorrectNotes
			if (totalNotesPlayed > 3):
				amountIncorrect = float(incorrectNotes) / float(totalNotesPlayed)
				if amountIncorrect < 0.2:
					serialComm.serialWrite('1')
				else:
					serialComm.serialWrite('0')
			else:
				serialComm.serialWrite('0')
			correctNotes = 0	
			incorrectNotes = 0
			time.sleep(2.5)

def startPracticeMode():
	global practice
	freestyleMode.stopFreestyleMode()
	practice = True

def stopPracticeMode():
	global practice
	serialComm.resetBlenderState()
	practice = False