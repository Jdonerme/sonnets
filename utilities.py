import sys
import random
from sets import Set
from nltk.corpus import cmudict 
import numpy as np

SYLLABLE_DICT = cmudict.dict()
PUNCTUATION = ",!?()'.:;"
def append_to_dict_set(d, word_raw, rhyme_raw, repeat=True):
    word = word_raw.strip(PUNCTUATION)
    rhyme = rhyme_raw.strip(PUNCTUATION)
    if rhyme is None:
        return d
    if word in d:
        d[word] |= set([rhyme])
    else:
        d[word] = set([rhyme])
    if rhyme in d:
            d[word] |= d[rhyme]
    if repeat:
        d = append_to_dict_set(d, rhyme, word, False)
    if word in d[word]:
        temp = d[word]
        temp.remove(word)
        d[word] = temp
    return d


def import_shakespeare(linear=False, file="shakespeare.txt"):
    ''' imports a txt file in the format given of the shakespeare files.

        Imports the file by constructing a 2D array where each element in
        the array contains a line of a sonnet.
        Each line contains a list of numbers with each number mapping to 
        a specific word. Words with punctuation are kept together for now.
        Returns the sonnets array, word_map, and num_map.
        (word_map maps words to numbers and num_maps vice versa)

        '''
    LINES_IN_POEM = 14
    lines = []
    num_unique_words = 0
    word_map = {}
    num_map = {}
    rhyme_dict = {}
    line_index = 1
    prev_rhymes = [None, None]
    with open(file) as f:
        for line in f:
            line_split = line.strip('\n').split(" ")
            if '' in line_split:
                line_split = filter(lambda a: a != '', line_split)
            # account for some edge poems
            if line_split and line_split[0] == str(126):
               LINES_IN_POEM = 12
            elif line_split and line_split[0] == str(127):
                LINES_IN_POEM = 14
            if line_split and line_split[0] == str(99):
               LINES_IN_POEM = 15
            elif line_split and line_split[0] == str(100):
                LINES_IN_POEM = 14

            if len(line_split) > 2:
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
                if line_index == LINES_IN_POEM:
                    rhyme = prev_rhymes[1]
                    rhyme_dict = append_to_dict_set(rhyme_dict, word, rhyme)

                elif line_index in [3, 4, (LINES_IN_POEM - 7), (LINES_IN_POEM - 6), (LINES_IN_POEM - 3), (LINES_IN_POEM - 2)]:
                    rhyme = prev_rhymes[0]
                    rhyme_dict = append_to_dict_set(rhyme_dict, word, rhyme)
               	prev_rhymes[0] = prev_rhymes[1]
               	prev_rhymes[1] = word
                if not linear:
                        lines.append(coded_line)
               
            else: # we're done with the sonnet
                prev_rhymes[0], prev_rhymes[1] = None, None
                line_index = 0
            line_index += 1
    return lines, word_map, num_map, rhyme_dict

def generate_emission(A, O, num_map, num_lines=14, syl_per_line=[10] * 14):
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
        t = 0
        while t < syl_per_line[l]:
            # Sample next observation.
            next_obs = np.random.choice(range(len(O[state])), p=O[state])
            word = num_map[next_obs]
            num_syl = num_syllables(word)
            if t + num_syl <= syl_per_line[l]:
                if t == 0:
                    emission += word.capitalize() + ' '
                else:
                    emission += word + ' '
                t += num_syl

                # Sample next state.
                next_state = np.random.choice(range(len(A[state])), p=A[state])
                state = next_state
        emission += '\n'

    return emission

def num_syllables(word):
    temp = word.lower().strip(PUNCTUATION)
    try:
        return [len(list(y for y in x if y[-1].isdigit())) \
        for x in SYLLABLE_DICT[temp]][0]
    except Exception as e:
        if '-' in temp:
            sub_temp = temp.split('-')
            return sum([num_syllables(w) for w in sub_temp])
        elif temp.endswith("'s"):
            return num_syllables(temp.strip("'s"))
        elif len(temp) <= 5:
            return 1
        elif len(temp) <= 10:
            return 2
        else:
            return 3
        return 1
''' s, _, n, rhyme_dict = import_shakespeare
    for line in s[17*14:18*14]:
        for word in line:
            sys.stdout.write(str(n[word]) + " ")
        print '\n'
    print rhyme_dict['love']'''

'''s, _, num_map = import_shakespeare()
count = 0
for i in range(len(num_map)):
    #print num_map[i]

    val = num_syllables(num_map[i])
    if val == False:
        count += 1
    print count
'''
