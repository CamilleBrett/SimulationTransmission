import numpy as np 


def generate_random_sequence(n_bits):
    return list(np.random.randint(0, 2, n_bits))

