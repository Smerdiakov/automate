#####################
# l'automate étoilé #
#####################

# on dispose d'un automate A et on souhaite construire l'automate A*
# où A* est l'automate étoilé associé à A, c'est-à-dire l'automate qui reconnait 
# toutes concatenations de plusieurs mots reconnus par A.

# l'algorithme fonctionne comme ceci :
# un rajoute un nouvel etat 0 (ou autre si 0 est déja pris)
# on rajoute des epsilon transitions 0 --> i  pour tout i état initial de l'automate
# on rajoute des epsilon transitions j --> 0 pour tout j état final de l'automate
# on transforme 0 en état initial est final.

from automate import *

def etoile (auto):
	nouvel_etat = 0;
	nouvel_auto = auto;
	nouvel_etat = ajoute_etat_zero(nouvel_auto);
	ajoute_transitions_initiales(nouvel_auto, nouvel_etat);
	ajoute_transitions_finales(nouvel_auto, nouvel_etat);