#####################################
## test pour l'union d'un automate ##
#####################################

# on va reprendre des automates du test de execution,
# construire les réunions et vérifier si la propriété 
# d'union est toujours satisfaite

from execution import *
from automate import *
from union import *
import unittest
import random

longueur_mots = 400;

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

auto_union = reunion(auto_det,auto_ndet)

class test_union(unittest.TestCase):
	def test_union (self):
		for test in range(longueur_mots):
			liste = liste_bits_alea(longueur_mots)
			mot = mot_alea(liste)
			
			execut_det = execution(auto_det)
			execut_det.execute(mot)
		
			execut_ndet = execution(auto_ndet)
			execut_ndet.execute(mot)
		
			execut_union = execution(auto_union)
			execut_union.execute(mot)
		
		# on vérifie si l'ensemble des mots acceptés par auto_union
		# est la réunion des 2 ensembles de mots acceptés resp.
		# par auto_det et auto_ndet
			if execut_union.bool:
				self.assertTrue(execut_det.bool or execut_ndet.bool)
			else:
				self.assertFalse(execut_det.bool or execut_ndet.bool)

if __name__=="__main__":
	print("\n")
	print(" -------------------------------")
	print("   debut du test sur l' union :")
	print(" -------------------------------")
	print("\n")
	unittest.main()
