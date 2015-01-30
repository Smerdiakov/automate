#####################
# l'automate étoilé #
#####################

# on dispose d'un automate A et on souhaite construire l'automate A*
# où A* est l'automate étoilé associé à A, c'est-à-dire l'automate qui reconnait 
# toutes concatenations de plusieurs mots reconnus par A.

# la fonction a appeler est "etoile".

from automate import *

def etoile (auto):
	nouvel_auto = auto;
	
	# un rajoute un nouvel etat 0 (ou autre si 0 est déja pris)
	nouvel_etat = etiquette_nouvel_etat(nouvel_auto)
	nouvel_auto.ajoute_etat(nouvel_etat)
	
	# on rajoute des epsilon transitions 0 --> i  pour tout i état initial de l'automate
	ajoute_transitions_initiales(nouvel_auto, nouvel_etat)
	
	# on rajoute des epsilon transitions j --> 0 pour tout j état final de l'automate
	ajoute_transitions_finales(nouvel_auto, nouvel_etat)
	
	# on transforme 0 en état initial et final.
	nouvel_auto.ajoute_initial(nouvel_etat)
	nouvel_auto.ajoute_final(nouvel_etat)
	
	return nouvel_auto;
	
def etiquette_nouvel_etat(auto):
	liste_etat = auto.liste_etats()
	nouvel_etat = 0
	
	# si 0 est déjà dans l'automate, on essaie un autre nombre.
	while (nouvel_etat in liste_etat):
		nouvel_etat = (nouvel_etat+1)*5
		
	return nouvel_etat
	
	
def ajoute_transitions_initiales(nouvel_auto, nouvel_etat):
	for etat_initial in nouvel_auto.initial:
		nouvel_auto.ajoute_epsilon(nouvel_etat, etat_initial)
		
def ajoute_transitions_finales(nouvel_auto, nouvel_etat):
	for etat_final in nouvel_auto.final:
		nouvel_auto.ajoute_epsilon(etat_final, nouvel_etat)
		
