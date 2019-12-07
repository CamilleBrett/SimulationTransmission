# Decodage canal par maximum de vraisemblance

from .CRC import crc, crc_encoding
from .sequence import generate_random_sequence

# On commence par definir les objets du trellis


class Wire:
    """ Lien entre deux etats du treillis (portion de chemin)"""

    def __init__(self, vert1, vert2, input, output, real_output):
        self.vert1 = vert1  # etat de depart du lien
        self.vert2 = vert2  # etat d'arrivee du lien
        self.input = input  # entree
        self.output = output  # sortie
        # poids de la portion de chemin (distance entre la sortie estimee et la sortie recue)
        self.weight = abs(self.output[0] - real_output[0]) + \
            abs(self.output[1] - real_output[1])


class Path:
    """Chemin sur le treillis : il est constitue de differents objets Wire"""

    def __init__(self, first_wire):
        self.weight = 0  # poids total du chemin
        # initialisation de la liste des portions de chemin constituant le chemin
        self.wires = [first_wire]
        self.last_state = first_wire.vert2  # point d'arrivee du chemin

    def add_wire(self, wire):
        """Ajoute une portion de chemin au chemin"""
        self.wires.append(wire)
        self.last_state = wire.vert2
        self.weight += wire.weight

    def print_path(self):
        """Methode print du path : on affiche dans la console tous les sommets du chemin, dans l'odre"""
        vertices = []
        for wire in self.wires:
            vertices.append(wire.vert1)
        vertices.append(self.last_state)
        print(vertices)


def copy_path(path):
    """Permet de dupliquer un chemin (si a partir d'un sommet on a deux chemins possibles)"""
    new_path = Path(path.wires[0])
    for wire in path.wires[1:]:
        new_path.add_wire(wire)
    new_path.weight = path.weight
    return new_path


def branches(current_state, real_output):
    """A partir de l'etat des registres current_state, on determine les deux etats suivants et sorties possibles"""
    output0, new_state0 = crc(0, current_state)  # possibilite 1 : input = 0
    output1, new_state1 = crc(1, current_state)  # possibilite 2 : input = 1
    wire0 = Wire(current_state, new_state0, 0, output0, real_output)
    wire1 = Wire(current_state, new_state1, 1, output1, real_output)
    return wire0, wire1


def viterbi(message):
    """
    On execute l'algorithme de Viterbi sur notre message recu
    On construit le treillis au fur et a mesure et on calcule le poids cumule de chaque chemin possible
    Si deux chemins arrivent au meme etat, on supprime le chemin le plus court
    A la fin du treillis, parmi les chemins survivants, on choisit le chemin au poids le plus faible
    C'est celui qui maximise la vraissemblance
    """
    paths = []
    decoded_message = []
    min_weight = len(message)*2
    init = 1
    for i in message:
        new_paths = []
        critical_paths = []

        if init == 1:  # si c'est le debut du treillis, alors les registres sont a l'etat 0
            wire0, wire1 = branches([0, 0], i)
            paths.append(Path(wire0))
            paths.append(Path(wire1))
            init = 0
        else:
            # pour chaque chemin du treillis, on determine les deux suites posibles
            for p in range(len(paths)):
                wire0, wire1 = branches(paths[p].last_state, i)
                new_path = copy_path(paths[p])
                paths[p].add_wire(wire0)
                new_path.add_wire(wire1)
                new_paths.append(new_path)
            paths.extend(new_paths)

        # on determine les chemins critiques (ceux de poids les plus importants)
        for p in range(len(paths)):
            for q in range(p+1, len(paths)):
                if paths[p].last_state == paths[q].last_state:
                    if paths[p].weight >= paths[q].weight:
                        critical_paths.append(p)
                    else:
                        critical_paths.append(q)
        # on elimine les chemins critiques pour ne garder que les chemins survivants
        for j in range(len(critical_paths)):
            paths.pop(critical_paths[j]-j)

    for p in paths:
        if p.weight <= min_weight:  # on compare les poids de chaque chemin survivant
            min_weight = p.weight
            best_path = p
    for wire in best_path.wires:  # on decode le meilleur chemin : le message est l'entree de chaque portion du meilleur chemin
        decoded_message.append(wire.input)
    return decoded_message


def main():
    """on teste si tout fonctionne"""
    message = generate_random_sequence(10)
    coded_message = crc_encoding(message)
    decoded_message = viterbi(coded_message)
    print("Message :", message)
    print("Coded message :", coded_message)
    print("Decoded message :", decoded_message)
    print("Right decoding ?", message == decoded_message)


if __name__ == '__main__':
    main()
