# Codage canal : CRC

from .sequence import generate_random_sequence

def crc(input, state):
    poly_1 = [1, 1, 1]
    poly_2=[1, 0, 1]
    output = [(poly_1[0] & input) ^ (poly_1[1] & state[0]) ^ (poly_1[2] & state[1]), (poly_2[0] & input) ^
              (poly_2[1] & state[0]) ^ (poly_2[2] & state[1])]
    return output, [input, state[0]]  # output, new_state

#print(crc(0, [0, 0]))


def crc_encoding(message):  # message is an array
    state = [0, 0]
    coded_message = []
    for i in message:
        output, new_state = crc(i, state)
        coded_message.append(output)
        state = new_state
    return coded_message

