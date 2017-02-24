import utilities as ut
import numpy as np
from hmmlearn.hmm import MultinomialHMM
import sys

print 'getting the data'
lines, word_map, num_map, rhyme_dict = ut.import_full(linear=True)
lines = np.reshape(lines,(-1, 1))
states = word_map.keys()
n_states = len(states)

print 'getting the model'
model = MultinomialHMM(n_components=6, n_iter=1500)
print 'fitting'
model.fit(lines)
print 'Sonnet:'
x = ut.generate_emission(model.transmat_, model.emissionprob_, num_map, rhyme_dict=rhyme_dict)
print("{:30}".format(x))

print 'Haiku:'
x = ut.generate_emission(model.transmat_, model.emissionprob_, num_map, 3, [5, 7, 5])
print("{:30}".format(x))

print 'visualizing'
ut.visualize(model.transmat_, model.emissionprob_, num_map)