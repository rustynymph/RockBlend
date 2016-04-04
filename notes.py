import sys, pygame, pygame.midi, serial, time, threading

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
	threading.Timer(3.0, practiceBlenderState).start()
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


def main(args):
	global ser
	key = None
	mode = None

	if len(args) < 2:
		print "USAGE: python notes.py <USB_PORT_NO> <KEY> <MODE>"
		print "You do not need to specify key and mode if you want to freestyle"
		exit(1)
	else:
		serialPort = '/dev/ttyACM{0}'.format(str(args[1]))
		ser = serial.Serial(serialPort, 9600)

	if (len(args) == 4):
		args[2] = args[2].lower()
		args[3] = args[3].lower()
		if (args[2] in ('a','b','c','d','e','f','g','a#','c#','d#','f#','g#')):
			key = args[2]
		if (args[3] in ('major','maj')):
			mode = 'major'
		elif (args[3] in ('minor', 'min')):
			mode = 'minor'

	# set up pygame
	pygame.init()
	pygame.midi.init()

	# list all midi devices
	for x in range( 0, pygame.midi.get_count() ):
		print pygame.midi.get_device_info(x)

	# open a specific midi device
	inp = pygame.midi.Input(3)	

	if (not(key and mode)):
		print "You are in FREESTYLE mode"
		midiThread = threading.Thread(target=freestyleListener, args=(inp,))
		midiThread.start()
		freestyleBlenderState()
	else:
		print "You are in PRACTICE mode"
		print "You have selected the key of {0} {1}".format(key, mode)
		initMidiScales(key, mode)
		midiThread = threading.Thread(target=practiceListener, args=(inp,))
		midiThread.start()
		practiceBlenderState()		

	# wait 10ms - this is arbitrary, but wait(0) still resulted
	# in 100% cpu utilization
	pygame.time.wait(10)	

if __name__ == "__main__":
	ser = None
	notesPlayed = 0;
	correctNotes = 0;
	incorrectNotes = 0;
	notes = []
	main(sys.argv)