# Modulation d'amplitude a 4 etats (ASK-4)
import numpy as np
import matplotlib.pyplot as plt
from .CRC import crc_encoding
from .sequence import generate_random_sequence

def TRMS(signal):
    return ([signal[i]**2 for i in range(len(signal))])/len(signal)

def ask_modulate(message, nb_symboles, f_porteuse, f_symboles, f_ech):
    #f_porteuse = 100.0 #Hz
    #f_symboles = 40.0 #Hz
    #f_ech = f_porteuse*8
    time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)
    porteuse = np.sin(2*np.pi*f_porteuse*time_fech)
    modulant = np.zeros(int(nb_symboles/f_symboles*f_ech))
    for i in range(len(message)):
        if message[i] == [0, 0]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 1.
        elif message[i] == [0, 1]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 2.
        elif message[i] == [1, 0]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 3.
        elif message[i] == [1, 1]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 4.
    signal_module = [porteuse[i] * modulant[i] for i in range(len(porteuse))]




    return porteuse, modulant, signal_module

def ask_demodulate(noisy_signal, nb_symboles, f_symboles, f_ech):
    """
    Pour la decision on va etudier la TRMS du signal bruite sur un intervalle de temps t_symboles
    """
    received_encoded_message = []
    for i in range(nb_symboles):
        symb_amplitude = np.sqrt(2)*TRMS(noisy_signal[i*f_ech/f_symboles, (i+1)*f_ech/f_symboles])
        if symb_amplitude < 1.5:
            received_encoded_message.append([0, 0])
        elif symb_amplitude < 2.5:
            received_encoded_message.append([0, 1])
        elif symb_amplitude < 3.5
            received_encoded_message.append([1, 0])
        else :
            received_encoded_message.append([1, 1])
    
    return received_encoded_message



def main():
    message = generate_random_sequence(20)
    encoded_message = crc_encoding(message)
    porteuse, modulant, signal_module = ask_modulate(encoded_message)
    plt.subplot(3,1,1)
    plt.plot(time_fech, porteuse)
    plt.subplot(3,1,2)
    plt.plot(time_fech, modulant)
    plt.subplot(3,1,3)
    plt.plot(time_fech, signal_module)
    plt.show()

if __name__ == '__main__':
    main()