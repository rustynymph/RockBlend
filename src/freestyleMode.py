import serialComm
import midiComm
import practiceMode

notesPlayed = 0;
freestyle = False

def freestyleListener():
	global notesPlayed
	global freestyle
	while 1:
		while freestyle == True and practice == False:
			if midiComm.inp.poll():
				# no way to find number of messages in queue
				# so we just specify a high max value
				msg = midiComm.inp.read(1000)
				if msg[0][0][2] == 100: #this is a note pressed event
					notesPlayed += 1

def freestyleBlenderState():
	global notesPlayed
	while 1:
		while freestyle == True and practice == False:
			avgCount = notesPlayed / 4
			if avgCount >= 2:
				serialComm.serialWrite('1')
			else:
				serialComm.serialWrite('0')
			notesPlayed = 0
			time.sleep(2.0)

def stopFreestyleMode():
	global freestyle
	serialComm.resetBlenderState()
	freestyle = False

def startFreestyleMode():
	global freestyle
	practiceMode.stopPracticeMode()
	freestyle = True