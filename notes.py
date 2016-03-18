import sys, pygame, pygame.midi, serial, time, threading

def blenderState():
	global notesPlayed
	threading.Timer(2.0, blenderState).start()
	avgCount = notesPlayed / 4
	if avgCount >= 1:
		print "on"
		serialWrite('1')
	else:
		print "off"
		serialWrite('0')
	notesPlayed = 0

def serialWrite(msg):
	global ser
	ser.write(msg)

def midiListener(inp):
	global notesPlayed
	while True:
		if inp.poll():
			# no way to find number of messages in queue
			# so we just specify a high max value
			msg = inp.read(1000)
			if msg[0][0][2] == 100: #this is a note pressed event
				notesPlayed += 1

def main():
	# set up pygame
	pygame.init()
	pygame.midi.init()

	# list all midi devices
	for x in range( 0, pygame.midi.get_count() ):
		print pygame.midi.get_device_info(x)

	# open a specific midi device
	inp = pygame.midi.Input(3)	

	midiThread = threading.Thread(target=midiListener, args=(inp,))
	midiThread.start()

	blenderState()

	# wait 10ms - this is arbitrary, but wait(0) still resulted
	# in 100% cpu utilization
	pygame.time.wait(10)	

if __name__ == "__main__":
	ser = serial.Serial('/dev/ttyACM6', 9600)
	notesPlayed = 0;
	main()