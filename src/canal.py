def bruit_gaussien(y, intensite):
    bruit = (np.random.normal(0, 1, len(y)) - 0.5) * intensite
    return np.array(y) + bruit