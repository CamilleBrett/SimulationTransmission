import numpy as np
from src.ASK import ask_modulate
from src.CRC import crc_encoding
from src.sequence import generate_random_sequence


#Frequences en Hz
f_porteuse = 100.
f_symboles = 40.
f_ech = 8*f_porteuse

#Nombre de bits dans le message transmis
nb_symboles = 20

#temps
time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)

#Debut du script
#Generation du message a envoyer

message = generate_random_sequence(nb_symboles)
encoded_message = crc_encoding(message)
porteuse, modulant, signal_module = ask_modulate(encoded_message)
plt.subplot(3,1,1)
plt.plot(time_fech, porteuse)
plt.subplot(3,1,2)
plt.plot(time_fech, modulant)
plt.subplot(3,1,3)
plt.plot(time_fech, signal_module)
plt.show()