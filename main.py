import numpy as np
import matplotlib.pyplot as plt

from src.ASK import ask_modulate, ask_demodulate
from src.CRC import crc_encoding
from src.sequence import generate_random_sequence
from src.canal import gaussian_noise, awgn
from src.viterbi import viterbi

#Frequences en Hz
f_porteuse = 100.
f_symboles = 40.
f_ech = 8*f_porteuse

#SNR en dB
gammadB = 15

#Nombre de bits dans le message transmis
nb_symboles = 200

#Nombre de points d'echantillonnage
nb_points = int(nb_symboles*f_ech/f_symboles)

nb_ech_per_symbole = int(f_ech/f_symboles)

#temps
time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)

#Debut du script
#Generation du message a envoyer
message = generate_random_sequence(nb_symboles)

#Codage du message pour le rendre resistant au canal
encoded_message = crc_encoding(message)

#Modulation du message: on passe sur un signal physique
porteuse, modulant, signal_module = ask_modulate(
    encoded_message, nb_symboles, f_porteuse, f_symboles, f_ech)


#Calcul de l'energie par bits
Eb = sum([signal_module[i]**2 for i in range(len(signal_module))])/nb_symboles

N0 = Eb/(10**(gammadB/10))
sigma = np.sqrt(N0/2)

#Le signal passe dans le canal
noise, noisy_signal = awgn(signal_module, sigma)

#On demodule le signal
received_message, received_amplitude = ask_demodulate(
    noisy_signal, nb_symboles, nb_ech_per_symbole)

#On decode le message
decoded_message = viterbi(received_message)

#On calcule le nombre d'erreurs et le TEB
nb_errors = sum([message[i] != decoded_message[i] for i in range(nb_symboles)])
TEB = nb_errors/nb_symboles

#On affiche des informations dans la console
print("Taille du message envoyé : ", nb_symboles, "bits")
print("Fréquence porteuse : ", f_porteuse, "Hz; ", "Fréquence d'échantillonnage : ",
      f_ech, "Hz; ", "Fréquence d'émission symbole : ", f_symboles, "Hz; ")
print("Nombre d'erreurs :", nb_errors)
print("Taux d'erreur binaire pour RSB =", gammadB, "dB : ", TEB)

message_print = []
decoded_message_print = []

for i in range(nb_symboles):
    message_print[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [message[i]
                                                                    for j in range(nb_ech_per_symbole)]
    decoded_message_print[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [
        decoded_message[i] for j in range(nb_ech_per_symbole)]

#Figures : porteuse, message encode, signal module

plt.figure("SNR = " + str(gammadB) + "dB; " + "TEB = " + str(TEB))
plt.subplot(3,2,1)
plt.plot(time_fech, message_print)
plt.xlabel("Temps (s)")
plt.ylabel("Etat")
plt.title("Information transmise")

plt.subplot(3,2,2)
plt.plot(time_fech, modulant)
plt.xlabel("Temps (s)")
plt.ylabel("Etat")
plt.title("Information codée")

plt.subplot(3,2,3)
plt.plot(time_fech, signal_module, lw=0.5)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.title("Signal modulé")

plt.subplot(3,2,4)
plt.plot(time_fech, noisy_signal, lw=0.5)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.title("Signal reçu après canal")

plt.subplot(3,2,5)
plt.plot(time_fech, received_amplitude)
plt.xlabel("Temps (s)")
plt.ylabel("Etat")
plt.title("Message codé reçu")

plt.subplot(3,2,6)
plt.plot(time_fech, decoded_message_print)
plt.xlabel("Temps (s)")
plt.ylabel("Etat")
plt.title("Information reçue (décodée)")

plt.tight_layout()
plt.show()

