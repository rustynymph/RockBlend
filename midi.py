import sys, pygame, pygame.midi, serial, time

# set up pygame
pygame.init()
pygame.midi.init()

ser = serial.Serial('/dev/ttyACM6', 9600)

lastNotePlayed = 0;
timeNotePlayed = 0;
timeDiff = 1;

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
	print pygame.midi.get_device_info(x)

# open a specific midi device
inp = pygame.midi.Input(3)

# run the event loop
while True:
	if (timeDiff < 1):
		ser.write('1')
	else:
		ser.write('0')
	if inp.poll():
		# no way to find number of messages in queue
		# so we just specify a high max value
		msg = inp.read(1000)
		if msg[0][0][2] == 100:
			lastNotePlayed = timeNotePlayed
			timeNotePlayed = time.time()
			timeDiff = timeNotePlayed - lastNotePlayed
			print timeDiff
			
# wait 10ms - this is arbitrary, but wait(0) still resulted
# in 100% cpu utilization
pygame.time.wait(10)
