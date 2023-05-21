class Algo:

    def __init__(self):
        self.explored_count = 0  # Initialisation du compteur

    def get_explored_states_count(self):
        return self.explored_count

    def a_star(self, mode, initial_state, final_state):
        border_set = []  # Liste ordonnée de l'ensemble frontière
        border_dict = {}  # Dictionnaire de l'ensemble frontière
        explored_dict = {}  # Dictionnaire pour vérifier si un état a déjà été exploré

        # Insérer l'état initial dans la frontière et le dictionnaire des états explorés
        initial_state.f = initial_state.get_h_score(mode, final_state)
        border_set.append(initial_state)
        border_dict[initial_state] = initial_state

        while border_set:
            # Sélectionner et supprimer le premier élément de la frontière
            current = border_set.pop(0)
            del border_dict[current]
            explored_dict[current] = current
            self.explored_count += 1

            # Vérifier si l'état courant correspond à l'état final
            if current.state == final_state.state:
                return current  # Si oui, terminer la boucle et renvoyer l'état courant

            # recuperer les enfants de ce premier etat de la liste fontiere
            children = current.getChild()

            for child in children:
                # Calculer l'heuristique (score) de l'enfant
                child.f = child.get_traveledPath() + child.get_h_score(mode, final_state)

               # rechercher dans l ensemble si les etats des enfants ne sont pas deja presents =

                if child in border_dict:
                    found = border_dict[child]
                    # Si l etat est deja present et a un chemin plus long que le nouveau, on le supprime de l'ensemble et du dictionnaire frontiere
                    if (found.get_traveledPath() > child.get_traveledPath()):
                        border_set.remove(found)
                        del border_dict[found]
                    else:
                        # Si l etat est deja present et l'ancien a un chemin plus court que le nouveau, on oublie le nouveau
                        continue

                # on insere le nouvel élément dans l ensemble fontiere par ordre d heuristique croissante, et on le reference dans le dictionnaire fontiere
                if child in explored_dict:
                    found = explored_dict[child]

                    if (found.get_traveledPath() > child.get_traveledPath()):
                        explored_dict[child] = child
                    else:
                        continue

                # Insérer le voisin dans la frontière en triant par ordre croissant d'heuristique
                border_set.append(child)
                border_set.sort(key=lambda x: x.f)
                border_dict[child] = child
                explored_dict[child] = child

                # Si aucun chemin menant à l'état final n'est trouvé, renvoyer None
        return None

    def bfs(self, initial_state, final_state):
        queue = []  # File d'attente pour les états à explorer
        explored_dict = {}  # Dictionnaire pour vérifier si un état a déjà été exploré

        # Insérer l'état initial dans la file d'attente et le dictionnaire des états explorés
        queue.append(initial_state)
        explored_dict[initial_state] = initial_state

        while queue:
            # Sélectionner et supprimer le premier élément de la file d'attente
            current = queue.pop(0)
            self.explored_count += 1

            # Vérifier si l'état courant correspond à l'état final
            if current.state == final_state.state:
                return current  # Si oui, terminer la boucle et renvoyer l'état courant

            # Récupérer les enfants de l'état courant
            children = current.getChild()

            for neighbor in children:
                # Vérifier si le voisin a déjà été exploré
                if neighbor in explored_dict:
                    continue

                # Ajouter le voisin à la file d'attente et le marquer comme exploré
                queue.append(neighbor)
                explored_dict[neighbor] = neighbor

        # Si aucun chemin menant à l'état final n'est trouvé, renvoyer None
        return None
