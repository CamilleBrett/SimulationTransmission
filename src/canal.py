#Genere un canal gaussien
import numpy as np

def gaussian_noise(nb_points, sigma):
    """genere un bruit blanc gaussien de longeur nb_points et d'ecart-type sigma"""
    noise = np.random.normal(0, sigma, nb_points)
    return noise

def awgn(signal, sigma):
    """retourne un signal bruite sortant d'un canal gaussien de parametre sigma"""
    noise = gaussian_noise(len(signal), sigma)
    return noise, (signal + noise)

