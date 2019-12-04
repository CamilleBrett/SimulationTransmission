from copy import deepcopy
from .CRC import crc, crc_encoding
from .sequence import generate_random_sequence

class Wire:
    def __init__(self, vert1, vert2, input, output, real_output):
        self.weight = 0
        self.vert1 = vert1
        self.vert2 = vert2
        self.input = input
        self.output = output
        self.weight = abs(self.output[0] - real_output[0]) + abs(self.output[1] - real_output[1])



class Path:
    def __init__(self, first_wire):
        self.weight=0
        self.wires=[first_wire]
        self.last_state = first_wire.vert2
        
    def compute_weight(self):
        new_weight = 0
        for wire in self.wires:
            new_weight += wire.weight
        self.weight = new_weight

    def add_wire(self, wire):
        self.wires.append(wire)
        self.last_state = wire.vert2
        self.compute_weight()


    def print_path(self):
        vertices = []
        for wire in self.wires:
            vertices.append(wire.vert1)
        vertices.append(self.last_state)
        print(vertices)

def copy_path(path):
    new_path = Path(path.wires[0])
    for wire in path.wires[1:]:
        new_path.add_wire(wire)
    new_path.compute_weight()
    return new_path


def branches(current_state, real_output):
    output0, new_state0 = crc(0, current_state)
    output1, new_state1 = crc(1, current_state)
    wire0 = Wire(current_state, new_state0, 0, output0, real_output)
    wire1 = Wire(current_state, new_state1, 1, output1, real_output)
    return wire0, wire1


def viterbi(message):
    # initialisation du graphe : premieres branches
    paths = []
    decoded_message = []
    min_weight = len(message)*2
    init = 1
    for i in message:
        new_paths = []
        critical_paths = []

        if init == 1:
            wire0, wire1 = branches([0, 0], i)
            paths.append(Path(wire0))
            paths.append(Path(wire1))
            init = 0
        else:
            for p in range(len(paths)):
                wire0, wire1 = branches(paths[p].last_state, i)
                new_path = copy_path(paths[p])
                paths[p].add_wire(wire0)
                new_path.add_wire(wire1)
                new_paths.append(new_path)
            paths.extend(new_paths)

        for path in paths:
            path.compute_weight()
        for p in range(len(paths)):
            for q in range(p+1, len(paths)):
                if paths[p].last_state == paths[q].last_state:
                    if paths[p].weight >= paths[q].weight:
                        critical_paths.append(p)
                    else:
                        critical_paths.append(q)
        for j in range(len(critical_paths)):
            paths.pop(critical_paths[j]-j)

    #Comparing weights
    for p in paths:
        if p.weight <= min_weight:
            min_weight = p.weight
            best_path = p
    for wire in best_path.wires:
        #Determining message
        decoded_message.append(wire.input)
    return decoded_message


def main():
    message = generate_random_sequence(10)
    coded_message = crc_encoding(message)
    decoded_message = viterbi(coded_message)
    print ("Message :", message)
    print ("Coded message :", coded_message)
    print ("Decoded message :", decoded_message)
    print ("Right decoding ?", message == decoded_message)
    
if __name__ == '__main__':
    main()