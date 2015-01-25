###########################
# Union de deux automates #
###########################

# cette fonction prend en argument 2 automates A1 et A2 
# qui reconnaissent un ensemble de mots X1 et X1 et construit 
# un automate qui reconnait l'ensemble X1 union X2.

# cet algorithme est inspié de la methode nouvelles_étiquetes

from automate import *

def reunion (auto1,auto2):
	auto1.nouvelles_etiquettes()
	auto_ou = auto1
	
	correspondance = {}
	nouvel_entier = auto1.nombre_etat()+1
		
	for depart in auto2.transition:
		if not depart in correspondance :
			correspondance[depart]=nouvel_entier
			nouvel_entier = nouvel_entier+1
			
		for lettre in auto2.transition[depart]:
			for arrivee in auto2.transition[depart][lettre]:
			
				if not arrivee in correspondance :
					correspondance[arrivee]=nouvel_entier
					nouvel_entier = nouvel_entier +1
						
				auto_ou.ajoute_transition(correspondance[depart],correspondance[arrivee],lettre)
				
	for etat in auto2.initial:
		if not etat in correspondance :
			correspondance[etat]=nouvel_entier
			nouvel_entier = nouvel_entier +1
		auto_ou.ajoute_initial(correspondance[etat])
		
	for etat in auto2.final:
		if not etat in correspondance :
			correspondance[etat]=nouvel_entier
			nouvel_entier = nouvel_entier +1
		auto_ou.ajoute_final(correspondance[etat])
		
	return auto_ou
			
