# Codage canal : CRC

from .sequence import generate_random_sequence

def crc(input, state):
    """
    Pour l'entree et l'etat des registres donnes, retourne l'etat suivant et la sortie
    d'un code convolutif ayant pour polynomes generateurs poly_1 et poly_2
    """
    poly_1 = [1, 1, 1]
    poly_2=[1, 0, 1]
    output = [(poly_1[0] & input) ^ (poly_1[1] & state[0]) ^ (poly_1[2] & state[1]), (poly_2[0] & input) ^
              (poly_2[1] & state[0]) ^ (poly_2[2] & state[1])]
    return output, [input, state[0]]  # output, new_state


def crc_encoding(message):  
    """Encode le message suivant le code convolutif de polynomes generateurs poly_1 et poly_2"""
    state = [0, 0] #etat initial de nos registres
    coded_message = []
    for i in message:
        output, new_state = crc(i, state)
        coded_message.append(output)
        state = new_state
    return coded_message

