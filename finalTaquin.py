import math

POIDS = ((36, 12, 12, 4, 1, 1, 4, 1, 0),  # pi1
         (8, 7, 6, 5, 4, 3, 2, 1, 0),  # pi2 = pi3
         (8, 7, 6, 5, 4, 3, 2, 1, 0),  # pi3 = pi2
         (8, 7, 6, 5, 3, 2, 4, 1, 0),  # pi4 = pi5
         (8, 7, 6, 5, 3, 2, 4, 1, 0),  # pi5 = pi4
         (1, 1, 1, 1, 1, 1, 1, 1, 0))  # pi6

COEFF = (4, 1, 4, 1, 4, 1)  # rho1 a rho6


class Taquin:

    def __init__(self, param):

        if isinstance(param, str):
            self.state = param
            self.size = int(math.sqrt(len(self.state)))
            if self.size ** 2 != len(self.state):
                raise Exception("Le taquin doit être un carre")
            self.f = 0
            self.history = ''
        elif isinstance(param, Taquin):
            self.state = param.state
            self.size = param.size
            self.history = param.history
            self.f = param.f
        else:
            raise Exception("Parametre inconnu")

    def __eq__(self, other):
        return isinstance(other, Taquin) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return ''.join(str(self.state))
        # grille = [self.state[i * self.size:(i + 1) * self.size]
        #           for i in range(self.size)]
        # return '\n'.join(' '.join(str(cell) for cell in row) for row in grille)

    def move(self, direction):

        pos = self.state.find('X')
        new_position = pos
        if pos is None:
            return None

        if direction == "N":
            new_position = pos - self.size
            if (new_position < 0):
                return None

        elif direction == "S":
            new_position = pos + self.size
            if new_position > (self.size * self.size) - 1:
                return None

        elif direction == "O":
            if pos % self.size == 0:
                return None
            new_position = pos - 1

        elif direction == "E":
            if pos % self.size == self.size - 1:
                return None
            new_position = pos + 1

        else:
            return None

        res = Taquin(self)
        tmp = res.state[new_position]
        res.state = res.state.replace('X', 'Y')
        res.state = res.state.replace(self.state[new_position], 'X')
        res.state = res.state.replace('Y', tmp)
        res.history += direction
        return res

    def getChild(self):
        children = []

        if self.move("N") is not None:
            children.append(self.move("N"))

        if self.move("S") is not None:
            children.append(self.move("S"))

        if self.move("E") is not None:
            children.append(self.move("E"))

        if self.move("O") is not None:
            children.append(self.move("O"))

        return children

    def dist_manhattan(self, e, state_final):
        # renvoie le nombre de deplacement a faire pour obtenir l'etat final
        pos = self.state.find(e)

        # cherche la position de la tuile dans l'etat final
        pos_final = state_final.state.index(e)
        # deplacements a faire pour obtenir la position finale de la tuile
        h = abs(pos % self.size - pos_final % self.size) + \
            abs(pos // self.size - pos_final // self.size)
        return h

    # Donne le coût de l'heuristique
    def get_h_score(self, mod, final_state):
        res = 0
        a = 0
        for e in self.state:
            if e == "X":
                continue

            a += POIDS[mod - 1][int(e)] * (self.dist_manhattan(e, final_state))
            res = a // COEFF[mod - 1]
        return res

    def get_traveledPath(self):
        return len(self.history)

    def printTaquin(self, deplacement):
        temp = self
        list_t = []
        for i in deplacement:
            a = temp.move(i)
            if a:
                temp = a
                list_t.append(a)
        return list_t
