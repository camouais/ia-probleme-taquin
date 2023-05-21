from finalTaquin import Taquin
from finalAlgo import Algo
import random
import time


class Test:
    def __init__(self, data):
        self.data = data

    def isSolvable(self):
        # Convertir la chaîne de caractères en une liste d'entiers hormis le "X"
        nums = [int(x) for x in self.data if x != 'X']

        # Compter le nombre d'inversions dans la liste
        inversions = 0
        for e in range(len(nums)):
            for j in range(e + 1, len(nums)):
                if nums[e] > nums[j]:
                    inversions += 1

        # Si le nombre d'inversions est pair, le puzzle est soluble
        return inversions % 2 == 0

    def shuffle(self):
        # Mélange une chaine de caractères
        list_car = list(self.data)
        random.shuffle(list_car)
        return [''.join(list_car), list_car]  # Reconcatene la chaine

    def test(self, taquin_t, taquin_finale, choiceAlgo):

        if taquin_t.isSolvable():
            taquin = Taquin(taquin_t.data)
            algo = Algo()

            start = time.time()
            if choiceAlgo == "a_star":
                res = algo.a_star(5, taquin, taquin_finale)
            elif choiceAlgo == "bfs":
                res = algo.bfs(taquin, taquin_finale)
            end = time.time()
            elapsed = end - start

            explored = algo.get_explored_states_count()
            # print("Etat initial :")
            # print("----------------------")
            # print(taquin)
            # cpt = 0
            # for i in taquin.printTaquin(res.history):
            #     cpt += 1
            #     print("                      ")
            #     print("Etape : ", cpt)
            #     print("----------------------")
            #     print(i)
            print("Temps d'exécution : ", round(elapsed, 5))
            print("Nombre de déplacements :", len(res.history))
            print("Déplacements realises :", res.history)
            print("Nombre d'états explorés : ", explored)
            return [taquin_t, res, elapsed, explored]
        else:
            print("Taquin non résolvable.")
            return [taquin_t, 0]

    def TestForThousand(self, taquin_finale, choiceAlgo):
        sum_dep = 0  # Somme des nombres de déplacements
        sum_time = 0  # Somme des temps d'exécutions
        sum_expl = 0  # Somme d'états explorés
        cpt_ok = 0  # Compteur de configurations soluble
        cpt_bad = 0  # Compteur de configurations non soluble

        for i in range(1000):
            print("Test :", i)

            taquin_rdm = Test(self.shuffle()[0])
            test = self.test(taquin_rdm, taquin_finale, choiceAlgo)

            if test[0].isSolvable():
                sum_expl += test[3]
                sum_time += round(test[2], 5)
                sum_dep += len(test[1].history)
                cpt_ok += 1

            else:
                print("Pas de solution.")
                cpt_bad += 1
            print("\n")

        print("Nombre d'états initiaux solvable : ", cpt_ok)
        print("Nombre d'états initiaux mauvais : ", cpt_bad, "\n")

        if cpt_ok > 0:
            print("Nombre d'états moyen explorés : ", round(sum_expl / cpt_ok))
            print("Temps moyen :", round(sum_time / cpt_ok, 5))
            print("Déplacement moyen :", round(sum_dep / cpt_ok))

        return [cpt_ok, cpt_bad, sum_expl, sum_time, sum_dep]


# # t_3x3 = Test("01234567X")  # Configuration initiale
# t_init = Test("135X76420")  # Configuration initial
# # test = Test("135X07642")
# final = Taquin("01234567X")  # Configuration finale

# # taquin_random = Test(t_3x3.shuffle())

# a_star = "a_star"
# bfs = "bfs"

# # test.test(test, final, a_star)
# print("Algo a_star : ")
# t_init.test(t_init, final, a_star)
# print('\n')
# print('\n')
# print("Algo bfs: ")
# t_init.test(t_init, final, bfs)
# print('\n')
# print('\n')


# # t_3x3.TestForThousand(final, bfs)
