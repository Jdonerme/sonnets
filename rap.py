import utilities as ut
import numpy as np
from hmmlearn.hmm import MultinomialHMM
import sys

print 'getting the data'
lines, word_map, num_map, rhyme_dict = ut.import_general(file="rap.txt", linear=True)
lines = np.reshape(lines,(-1, 1))

print 'getting the model'
model = MultinomialHMM(n_components=10, n_iter=5000)
print 'fitting'
model.fit(lines)
print 'Rap:'
x = ut.generate_rap(model.transmat_, model.emissionprob_, num_map)
print("{:30}".format(x))



print 'visualizing'
ut.visualize(model.transmat_, model.emissionprob_, num_map)