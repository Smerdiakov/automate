#####################################
## test pour les automates étoilés ##
#####################################

from execution import *
from automate import *
from etoile import *
import unittest
import random


longueur_mots = 150;

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
	

auto = automate()
auto.ajoute_initial(1)
auto.ajoute_final(2)
auto.ajoute_final(3)
auto.ajoute_transition(1,2,"a")
auto.ajoute_transition(2,3,"a")
auto.ajoute_transition(3,1,"a")
auto.ajoute_transition(1,1,"b")
auto.ajoute_transition(2,2,"b")
auto.ajoute_transition(3,3,"b")

auto_etoile = etoile(auto)

class test_etoile(unittest.TestCase):
	def test_etoile(self):
	
		for test in range(longueur_mots):
		
		# on va concatener 5 mots :
		
			liste_1 = liste_bits_alea(longueur_mots)
			mot_1 = mot_alea(liste_1)
			execut_1 = execution(auto)
			execut_1.execute(mot_1)
			
			liste_2 = liste_bits_alea(longueur_mots)
			mot_2 = mot_alea(liste_2)
			execut_2 = execution(auto)
			execut_2.execute(mot_2)
			
			liste_3 = liste_bits_alea(longueur_mots)
			mot_3 = mot_alea(liste_3)
			execut_3 = execution(auto)
			execut_3.execute(mot_3)
			
			liste_4 = liste_bits_alea(longueur_mots)
			mot_4 = mot_alea(liste_4)
			execut_4 = execution(auto)
			execut_4.execute(mot_4)
			
			liste_5 = liste_bits_alea(longueur_mots)
			mot_5 = mot_alea(liste_5)
			execut_5 = execution(auto)
			execut_5.execute(mot_5)
		
			execut_etoile = execution(auto_etoile)
			execut_etoile.execute(mot_1+mot_2+mot_3+mot_4+mot_5)
		
		# on vérifie si la propriété de concatenation est vérifiée :
			if (execut_1.bool and execut_2.bool and execut_3.bool and execut_4.bool and execut_5.bool):
				if(execut_etoile.bool):
					pass
				else :
					print("la concatenation de fonctionnne pas pour les mots :\n",mot_1,"\n", mot_2,"\n", mot_3,"\n", mot_4,"\n", mot_5)
				self.assertTrue(execut_etoile.bool)
			
if __name__=="__main__":
	print("\n")
	print(" --------------------------------------------")
	print("   debut du test sur les automates étoilés :")
	print(" --------------------------------------------")
	print("\n")
	unittest.main()