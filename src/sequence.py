# Genere un message aleatoire

import numpy as np


def generate_random_sequence(n_bits):
    """Genere un message aleatoire de n_bits bits"""
    return list(np.random.randint(0, 2, n_bits))
