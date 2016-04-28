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