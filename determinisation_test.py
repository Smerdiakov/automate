################################################
## test pour la déterminisation d'un automate ##
################################################

from automate import *
from execution import *
from determinisation import *
import unittest
import random

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

if __name__=="__main__":
	print("\n")
	print(" -------------------------------------------------")
	print("   debut du test sur la classe determinisation :")
	print(" -------------------------------------------------")
	print("\n")
	unittest.main()