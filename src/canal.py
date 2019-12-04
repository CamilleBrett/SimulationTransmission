import numpy as np

def gaussian_noise(nb_points, sigma):
    noise = np.random.normal(0, sigma, nb_points)
    return noise

def awgn(signal, sigma):
    noise = gaussian_noise(len(signal), sigma)
    return noise, (signal + noise)

