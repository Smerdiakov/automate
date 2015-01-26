##############################################
## test pour la concatenation d'un automate ##
##############################################

# les tests sont semblables aux tests pour la fonction union

from execution import *
from automate import *
from concatenation import *
import unittest
import random

longueur_mots = 100;

# transforme la liste de bits en mot avec les lettres a et b.
def mot_alea (liste_bits):
	mot = ""
	for bit in liste_bits:
		if bit == 0 :
			mot = mot + "a"
		else:
			mot = mot + "b"
	return mot
	
# renvoie une liste aléatoire de bits		
def liste_bits_alea (taille) :
	liste_bits = []
	for entier in range(random.randint(1,taille)):
		liste_bits.append(random.randint(0,1))
	return liste_bits
	
# pour vérifier les propriétés de l'automate déterministe
def nombre_de_zeros_mod_3 (liste_bits):
	nombre = 0
	for bit in liste_bits:
		if bit==0 :
			nombre = nombre +1
	nombre = nombre % 3
	return nombre

# cet automate déterministe reconnait les mots qui vérifient la propriété suivante :
# le nombre de a dans le mot est un multiple de 3.

auto_det = automate()
auto_det.ajoute_initial(1)
auto_det.ajoute_final(1)
auto_det.ajoute_etat(2)
auto_det.ajoute_etat(3)
auto_det.ajoute_transition(1,1,"b")
auto_det.ajoute_transition(2,2,"b")		
auto_det.ajoute_transition(3,3,"b")
auto_det.ajoute_transition(1,2,"a")
auto_det.ajoute_transition(2,3,"a")
auto_det.ajoute_transition(3,1,"a")

# cet automate non déterministe reconnait les mots qui se terminent par a ou par ab
auto_ndet = automate()
auto_ndet.ajoute_initial(1)
auto_ndet.ajoute_final(2)
auto_ndet.ajoute_final(3)
auto_ndet.ajoute_transition(1,2,"a")
auto_ndet.ajoute_transition(1,1,"a")
auto_ndet.ajoute_transition(1,1,"b")
auto_ndet.ajoute_transition(2,3,"b")

auto_concat = concat(auto_det,auto_ndet)

class test_union(unittest.TestCase):
	def test_union (self):
		for test in range(longueur_mots):
			liste_1 = liste_bits_alea(longueur_mots)
			liste_2 = liste_bits_alea(longueur_mots)
			mot_1 = mot_alea(liste_1)
			mot_2 = mot_alea(liste_2)
			
			execut_det = execution(auto_det)
			execut_det.execute(mot_1)
		
			execut_ndet = execution(auto_ndet)
			execut_ndet.execute(mot_2)
		
			execut_concat = execution(auto_concat)
			execut_concat.execute(mot_1+mot_2)
		
		# on vérifie si la propriété de concatenation des vérifiée :
			if execut_det.bool and execut_ndet.bool, execut_concat.bool :
				pass
			else :
				print("la concatenation de fonctionnne pas pour les mots :\n",mot_1,"\n et :\n", mot_2)
			self.assertEqual( execut_det.bool and execut_ndet.bool, execut_concat.bool)

if __name__=="__main__":
	print("\n")
	print(" ----------------------------------------------")
	print("   debut du test sur la classe concatenation :")
	print(" ----------------------------------------------")
	print("\n")
	unittest.main()
