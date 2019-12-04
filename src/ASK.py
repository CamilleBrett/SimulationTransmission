# Modulation d'amplitude a 4 etats (ASK-4)
import numpy as np
import matplotlib.pyplot as plt
from .CRC import crc_encoding
from .sequence import generate_random_sequence

def ask_modulate(message, f_porteuse, f_symboles, f_ech):
    #f_porteuse = 100.0 #Hz
    #f_symboles = 40.0 #Hz
    #f_ech = f_porteuse*8
    time_fech = np.arange(0, nb_symboles/f_symboles, 1/f_ech)
    porteuse = np.sin(2*np.pi*f_porteuse*time_fech)
    modulant = np.zeros(int(nb_symboles/f_symboles*f_ech))
    for i in range(len(message)):
        if message[i] == [0, 0]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 1
        elif message[i] == [0, 1]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 2
        elif message[i] == [1, 0]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 3
        elif message[i] == [1, 1]:
            for j in range(i*int(f_ech/f_symboles), (i+1)*int(f_ech/f_symboles)):
                modulant[j] = 4
    signal_module = [porteuse[i] * modulant[i] for i in range(len(porteuse))]




    return porteuse, modulant, signal_module




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