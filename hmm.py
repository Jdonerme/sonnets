import utilities as ut
import numpy as np
from hmmlearn.hmm import MultinomialHMM
import sys
print 'getting the data'
NUM_WORDS = 300
lines, word_map, num_map = ut.import_shakespeare(linear=True)
lines = np.reshape(lines,(-1, 1))[:NUM_WORDS]
states = word_map.keys()
n_states = len(states)

print 'getting the model'
model = MultinomialHMM(n_components=NUM_WORDS)
print 'fitting'
model.fit(lines)
print 'sonnet:\n'
x = ut.generate_emission(8, model.transmat_, model.emissionprob_, num_map)
print("{:30}".format(x))