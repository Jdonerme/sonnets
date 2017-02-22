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
print 'yay'
for _ in range(14):
    seed = np.random.randint(0, NUM_WORDS)
    model.random_state = seed
    samples = model.sample(n_samples=8)[1]
    for state in samples:
        word = num_map[state]
        if state == samples[0]:
            word = word.capitalize()
        sys.stdout.write(word + ' ')
    print
