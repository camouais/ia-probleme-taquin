import tkinter
import tkinter as tk
from tkinter import TOP, NW
from finalTaquin import Taquin
from finalTest import Test

valeur = [0, 1, 2, 3, 4, 5, 6, 7, 8]
global label


def changeTypeValeur(taquin):
    global valeur
    valeur = [int(x) if x != "X" else 8 for x in taquin]
    return valeur


def changeTypeTaquin(valeur):
    n_val = [str(x) if x != 8 else 'X' for x in valeur]
    return n_val


def melanger_taquin():
    global valeur
    taquin = Test("01234567X").shuffle()[1]
    valeur = changeTypeValeur(taquin)
    print("Nouveau taquin : ", str(valeur))


def update_taquin(canvas, photos):
    canvas.delete("all")
    for k in range(len(photos)):
        canvas.create_image((30 + 150 * (k % 3)), 30 +
                            (150 * (k // 3)), anchor=NW, image=photos[valeur[k]])


def resoudre_taquin(canvas, photos, new_fen, ChoixAlgo):
    global valeur
    n_valeur = changeTypeTaquin(valeur)
    n_list = ''.join(n_valeur)
    test = Test(n_list)
    taquin = Taquin(n_list)
    nt = Test("01234567X").test(test, Taquin("01234567X"), ChoixAlgo)

    if nt[1] == 0:
        fenetre_err = tk.Tk()
        tk.Label(
            fenetre_err, text="Taquin non resolvable en A* \n Veuillez mélanger de nouveau", width=50).pack()
    else:
        a = nt[1].history
        cpt = 0
        print("Etat initial :", taquin)

        n_lab = tkinter.Label(
            new_fen, text="Execution du taquin étape : " + str(cpt))
        n_lab.pack()

        # Affichage des étapes
        for i in taquin.printTaquin(a):
            cpt += 1
            v = list(str(i))
            # Affichage des étapes
            print(f"Etape {cpt} : Nouvel Etat : {v} ")
            n_lab.config(text="Execution du taquin étape : " + str(cpt))

            # Mise à jour
            valeur = changeTypeValeur(v)
            update_taquin(canvas, photos)
            new_fen.after(500)
            new_fen.update()

        # Affichage des résultats
        n_lab.config(text="Temps execution : " + str(round(nt[2], 5)) + "\n Nombre d'états explorés : " + str(
            nt[3]) + "\n Nombre de déplacements : " + str(len(a)))
        # Affichage de la fenêtre résolue
        t_resolve = tk.Tk()

        # Taille de l'ecran
        largeur_ecran = t_resolve.winfo_screenwidth()
        hauteur_ecran = t_resolve.winfo_screenheight()

        # Calculer les coordonnées pour centrer la fenêtre
        x = (largeur_ecran - t_resolve.winfo_reqwidth()) / 2
        y = (hauteur_ecran - t_resolve.winfo_reqheight()) / 2

        # Définition de la position de la fenêtre
        t_resolve.geometry("+%d+%d" % (x - 100, y))

        # Affichage
        t_resolve.title('Résolu')
        tk.Label(t_resolve, text="Taquin résolu", width=30).pack()
        print("Taquin Résolu.")
        t_resolve.protocol("WM_DELETE_WINDOW", lambda: [
                           n_lab.destroy(), t_resolve.quit(), t_resolve.destroy()])
        t_resolve.mainloop()


def new_window():
    # Destruction de l'ancienne fenêtre
    maFenetre.destroy()
    # Créer une nouvelle fenêtre
    nouvelle_fen = tk.Tk()
    nouvelle_fen.title('Taquin 3x3')
    nouvelle_fen.configure(background='grey')

    # Taille de l'ecran
    largeur_ecran = nouvelle_fen.winfo_screenwidth()
    hauteur_ecran = nouvelle_fen.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x = (largeur_ecran - nouvelle_fen.winfo_reqwidth()) / 2
    y = (hauteur_ecran - nouvelle_fen.winfo_reqheight()) / 2

    # Définition de la position de la fenêtre
    nouvelle_fen.geometry("+%d+%d" % (x - 200, y - 250))

    # Création de l'environnement du taquin
    canvas = tk.Canvas(nouvelle_fen, width=540, height=180 * 3, bg='white')
    canvas.pack(side=TOP, padx=20, pady=20)

    # Chargement des images
    photos = [tk.PhotoImage(
        file=f"./number_buttons/{i}.png") for i in range(0, 9)]

    # Affichage initial du taquin
    update_taquin(canvas, photos)

    n_label = tkinter.Label(
        nouvelle_fen, text="Mélangez puis executez le taquin.")
    n_label.pack()
    n_label2 = tkinter.Label(
        nouvelle_fen, text="Mélangez puis executez le taquin.")

    # Création de la barre de menu
    menubar = tk.Menu(nouvelle_fen)

    # Menu "Mélanger / Quitter"
    menu1 = tk.Menu(menubar, tearoff=0)
    menu1.add_command(label="Mélanger", command=lambda: [
                      melanger_taquin(), update_taquin(canvas, photos)])
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=nouvelle_fen.quit)
    menubar.add_cascade(label="Mélange", menu=menu1)

    # Menu "Résoudre"
    menu2 = tk.Menu(menubar, tearoff=0)
    menu2.add_command(label="A*", command=lambda: [n_label.pack_forget(
    ), resoudre_taquin(canvas, photos, nouvelle_fen, "a_star"), n_label.pack()])
    menu2.add_command(label="Recherche en longueur", command=lambda: [n_label.pack_forget(
    ), resoudre_taquin(canvas, photos, nouvelle_fen, "dfs"), n_label.pack()])
    menu2.add_command(label="Recherche en largeur", command=lambda: [n_label.pack_forget(
    ), resoudre_taquin(canvas, photos, nouvelle_fen, "bfs"), n_label.pack()])
    menubar.add_cascade(label="Résoudre", menu=menu2)

    nouvelle_fen.config(menu=menubar)

    nouvelle_fen.mainloop()


# Création de la fenêtre principale
maFenetre = tk.Tk()
maFenetre.title('Jeu du Taquin')
maFenetre.configure(background="grey")

# Taille de l'ecran
largeur_ecran = maFenetre.winfo_screenwidth()
hauteur_ecran = maFenetre.winfo_screenheight()

# Calculer les coordonnées pour centrer la fenêtre
x = (largeur_ecran - maFenetre.winfo_reqwidth()) / 2
y = (hauteur_ecran - maFenetre.winfo_reqheight()) / 2

# Définition de la position de la fenêtre
maFenetre.geometry("+%d+%d" % (x-100, y))

# Texte de la fenêtre principale
tk.Label(maFenetre, text="Choix du taquin", width=50).pack()

# Création du bouton "Lancer Taquin 3x3"
button = tk.Button(maFenetre, text="Lancer Taquin 3x3",
                   width=50, command=new_window)

button.pack()
# Laisser la fenêtre principale active
maFenetre.mainloop()
