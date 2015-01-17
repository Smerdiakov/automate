################################################
## test pour la déterminisation d'un automate ##
################################################

from automate import *
from execution import *
from determinisation import *
import unittest
import random

longueur_mots = 30

# renvoie un mot aléatoire
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

class test_determinisation (unittest.TestCase):

	def test_suppr_epsilon(self):
		auto_test=automate()
		auto_test.pour_le_test()
		auto_test.ajoute_final(3)
		det_test = determinisation(auto_test)
		self.assertFalse(det_test.auto.est_sans_epsilon())
		det_test.suppr_epsilon()
		self.assertTrue(det_test.auto.est_sans_epsilon())
# il faut aussi voir si l'algorithme de change pas l'ensemble des mots reconnus par l'automate :
		exec_test = execution(auto_test)
		exec_test.solution("bbaa")
		self.assertTrue(exec_test.bool)
		exec_test.solution("bbaaa")
		self.assertTrue(exec_test.bool)
		exec_test.solution("bbabb")
		self.assertTrue(exec_test.bool)
		exec_test.solution("a")
		self.assertTrue(exec_test.bool)
		exec_test.solution("abbba")
		self.assertFalse(exec_test.bool)
		
	def test_determine(self):
		auto_test=automate()
		auto_test.pour_le_test()
		auto_test.ajoute_final(3)
		det_test = determinisation(auto_test)
		auto_det = det_test.determinise()
		exec_test = execution(auto_det)
		exec_test.solution("bbaa")
		self.assertTrue(exec_test.bool)
		exec_test.solution("bbaaa")
		self.assertTrue(exec_test.bool)
		exec_test.solution("bbabb")
		self.assertTrue(exec_test.bool)
		exec_test.solution("a")
		self.assertTrue(exec_test.bool)
		exec_test.solution("abbba")
		self.assertFalse(exec_test.bool)
		
# un test aleatoire sur un plus gros automate :
	def test_determinise(self):
		auto_test=automate()
		auto_test.ajoute_initial(1)
		auto_test.ajoute_initial(2)
		auto_test.ajoute_final(3)
		auto_test.ajoute_final(4)
		auto_test.ajoute_etat(5)
		auto_test.ajoute_etat(6)
		auto_test.ajoute_epsilon(1,5)
		auto_test.ajoute_epsilon(6,3)
		auto_test.ajoute_epsilon(3,2)
		auto_test.ajoute_transition(1,2,'a')
		auto_test.ajoute_transition(2,3,'a')
		auto_test.ajoute_transition(3,6,'a')
		auto_test.ajoute_transition(1,5,'b')
		auto_test.ajoute_transition(3,5,'b')
		auto_test.ajoute_transition(5,2,'b')
		auto_test.ajoute_transition(5,6,'b')
		auto_test.ajoute_transition(5,4,'a')
		
		det_test = determinisation(auto_test)
		auto_det = det_test.determinise()
		exec_test = execution(auto_test)
		exec_test_det = execution(auto_det)
		
		for test in range(100):
			mot = mot_alea(liste_bits_alea(longueur_mots))
			exec_test.execute(mot)
			exec_test_det.execute(mot)
			self.assertEqual(exec_test.bool, exec_test_det.bool)
	

if __name__=="__main__":
	print("\n")
	print(" -------------------------------------------------")
	print("   debut du test sur la classe determinisation :")
	print(" -------------------------------------------------")
	print("\n")
	unittest.main()