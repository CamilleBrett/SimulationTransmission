# Modulation d'amplitude a 4 etats (ASK-4)
import numpy as np
import matplotlib.pyplot as plt
from .CRC import crc_encoding
from .sequence import generate_random_sequence


def sq_TRMS(signal):
    """Calcule le carre de la valeur efficace d'un signal"""
    return sum([signal[i]**2 for i in range(len(signal))])/len(signal)


def ask_modulate(message, nb_symboles, f_porteuse, f_symboles, f_ech):
    """Modulation de l'information sur une porteuse de frequence f_porteuse, modulation a 4 etats
    A l'etat 0 on associe une amplitude 1
    A l'etat 1 on associe une amplitude 2
    A l'etat 2 on associe une amplitude 3
    A l'etat 3 on associe une amplitude 4
    On renvoie le signal module echantillonne a une frequence f_ech
    """
    time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)
    # on cree notre signal porteuse
    porteuse = np.sin(2*np.pi*f_porteuse*time_fech)
    modulant = np.zeros(int(nb_symboles/f_symboles*f_ech))
    for i in range(len(message)):
        if message[i] == [0, 0]:  # etat 0
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 1.
        elif message[i] == [0, 1]:  # etat 1
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 2.
        elif message[i] == [1, 0]:  # etat 2
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 3.
        elif message[i] == [1, 1]:  # etat 3
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 4.
    signal_module = [porteuse[i] * modulant[i] for i in range(len(porteuse))]
    return porteuse, modulant, signal_module


def ask_demodulate(noisy_signal, nb_symboles, nb_ech_per_symbole):
    """
    Demodule le signal ASK
    Pour chaque symbole module (portion de noisy_signal de duree t_symbole), 
    on etudie une approximation de l'amplitude a partir de la valeur efficace
    (pour un signal sinusoidal Veff = Amplitude/sqrt(2))
    On compare cette amplitude a 3 seuils pour prendre notre decision
    """
    received_amplitude = []
    received_message = []
    for i in range(nb_symboles):
        symb_amplitude = 2 * \
            sq_TRMS(
                noisy_signal[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole])
        if symb_amplitude <= 1.5**2:
            received_message.append([0, 0])
            received_amplitude[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [
                1 for i in range(nb_ech_per_symbole)]
        elif symb_amplitude <= 2.5**2:
            received_message.append([0, 1])
            received_amplitude[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [
                2 for i in range(nb_ech_per_symbole)]
        elif symb_amplitude <= 3.5**2:
            received_message.append([1, 0])
            received_amplitude[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [
                3 for i in range(nb_ech_per_symbole)]
        else:
            received_message.append([1, 1])
            received_amplitude[i*nb_ech_per_symbole:(i+1)*nb_ech_per_symbole] = [
                4 for i in range(nb_ech_per_symbole)]

    return received_message, received_amplitude


def main():
    """test pour voir si tout fonctionne"""
    message = generate_random_sequence(20)
    encoded_message = crc_encoding(message)
    porteuse, modulant, signal_module = ask_modulate(encoded_message)
    plt.subplot(3, 1, 1)
    plt.plot(time_fech, porteuse)
    plt.subplot(3, 1, 2)
    plt.plot(time_fech, modulant)
    plt.subplot(3, 1, 3)
    plt.plot(time_fech, signal_module)
    plt.show()


if __name__ == '__main__':
    main()
