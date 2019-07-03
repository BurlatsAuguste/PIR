# PIR
Guide d'utilisation:

AlphaUno.py est mon programme inspiré de AlphaZero. Pour le lancer il suffit d'entrer la commande python AlphaUno.py

Epsilon_greedy.py est un programme pour entrainer une politique epsilon-greedy. 
Pour le lancer il faut rentrer python Epsilon_greedy.py charge? emplacement_charge emplacement_sauvegarde epsilon nbrEntrainement
avec charge? = 1 si vous voulez charger un fichier, 0 si non
emplacement_charge est le chemin vers le fichier que vous voulez charger, veuillez le remplir même si vous ne voulez pas charger de fichier
emplacement_sauvegarde est le chemin vers le fichier dans lequel vous voulez effectuer votre sauvegarde, si le programme ne le trouve pas il le créera
epsilon correspond à la valeur de epsilon
nbrEntrainement correspond au nombre de partie à effectuer pour s'entrainer

UCB.py est un programme pour entrainer une politique avec un ucb.
Pour le lancer il faut rentrer python UCB.py charge? emplacement_charge emplacement_sauvegarde c nbrEntrainement
avec charge? = 1 si vous voulez charger un fichier, 0 si non
emplacement_charge est le chemin vers le fichier que vous voulez charger, veuillez le remplir même si vous ne voulez pas charger de fichier
emplacement_sauvegarde est le chemin vers le fichier dans lequel vous voulez effectuer votre sauvegarde, si le programme ne le trouve pas il le créera
c correspond à la valeur du paramètre réglant le taux d'exploration, si c=2 ce paramètre vaudra sqrt(2)
nbrEntrainement correspond au nombre de partie à effectuer pour s'entrainer

MCP_vs_MCP.py permet à deux sauvegardes de s'affronter.
Pour le lancer il faut rentrer python MCP_vs_MCP.py emplacementJ1 emplacementJ2 nbrParties
emplacementJ1 est le chemin vers la sauvegarde du joueur 1
emplacementJ2 est le chemin vers la sauvegarde du joueur 2
nbrParties est le nombre de Parties

MCP_vs_MCTS.py permet à une sauvegarde d'affronter le MCTS
Pour le lancer il faut rentrer python MCP_vs_MCTS.py emplacementSauvegarde J nbrParties
emplacementSauvegarde est le chemin vers la sauvegarde
J = 1 si vous voulez que le MCTS soit joueur 1, J = 2 si vous voulez qu'il soit joueur 2
nbrParties est le nombre de Parties

MonteCarloTreeSearch.py permet à l'utilisateur d'affronter le MCTS
Pour le lancer il faut rentrer python MonteCarloTreeSearch.py J
J = 1 si vous voulez que le MCTS soit joueur 1, J = 2 si vous voulez qu'il soit joueur 2

humain_vs_MCP.py permet à l'utilisateur d'affronter une sauvegarde
Pour le lancer il faut rentrer python humain_vs_MCP.py emplacementSauvegarde J
emplacementSauvegarde est le chemin vers la sauvegarde
J =1 si l'utilisateur est joueur 1, j=2 s'il est joueur 2


Explication des noms des sauvegardes:
save_epsilon03_5000 signifie que la politique a été entrainée en epsilon-greedy, avec epsilon = 0.3 et pendant 5000 parties
save_ucb_2_2500 signifie que la politique a été entrainée avec une exploration controlée par un ucb, avec c=sqrt(2) et pendant 2500 parties















