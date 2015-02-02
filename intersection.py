############################
# intersection d'automates #
############################

# cette fonction prend en argument 2 automates A1 et A2 
# qui reconnaissent un ensemble de mots X1 et X2 et construit 
# un automate qui reconnait l'ensemble X1 inter X2.

# On va utiliser les automates produits 

# les automates produits sont étiquetés par des couples . 
# Il peut être utile de refaire l'étiquetage après l'exécution 
# de l'algorithme pour une meilleure lisibilitée.

# la fonction à appeler est inter.

from automate import *

def inter (auto1, auto2):
	liste_etats_1 = auto1.liste_etats()
	liste_etats_2 = auto2.liste_etats()
	
	alph1 = auto1.alphabet()
	alph2 = auto2.alphabet()
	
	# l'intersection des deux alphabet :	
	alph = intersection (alph1, alph2)
	
	# creation des etats de l'automate produit :
	auto_produit = etats_produits(liste_etats_1,liste_etats_2)
	
	# on relie les etats du nouvel automate :
	for etat1 in liste_etats_1:
		for etat2 in liste_etats_2:
			for lettre in alph:
				# on regarde l'image de (etat1,etat2)
				# et on relie :
				for etat in image(etat1, auto1, etat2,auto2, lettre):
					auto_produit.ajoute_transition((etat1,etat2),etat,lettre)
	
	# on gère les états initiaux et finaux :
	gestion_initiaux(auto_produit, auto1, auto2)
	gestion_finaux(auto_produit, auto1, auto2)	
	
	return auto_produit
	
# creation des etats de l'automate produit :
def etats_produits(liste_etats_1,liste_etats_2):
	auto_produit = automate()
	for etat1 in liste_etats_1:
		for etat2 in liste_etats_2:
			auto_produit.ajoute_etat((etat1,etat2))
	return auto_produit
			

# l'intersection de deux liste :	
def intersection (liste1, liste2):
	liste_inter = []
	for element in liste1:
		if element in liste2:
			liste_inter.append(element)
	return liste_inter

# image d'un couple d'état :
def image(etat1, auto1, etat2, auto2, lettre):
	liste1 = auto1.image(etat1, lettre)
	liste2 = auto2.image(etat2, lettre)
	return produit_carthesien( liste1, liste2)
	
# produit carthésien de 2 listes :
def produit_carthesien( liste1, liste2):

# gestion des etats initiaux :
def gestion_initiaux(auto_produit, auto1, auto2):

# gestion des etats finaux :
def gestion_finaux(auto_produit, auto1, auto2):
