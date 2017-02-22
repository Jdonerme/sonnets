import sys
import random
from nltk.corpus import cmudict 

SYLLABLE_DICT = cmudict.dict()
PUNCTUATION = ",!?()'.:;"

def import_shakespeare(linear=False, file="shakespeare.txt"):
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
                for word_raw in line_split:
                    word = word_raw.lower()
                    if word in word_map.keys():
                        if not linear:
                            coded_line.append(word_map[word])
                        else:
                            lines.append(word_map[word])
                    else:
                        if not linear:
                            coded_line.append(num_unique_words)
                        else:
                            lines.append(num_unique_words)
                        word_map[word] = num_unique_words
                        num_map[num_unique_words] = word
                        num_unique_words += 1
                if not linear:
                    lines.append(coded_line)
    return lines, word_map, num_map

def generate_emission(M, A, O, num_map, num_lines=14):
    '''
    Generates an emission of length M, assuming that the starting state
    is chosen uniformly at random.

    Arguments:
        M:          Length of the emission to generate.

    Returns:
        emission:   The randomly generated emission as a string.
    '''

    emission = ''
    L = len(A)
    state = random.choice(range(L))

    for l in range(num_lines):
        for t in range(M):
            # Sample next observation.
            rand_var = random.uniform(0, 1)
            next_obs = 0

            while rand_var > 0:
                rand_var -= O[state][next_obs]
                next_obs += 1

            next_obs -= 1
            if t == 0:
                emission += num_map[next_obs].capitalize() + ' '
            else:
                emission += num_map[next_obs] + ' '

            # Sample next state.
            rand_var = random.uniform(0, 1)
            next_state = 0

            while rand_var > 0:
                rand_var -= A[state][next_state]
                next_state += 1

            next_state -= 1
            state = next_state
        emission += '\n'

    return emission

def num_syllables(word):
    try:
        temp = word.strip(PUNCTUATION)
        return [len(list(y for y in x if y[-1].isdigit())) \
        for x in SYLLABLE_DICT[temp]][0]
    except Exception as e:
        return 1

''' example use case: writing sonnet 18
s, _, n= import_shakespeare()

for line in s[17*14:18*14]:
    for word in line:
        sys.stdout.write(str(n[word]) + " ")
    print '\n' 
'''

'''s, _, num_map = import_shakespeare()
count = 0
for i in range(len(num_map)):
    #print num_map[i]

    val = num_syllables(num_map[i])
    if val == False:
        count += 1
    print count
'''
