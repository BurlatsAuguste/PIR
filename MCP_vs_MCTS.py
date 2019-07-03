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

class MCTS(object):
    """docstring for MCTS."""
    #cette classe correspond aux noeuds de l'arbre
    #chaque noeud contient une grille, un numéro correspondant au joueur censé joué face à cette grille
    #une liste des actions possibles, une liste des branches correspondantes à ces actions
    #une valeur d'état
    #un nombre de visite

    def __init__(self, grille, joueur):
        self.player = joueur
        self.grille = grille
        self.actions = getAction(grille)
        self.fils = []
        for move in self.actions:
            self.fils.append(Edge(move))
        self.valeur = 0.0
        self.visite = 1

    #n'affiche que les noeuds juste en dessous avec leurs valeurs et leur nombre de visite
    def Afficher_fils(self): 
        for son in self.fils:
            if son.fils != None:
                afficher(son.fils.grille)
                print(son.valeur)
                print(son.visite)
                print("")

    #affiche l'arbre partant de ce noeud avec les valeurs et nombre de visite de chaque grille
    def Afficher_arbre(self):
        afficher(self.grille)
        print(self.valeur)
        print(self.visite)
        print("")
        for son in self.fils:
            son.Afficher_arbre()


    def Selection(self):
        end = fin(self.grille) #on observe si le noeud correspond à une fin de partie
        if end == 0: #si non on va plus profond
            choix = 0
            if self.player == 2: #si c'est au tour du joueur 2, on prend l'opposé de chaque valeur d'actions, car son but est minimiser les gains du joueur 1
                ucb = -self.fils[choix].valeur + sqrt(4)*sqrt(log(self.visite)/self.fils[choix].visite)
            else:
                ucb = self.fils[choix].valeur + sqrt(4)*sqrt(log(self.visite)/self.fils[choix].visite)
            for i in range(len(self.fils)):
                if self.player == 2:
                    new_ucb = -self.fils[i].valeur + sqrt(4)*sqrt(log(self.visite)/self.fils[i].visite)
                else:
                    new_ucb = self.fils[i].valeur + sqrt(4)*sqrt(log(self.visite)/self.fils[i].visite)
                if new_ucb > ucb : #l'action maximisant q(s,a)+ucb(s,a) est choisie
                    choix = i
                    ucb = new_ucb
            self.visite += 1
            if self.fils[choix].fils == None: #s'il n'y a pas plus profond on étend l'arbre
                self.fils[choix].Expansion(copie_grille(self.grille), self.player)
            else: #sinon on continue à descendre
                self.fils[choix].Selection()
        else: #si l'on est à une fin de partie la valeur du noeud est le résultat
            self.visite +=1
            if end == 2:
                end = -1
            if end == 3:
                end = 0
            self.valeur = end 

    #plusieurs partie sont simulées en partant de l'état du noeud
    def Evaluation(self):
        resultats = []
        for i in range(100):
            jeu = copie_grille(self.grille)
            joueur = self.player
            end = fin(jeu)
            while end == 0:
                move = getAction(jeu)
                coup = choice(move) #pour la simulation les coups sont choisis au hasard
                placer(jeu, joueur, coup[0], coup[1])
                joueur = joueur%2
                joueur += 1
                end = fin(jeu)
            if end == 2:
                end = -1
            if end == 3:
                end = 0
            resultats.append(end)
        self.valeur = sum(resultats)/len(resultats) #on calcule la moyenne des résultats obtenus

    def Backpropagation(self):
        somme = self.valeur
        total = 1
        for son in self.fils:
             if son.fils != None:
                 val, nbr = son.Backpropagation()
                 somme += val*(son.visite/self.visite)
                 total += nbr
        return (somme, total) #on fait remonter la somme de toute les valeurs d'état du sous arbre ainsi que le nombre de noeud de ce sous arbre

    def Decision(self):
        for i in range(500): #répetition de 500 cycles Selection-Expansion-Evaluation-Backpropagation
            self.Selection()
            self.Backpropagation()
        choix = 0
        for i in range(len(self.fils)): #choix de l'action maximisant q(s,a)
            if ((self.fils[i].valeur > self.fils[choix].valeur) and self.player == 1) or ((-self.fils[i].valeur > -self.fils[choix].valeur) and self.player == 2):
                choix = i
        return self.actions[choix]

class Edge(object):

    #correspond aux branches de l'arbre
    #chaque branche contient : une action
    #une valeur d'action
    #un noeud fils correspondant à l'état obtenu après avoir effectué l'action de la branche depuis l'état du noeud précédent
    #un nombre de visite

    def __init__(self, action):
        self.action = action
        self.valeur = 0.0
        self.fils = None
        self.visite = 1

    def Selection(self):
        self.visite += 1
        self.fils.Selection()

    #création du nouveau noeud
    def Expansion(self, grille, joueur):
        placer(grille, joueur, self.action[0], self.action[1])
        joueur = joueur%2
        joueur+=1
        self.fils = MCTS(grille, joueur)
        self.fils.Evaluation()

    #q(s,a) = somme de toute les valeurs d'état du sous arbre divisée par le nombre de noeud du sous arbre
    #soit la moyenne des valeurs d'état du sous arbre
    def Backpropagation(self):
        somme, total = self.fils.Backpropagation()
        self.valeur = somme/total
        return (somme, total)

    def Afficher_arbre(self):
        if self.fils != None:
            self.fils.Afficher_arbre()

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
	#print("match nul")
	return True

#determine si la partie est finie
#renvoi 1 si le joueur 1 a gagné, 2 si c'est le joueur 2, 3 si c'est un match nul
# 0 si c'est un match nul 
def fin(grille):
	a = victoire(grille)
	if a != 0:
		#print("bravo joueur ", a)
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

from random import choice
from math import sqrt, log
import pickle
import sys
Q = MC()
Q.charger(sys.argv[1])
resultats = []
for i in range(int(sys.argv[3])):
    print("partie ", i)
    jeu = initialisation()
    afficher(jeu)
    joueur = 0
    end = fin(jeu)
    while end == 0:
        joueur = joueur%2
        joueur += 1
        if joueur == int(sys.argv[2]):
            arbre = MCTS(copie_grille(jeu), joueur)
            coup = arbre.Decision()
        else:
            coup = Decision(Q, jeu)
        placer(jeu, joueur, coup[0], coup[1])
        afficher(jeu)
        end = fin(jeu)
    resultats.append(end)
print("victoires joueur 1 : ", resultats.count(1))
print("victoires joueur 2 : ", resultats.count(2))
print("matchs nuls : ", resultats.count(3))
