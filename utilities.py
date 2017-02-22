import sys
def import_shakespeare(file="shakespeare.txt"):
	''' imports a txt file in the format given of the shakespeare files.

		Imports the file by constructing a 2D array where each element in
		the array contains a line of a sonnet.
		Each line contains a list of numbers with each number mapping to 
		a specific word. Words with punctuation are kept together for now.
		Returns the sonnets array, word_map, and num_map.
		(word_map maps words to numbers and num_maps vice versa)

		'''
	lines = []
	num_unique_words = 0
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
						coded_line.append(num_unique_words)
						word_map[word] = num_unique_words
						num_map[num_unique_words] = word
						num_unique_words += 1
				lines.append(coded_line)
	return lines, word_map, num_map
''' example use case: writing sonnet 18
s, _, n= import_shakespeare()

for line in s[17*14:18*14]:
	for word in line:
		sys.stdout.write(str(n[word]) + " ")
	print '\n' 
''


