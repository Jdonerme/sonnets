import sys
def import_shakespeare(file="shakespeare.txt"):
	''' imports a txt file in the format given of the shakespeare files.

		Imports the file by constructing a 2D array where each element in
		the array contains the lines of a sonnet.
		Each line contains a list of numbers with each number mapping to 
		a specific word. Words with punctuation are kept together for now.
		Returns the sonnets array, word_map, and num_map.
		(word_map maps words to numbers and num_maps vice versa)

		'''
	sonnets = []
	lines = []
	word_counter = 0
	word_map = {}
	num_map = {}
	with open(file) as f:
		for line in f:
			line_split = line.strip('\n').split(" ")
			if '' in line_split:
				line_split = filter(lambda a: a != '', line_split)
				
			if len(line_split) > 1:
				coded_line = []
				for word in line_split:
					if word in word_map.keys():
						coded_line.append(word_map[word])
					else:
						coded_line.append(word_counter)
						word_map[word] = word_counter
						num_map[word_counter] = word
						word_counter += 1
				lines.append(coded_line)
				if len(lines) == 14:
					sonnets.append(lines)
					lines = []
	return sonnets, word_map, num_map
'''s, w, n= import_shakespeare()
for line in s[8]:
	for word in line:
		sys.stdout.write(str(n[word]) + " ")
	print '\n' '''

