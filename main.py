import numpy as np
import matplotlib.pyplot as plt

from src.ASK import ask_modulate
from src.CRC import crc_encoding
from src.sequence import generate_random_sequence
from src.canal import gaussian_noise, awgn

#Frequences en Hz
f_porteuse = 100.
f_symboles = 40.
f_ech = 8*f_porteuse

#SNR en dB
gammadB = 30

#Nombre de bits dans le message transmis
nb_symboles = 20

#Nombre de points d'echantillonnage
nb_points = int(nb_symboles*f_ech/f_symboles)

#temps
time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)

#Debut du script
#Generation du message a envoyer
message = generate_random_sequence(nb_symboles)

#Codage du message pour le rendre resistant au canal
encoded_message = crc_encoding(message)

 #Modulation du message: on passe sur un signal physique
porteuse, modulant, signal_module = ask_modulate(encoded_message, nb_symboles, f_porteuse, f_symboles, f_ech)

#Figures : porteuse, message encode, signal module

plt.subplot(3,2,1)
plt.plot(time_fech, porteuse)
plt.subplot(3,2,2)
plt.plot(time_fech, modulant)
plt.subplot(3,2,3)
plt.plot(time_fech, signal_module)
#plt.show()


#Calcul de l'energie par bits
Eb = sum([signal_module[i]**2 for i in range(len(signal_module))])/nb_symboles
print(Eb)
N0 = Eb/(10**(gammadB/10))
sigma = np.sqrt(N0/2)

noise, noisy_signal = awgn(signal_module, sigma)

plt.subplot(3,2,4)
plt.plot(time_fech, noise)
plt.subplot(3,2,5)
plt.plot(time_fech, noisy_signal)
#plt.show()

