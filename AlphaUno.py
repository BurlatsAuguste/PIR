class Node(object):
	"""docstring for MCTS."""

	# un noeud correspond à un état
	#chaque noeud contient une grille, le joueur censé jouer face à cette grille
	#une liste des actions possibles, une liste de branches correspondantes à ces actions
	#une valeur d'état
	def __init__(self, grille, joueur, f):
		self.etat = copie_grille(grille)
		self.player = joueur
		self.actions = getAction(grille)
		self.edges = []
		self.probabilites, self.value = f.get_value(self.etat) #à la création du noeud, l'état est évalué par f_teta
		for i in range(len(self.actions)):
			self.edges.append(Edge(self.etat, self.actions[i], self.probabilites[i], joueur, f))
		if joueur == 2:
			self.value = -self.value

	#affiche l'arbre
	def afficherArbre(self):
		afficher(self.etat)
		print("V = ", self.value)
		for poss in self.edges:
			print(poss.action)
			print("Q = ", poss.value)
			if poss.node != None:
				poss.afficherArbre()

	#selectionne l'action maximisant q(s,a)+ucb(s,a)
	def Selection(self):
		if fin(self.etat) == 0:
			choix = 0
			u = []
			somme = 0
			for move in self.edges:
				somme += move.Prior_Proba/(1+move.visit_count)
			for move in self.edges:
				u.append((move.Prior_Proba/(1+move.visit_count))/somme)
			for i in range(len(self.edges)):
				if((u[i]+self.edges[i].value) > (u[choix]+self.edges[choix].value)):
					choix = i
			self.edges[choix].Selection()

	#calcule la somme des valeurs d'états du sous arbre et la fait remonter à la branche supérieure
	def Backpropagation(self):
		somme = 0
		for poss in self.edges:
			if(poss.node != None):
				somme += poss.Backpropagation()
		somme += self.value
		return somme

	#répète 500 cycles : sélection-expansion-evaluation-backpropagation
	#génère un vecteur de probabilités p(a|s) proportionnelles au nombre de visite de l'action
	def Decision(self):
		for i in range(500):
			self.Selection()
			self.Backpropagation()
		somme = 0
		for move in self.edges:
			somme += move.visit_count
		p = []
		for move in self.edges:
			p.append(move.visit_count/somme)
		return (p, self.actions)

class Edge(object):

	#les branches correspondent aux doublet (s,a)
	#chaque branche contient: le joueur censé jouer face à s
	#une action et un état
	#une prior probabilité donné par f_teta(s)
	#un nombre de visite
	#une valeur
	#un noeud correspondant à s', l'état après avoir effectué l'action a depuis l'état s
	#garde en mémoire un pointeur vers la classe f_teta

	def __init__(self, grille, coup, proba, joueur, f):
		self.player = joueur
		self.action = coup
		self.etat = grille
		self.Prior_Proba = proba
		self.visit_count = 0
		self.value = 0
		self.node = None
		self.function = f

	#si la branche à un fils elle le sélectionne
	#sinon elle le crée
	def Selection(self):
		self.visit_count += 1
		if self.node != None:
			self.node.Selection()
		else:
			self.Expansion()

	#création d'un nouveau noeud
	def Expansion(self):
		a = copie_grille(self.etat)
		placer(a, self.player, self.action[0], self.action[1])
		self.node = Node(a, self.player, self.function)

	#calcule son q(s,a)
	def Backpropagation(self):
		somme = self.node.Backpropagation()
		self.value = (1/self.visit_count)*somme
		return somme

	def afficherArbre(self):
		self.node.afficherArbre()

class f_teta(object):
	"""docstring for f_teta."""

	#fonction remplaçant le réseau de neurone
	#elle contient un tableau avec toute les valeurs
	#une ligne du tableau est [etat s, vecteur p, valeur v]

	def __init__(self):
		self.tableau = []

	#retourne l'index de la ligne correspondant à l'état s
	#retourne -1 s'il ne le trouve pas
	def find_state(self, grille):
		index = -1
		for i in range(len(self.tableau)):
			if comparer_grille(self.tableau[i][0], grille) == True:
				index = i
		return index

	#récupère les valeurs de la ligne de l'état s
	#si la ligne n'existe pas, on la crée
	def get_value(self, grille):
		index = self.find_state(grille)
		if index == -1:
			p = []
			action = getAction(grille)
			for move in action:
				p.append(1/len(action))
			self.tableau.append([grille, p, 0])
			index = self.find_state(grille)
		return (self.tableau[index][1], self.tableau[index][2])

	#met à jour les valeurs à l'aide d'une descente de gradiant
	def learn(self, grille, pi, resultat):
		index = self.find_state(grille)
		delta_v = 2*(self.tableau[index][2]-resultat)
		self.tableau[index][2] = self.tableau[index][2] - (0.3 * delta_v)
		somme = 0
		for i in range(len(pi)):
			delta_p = pi[i]/self.tableau[index][1][i]
			self.tableau[index][1][i] = self.tableau[index][1][i] + 0.3*delta_p
		somme = sum(self.tableau[index][1])
		for i in range(len(self.tableau[index][1])):
			self.tableau[index][1][i] = self.tableau[index][1][i]/somme

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

from random import random, choice, randint
f = f_teta()
for i in range(300): #entrainement de f_teta, modifiez ce nombre pour changer le nombre de partie pour l'entrainement
	print(i)
	a = initialisation()
	joueur = 0
	episode = []
	while fin(a) == 0:
		joueur = joueur%2
		joueur += 1
		arbre = Node(a, joueur, f)
		p, c = arbre.Decision()
		episode.append([copie_grille(a), p, 0])
		choix = random()
		d = 0
		coup = -1
		for prob in p:
			if(d >= choix):
				break
			else:
				d+=prob
				coup+=1
		placer(a, joueur, c[coup][0], c[coup][1])
	gagnant = fin(a)
	print("bravo ", gagnant)
	print(gagnant)
	if gagnant == 2:
		gagnant = -1
	if gagnant == 3:
		gagnant = 0
	for ep in episode:
		ep[2] = gagnant
		f.learn(ep[0], ep[1], ep[2])
while True: #l'utilisateur joue contre l'IA
	joueur = 0
	a = initialisation()
	while fin(a) == 0:
		joueur=joueur%2
		joueur+=1
		print("joueur = ", joueur)
		if joueur == 1: 
			arbre = Node(a, joueur, f)
			p, c = arbre.Decision()
			choix = random()
			d = 0
			coup = -1
			for prob in p:
				if(d >= choix):
					break
				else:
					d+=prob
					coup+=1
			placer(a, joueur, c[coup][0], c[coup][1])
			afficher(a)
		else:
			valide = False
			while valide == False:
				print("veuillez jouer" + str(joueur))
				l = int(input("ligne ?"))
				c = int(input("colonne ?"))
				valide = placer(a, joueur, l, c)
		afficher(a)
	print("bravo ")
