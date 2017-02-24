import utilities as ut
import numpy as np
from hmmlearn.hmm import MultinomialHMM
import sys

print 'getting the data'
lines, word_map, num_map, rhyme_dict = ut.import_shakespeare(linear=True)
lines = np.reshape(lines,(-1, 1))

print 'getting the model'
model = MultinomialHMM(n_components=8, n_iter=500)
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