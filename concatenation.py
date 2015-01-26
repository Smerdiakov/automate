###################################
# Concatenation de deux automates #
###################################

from automate import *
from union import *

# cette fonction concatène 2 automates A et B

# ie : si a est reconnu par A et b reconnu par B
# alors l'automate concaténé reconnait le mot
# alors a.b (concaténation de 2 strings)

# Réciproquement, si l'automate concaténé reconnait un mot c,
# alors il existe a reconnu par A et b reconnu par B tels que :
# c = a.b (concaténation de 2 strings)

# l'algorithme effectue premièrement une réunion des deux automates puis
# banalise les états initiaux du deuxième automate  et les états finaux 
# du premier automate et les relie 2 à 2.

def concat (auto_1, auto_2):
	auto_concat = reunion(auto_1, auto_2)
	taille_1 = auto1.nombre_etat()
	taille_2 = auto2.nombre_etat()
	
	# liste des états finaux de l'automate 1
	liste_final_1 = remplit_final_1(auto_concat, taille_1)
	#liste des états initiaux de l'automate 2
	liste_initial_2= remplit_initial_2(auto_concat, taille_1, taille_2)
	
	for etat_1 in liste_final_1:
		for etat_2 in liste_initial_2:
			auto_concat.ajoute_epsilon(etat_1,etat_2)
			
	return auto_concat
	
	

def remplit_final_1(auto_concat, taille_1):
	liste = []
	for entier in range(1, taille_1+1):
		if entier in auto_concat.final:
			liste.append(entier)
			auto_concat.final.remove(entier)
	return liste		
			
def remplit_initial_2(auto_concat, taille_1, taille_2):
	liste = []
	for entier in range(taille_1+1, taille_2+1):
		if entier in auto_concat.initial:
			liste.append(entier)
			auto_concat.initial.remove(entier)
	return liste
			
			

			