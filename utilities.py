import sys
import random
from sets import Set
from nltk.corpus import cmudict
import numpy as np
import re
import pronouncing
import json

SYLLABLE_DICT = cmudict.dict()
PUNCTUATION = ",!?()'.:;"
def append_to_dict_set(d, word_raw, rhyme_raw, repeat=True):
    word = word_raw.strip(PUNCTUATION)
    rhyme = rhyme_raw.strip(PUNCTUATION)
    if word == '' or rhyme == '':
        return d

    if rhyme is None:
        return d
    if word in d:
        for other_rhyme in d[word]:
            d[other_rhyme] |= set([rhyme])
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
            line_split = re.findall(r"[\w']+|[.,!?;:]", line.strip('\n'))
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
                    if word in PUNCTUATION:
                        word = line_split[-2].lower()
                    rhyme_dict = append_to_dict_set(rhyme_dict, word, rhyme)
                   
                elif (LINES_IN_POEM) == 12:
                    if line_index % 2 == 0 and line_index > 0:
                        rhyme = prev_rhymes[1]
                        if word in PUNCTUATION:
                            word = line_split[-2].lower()
                        rhyme_dict = append_to_dict_set(rhyme_dict, word, rhyme)
                        prev_rhymes[0] = prev_rhymes[1]

                elif line_index in [3, 4, (LINES_IN_POEM - 7), (LINES_IN_POEM - 6), (LINES_IN_POEM - 3), (LINES_IN_POEM - 2)]:
                    rhyme = prev_rhymes[0]
                    if word in PUNCTUATION:
                        word = line_split[-2].lower()
                    rhyme_dict = append_to_dict_set(rhyme_dict, word, rhyme)
               	prev_rhymes[0] = prev_rhymes[1]
                if word not in PUNCTUATION:
               	    prev_rhymes[1] = word
                else:
                    prev_rhymes[1] = line_split[-2].lower()
                if not linear:
                        lines.append(coded_line)

            else: # we're done with the sonnet
                prev_rhymes[0], prev_rhymes[1] = None, None
                line_index = 0
            line_index += 1
    return lines, word_map, num_map, rhyme_dict

def generate_emission(A, O, num_map, num_lines=14, syl_per_line=[10] * 14, rhyme_dict=None):
    '''
    Generates an emission of length M, assuming that the starting state
    is chosen uniformly at random.

    Arguments:
        M:          Length of the emission to generate.

    Returns:
        emission:   The randomly generated emission as a string.
    '''

    emission = ''
    prev_rhymes = [None, None]
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
                    # Lines should never start with punctuation
                    if word not in PUNCTUATION:
                        emission += word.capitalize()
                    
                elif t + num_syl == syl_per_line[l] and rhyme_dict:
                    if l in [2, 3, 6, 7, 10, 11, 13]:
                        to_add = []
                        prev = prev_rhymes[0]
                        if l == 13:
                            prev = prev_rhymes[1]
                        if prev in rhyme_dict:
                            for rhyme in rhyme_dict[prev]:
                                if num_syllables(rhyme) == num_syl:
                                    to_add.append(rhyme)
                        if to_add == []:
                            all_rhymes = pronouncing.rhymes(prev)
                            common = list(set(num_map.values()).intersection(set(all_rhymes)))
                            if common != []:
                                for rhyme in common:
                                    if num_syllables(rhyme) == num_syl:
                                        to_add.append(rhyme)
                            else:
                                for rhyme in all_rhymes:
                                    if num_syllables(rhyme) == num_syl:
                                        to_add.append(rhyme)

                        if to_add != []:
                            word = np.random.choice(to_add)
                            
                    emission += ' ' + word
                    prev_rhymes[0] = prev_rhymes[1]
                    prev_rhymes[1] = word.lower().strip(PUNCTUATION)

                else:
                    # Lines shouldn't include this punctuation in the middle
                    if word not in PUNCTUATION:
                        emission += ' ' + word
                    elif word in ',!:;':
                       if emission[-1] not in PUNCTUATION:
                             emission +=  word

                t += num_syl

                # Sample next state.
                next_state = np.random.choice(range(len(A[state])), p=A[state])
                state = next_state
        if word in '!.,:;?':
            emission += word
        else:
            if l == num_lines-1:
                emission += '.'
            else:
                emission += ','
        emission += '\n'

    return emission

def num_syllables(word):
    temp = word.lower().strip(PUNCTUATION)
    try:
        if temp == "":
            return 0
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
def print_rhyme_dict():
    _, _, _, rhyme_dict = import_shakespeare()
    new_dict = {}
    for key, val in rhyme_dict.iteritems():
        new_dict[key] = list(val)
    with open('output.txt', 'w') as f:
        json.dump(new_dict, f)

'''def main():
    s, _, n, rhyme_dict = import_shakespeare()
    #for line in s[17*14:18*14]:
    #    for word in line:
    #       sys.stdout.write(str(n[word]) + " ")
    #    print '\n'
    return rhyme_dict
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
