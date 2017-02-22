def import_shakespeare(file="shakespeare.txt"):
	sonnets = []
	lines = []
	with open(file) as f:
		for line in f:
			line_split = line.strip('\n').split(" ")
			if '' in line_split:
				line_split = filter(lambda a: a != '', line_split)
				
			if len(line_split) > 1:
				lines.append(line_split)
				if len(lines) == 14:
					sonnets.append(lines)
					lines = []
	print sonnets[17]
import_shakespeare()

