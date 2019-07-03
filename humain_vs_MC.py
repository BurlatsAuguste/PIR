class MC(object):
    """docstring for MC."""

    def __init__(self):
        self.tableau = [] #correspond à q(s,a)

    #cherche à trouver l'index du tableau correspondant à q(s,a) avec s=grille et a=action
    #renvoi -1 s'il ne le trouve pas
    def find_state(self, grille, action):
        index = -1
        for i in range(len(self.tableau)):
            if (comparer_grille(self.tableau[i][0][0], grille) == True) and (comparer_action(self.tableau[i][0][1], action) == True):
                index = i
        return index

    #donne q(grille, action)
    def get_value(self, grille, action):
        index = self.find_state(grille, action)
        if index == -1:
            return 0
        return self.tableau[index][1]

    #met à jour q(grille, action) grâce au résultat de la partie
    #self.tableau[index][2] contient le nombre de resultats
    #self.tableau[index][1] contient la somme des résultats
    def learn(self, grille, action, resultat):
        index = self.find_state(grille, action)
        if index == -1: #si le doublet (grille, action) est inconnu on rajoute une ligne au tableau
            self.tableau.append([(grille, action), resultat, 1])
        else:
            valeur = self.tableau[index][1]*self.tableau[index][2]
            valeur += resultat
            self.tableau[index][2] += 1
            self.tableau[index][1] = valeur/self.tableau[index][2]

    #permet d'afficher tout les q(s,a)
    def afficher(self):
        for valeurs in self.tableau:
            afficher(valeurs[0][0])
            print(valeurs[0][1])
            print(valeurs[1])

    #permet de sauvegarder q sur un fichier
    def sauvegarder(self, emplacement):
        with open(emplacement, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(self.tableau)
    
    #permet de charger q depuis un fichier
    def charger(self, emplacement):
        with open(emplacement, 'rb') as fichier:
            mon_unpickler = pickle.Unpickler(fichier)
            self.tableau = mon_unpickler.load()


#crée une grille de morpion remplie de 0
def initialisation():
	grille = [[0 for i in range(3)] for j in range(3)]
	return grille

#affiche la grille
def afficher(grille):
	for j in range(3):
		for i in range(3):
			print(grille[j][i], end ='')
		print("")
	print("")

#détermine s'il y a un vainqueur et qui
def victoire(grille):
	if grille[0][0] != 0:
		if grille[0][1] == grille[0][0] and grille[0][0] == grille[0][2]:
			return grille[0][0]
		if grille[1][0] == grille[0][0] and grille[2][0] == grille[0][0]:
			return grille[0][0]
		if grille[1][1] == grille[0][0] and grille[2][2] == grille[0][0]:
			return grille[0][0]
	if grille[1][1] != 0:
		if grille[0][1] == grille[1][1] and grille[2][1] == grille[1][1]:
			return grille[1][1]
		if grille[1][0] == grille[1][1] and grille[1][2] == grille[1][1]:
			return grille[1][1]
		if grille[2][0] == grille[1][1] and grille[0][2] == grille[1][1]:
			return grille[1][1]
	if grille[2][2] != 0:
		if grille[0][2] == grille[2][2] and grille[1][2] == grille[2][2]:
			return grille[2][2]
		if grille[2][0] == grille[2][2] and grille[2][1] == grille[2][2]:
			return grille[2][2]
	return 0

#effectue le coup du joueur
def placer(grille, joueur, ligne, colonne):
	if grille[ligne][colonne] == 0:
		grille[ligne][colonne] = joueur
		return True
	return False

#determine si la grille est pleine
def grille_pleine(grille):
	for j in range(3):
		for i in range(3):
			if grille[j][i] == 0:
				return False
	return True

#determine si la partie est finie
#renvoi 1 si le joueur 1 a gagné, 2 si c'est le joueur 2, 3 si c'est un match nul
# 0 si c'est un match nul
def fin(grille):
	a = victoire(grille)
	if a != 0:
		return a
	elif grille_pleine(grille):
		return 3
	else:
		return 0

#détermine si deux grilles sont identiques, renvoie True si oui
def comparer_grille(a, b):
	for j in range(3):
		for i in range(3):
			if a[j][i] != b[j][i]:
				return False
	return True

#détermine si deux actions sont identiques, renvoie True si oui
def comparer_action(a, b):
    for i in range(2):
        if a[i] != b[i]:
            return False
    return True

#crée une copie de la grille passée en paramètre
def copie_grille(grille):
	b = []
	for j in range(3):
		b.append([])
		for i in range(3):
			b[j].append(grille[j][i])
	return b

#donne les actions possibles depuis une grille
def getAction(grille):
	possibilitees = []
	for i in range(3):
		for j in range(3):
			if grille[i][j] == 0:
				possibilitees.append([i,j])
	return possibilitees

#choisi l'action qui maximise q(s,a)
def Decision(Q_function, grille):
    actions = getAction(grille)
    choix = 0
    val = -100000000
    for i in range(len(actions)):
        new_val = Q_function.get_value(grille, actions[i])
        if new_val > val:
            choix = i
            val = new_val
    return actions[choix]

import pickle
import sys
Q = MC()
Q.charger(sys.argv[1])
while True:
    jeu = initialisation()
    joueur = 0
    afficher(jeu)
    end = fin(jeu)
    while end == 0:
        joueur = joueur%2
        joueur += 1
        if joueur == int(sys.argv[2]): #le joueur décide au lancement s'il est joueur 1 ou 2
            valide = False
            while valide == False:
                print("veuillez jouer" + str(joueur))
                l = int(input("ligne ?"))
                c = int(input("colonne ?"))
                valide = placer(jeu, joueur, l, c)
        else:
            coup = Decision(Q, jeu)
            placer(jeu, joueur, coup[0], coup[1])
        afficher(jeu)
        end = fin(jeu)
    print("victoire joueur ", end)
