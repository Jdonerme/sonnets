import utilities as ut
import numpy as np
from hmmlearn.hmm import MultinomialHMM

lines, word_map, num_map = ut.import_shakespeare()
print lines
lines = np.asarray(lines)
lines = lines.flatten()#np.reshape(lines.flatten(), (-1, 1))
print lines
model = MultinomialHMM(n_components=5)
model.fit(lines)
hidden_states = model.predict(lines)

print hidden_states