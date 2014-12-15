#######################################
## Les tests pour la classe automate ##
#######################################

from automate import *
import unittest
import random

class test_unitaire (unittest.TestCase):

	def test_ajoute_etat(self):
		auto_test = automate()
		self.assertTrue(auto_test.est_vide)
		self.assertEqual(auto_test.nombre_etat(),0)
		auto_test.ajoute_etat(1)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_etat(),1)
		auto_test.ajoute_etat(2)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_etat(),2)
		auto_test.ajoute_etat(3)
		self.assertEqual(auto_test.nombre_etat(),3)
		self.assertFalse(auto_test.est_vide())
		
	def test_ajoute_initial(self):
		auto_test = automate()
		self.assertTrue(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_initial(),0)
		auto_test.ajoute_etat(1)
		auto_test.ajoute_initial(1)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_initial(),1)
		auto_test.ajoute_initial(2)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_initial(),2)
		self.assertEqual(auto_test.nombre_etat(),2)
	
	def test_ajoute_final(self):
		auto_test = automate()
		self.assertTrue(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_final(),0)
		auto_test.ajoute_etat(1)
		auto_test.ajoute_final(1)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_final(),1)
		auto_test.ajoute_final(2)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_final(),2)
		self.assertEqual(auto_test.nombre_etat(),2)
		
	def test_ajoute_transition(self):
		auto_test = automate()
		self.assertEqual(auto_test.transition,{})
		auto_test.ajoute_etat(1)
		auto_test.ajoute_etat(2)
		auto_test.ajoute_etat(3)
		auto_test.ajoute_etat(4)
		self.assertEqual(auto_test.nombre_transitions(),0)
		auto_test.ajoute_transition(1,2,"a")
		auto_test.ajoute_transition(1,3,"a")
		auto_test.ajoute_transition(2,2,"a")
		self.assertEqual(auto_test.nombre_transitions(),3)
		self.assertEqual(len(auto_test.alphabet()),1)
		auto_test.ajoute_transition(4,2,"b")
		auto_test.ajoute_transition(4,3,"b")
		auto_test.ajoute_transition(2,4,"b")
		self.assertEqual(auto_test.nombre_transitions(),6)
		self.assertEqual(len(auto_test.alphabet()),2)
		
	def test_ajoute_liste_etat(self):
		auto_test=automate()
		etat = 200
		liste_etat = range(etat)
		auto_test.ajoute_liste_etat(liste_etat)
		self.assertEqual(auto_test.nombre_etat(),etat)
		
	def test_ajoute_liste_initial(self):
		auto_test=automate()
		etat = 200
		liste_etat = range(etat)
		auto_test.ajoute_liste_initial(liste_etat)
		self.assertEqual(auto_test.nombre_etat(),etat)
		self.assertEqual(auto_test.nombre_initial(),etat)
		
	def test_ajoute_liste_transition(self):
		auto_test=automate()
		etat = 200
		liste_etat = range(etat)
		liste_transition = []
		for etat1 in liste_etat:
			for etat2 in liste_etat:
				depart = etat1
				lettre = random.randint(0,etat)
				arrive = etat2
				liste_transition.append((depart,arrive,lettre))
		auto_test.ajoute_liste_etat(liste_etat)
		auto_test.ajoute_liste_transition(liste_transition)
		self.assertEqual(auto_test.nombre_etat(),etat)
		self.assertEqual(auto_test.nombre_transitions(),etat*etat)
		auto_test.ajoute_initial(0)
		self.assertTrue(auto_test.est_correct())

		
	def test_ajoute_epsilon(self):
		auto_test = automate()
		self.assertTrue(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_initial(),0)
		self.assertEqual(len(auto_test.alphabet()),0)
		auto_test.ajoute_etat(1)
		auto_test.ajoute_etat(2)
		auto_test.ajoute_etat(3)
		auto_test.ajoute_epsilon(1,2)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_epsilon(),1)
		self.assertEqual(len(auto_test.alphabet()),0)
		auto_test.ajoute_epsilon(2,3)
		self.assertFalse(auto_test.est_vide())
		self.assertEqual(auto_test.nombre_epsilon(),2)
		self.assertEqual(auto_test.nombre_etat(),3)
		self.assertEqual(len(auto_test.alphabet()),0)
		
	def test_ajoute_liste_epsilon(self):
		auto_test=automate()
		etat = 50
		liste_etat = range(etat)
		liste_transition = []
		for etat1 in liste_etat:
			for etat2 in liste_etat:
				depart = etat1
				arrive = etat2
				liste_transition.append((depart,arrive))
		auto_test.ajoute_liste_etat(liste_etat)
		auto_test.ajoute_liste_epsilon(liste_transition)
		self.assertEqual(auto_test.nombre_etat(),etat)
		self.assertEqual(auto_test.nombre_transitions(),etat*etat)
		auto_test.ajoute_initial(0)
		self.assertTrue(auto_test.est_correct())
		
	def test_supprime_etat(self):
		auto_test=automate()
		etat = 100
		liste_etat = range(etat)
		liste_transition = []
		for etat1 in liste_etat:
			for etat2 in liste_etat:
				depart = etat1
				lettre = random.randint(0,etat)
				arrive = etat2
				liste_transition.append((depart,arrive,lettre))
		auto_test.ajoute_liste_etat(liste_etat)
		auto_test.ajoute_liste_transition(liste_transition)		
		for etat2 in range(30):
			if etat2%2==0:
				auto_test.ajoute_initial(etat2)
			else:
				auto_test.ajoute_final(etat2)
		auto_test.ajoute_initial(80)
		
		for etat_suppr in range(50):
			self.assertEqual(auto_test.nombre_etat(),etat-etat_suppr)
			auto_test.supprime_etat(etat_suppr)

		self.assertTrue(auto_test.est_correct())
		
	def test_supprime_transition(self):
		auto_test=automate()
		etat = 100
		liste_etat = range(etat)
		liste_transition = []
		for etat1 in liste_etat:
			for etat2 in liste_etat:
				lettre = etat1+etat2
				liste_transition.append((etat1,etat2,lettre))
		auto_test.ajoute_liste_etat(liste_etat)
		auto_test.ajoute_liste_transition(liste_transition)		
		for etat2 in range(30):
			if etat2%2==0:
				auto_test.ajoute_initial(etat2)
			else:
				auto_test.ajoute_final(etat2)
		auto_test.ajoute_initial(80)
		
		for etat1 in range(70):
			self.assertEqual(auto_test.nombre_transitions(),etat*etat-2*etat1)
			auto_test.supprime_transition(etat1,etat1,2*etat1)
			auto_test.supprime_transition(etat1,etat1+1,2*etat1+1)
			
		self.assertTrue(auto_test.est_correct())
		
	def test_supprime_lettre(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.nombre_transitions(),6)
		self.assertEqual(len(auto_test.alphabet()),2)
		auto_test.supprime_lettre("a")
		self.assertEqual(auto_test.nombre_transitions(),3)
		self.assertEqual(len(auto_test.alphabet()),1)
		
	def test_est_correct(self):
		auto_test=automate()
		auto_test.pour_le_test()
		del auto_test.transition[4]
		self.assertFalse(auto_test.est_correct())
		
	def test_est_initial(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertTrue(auto_test.est_initial(2))
		self.assertFalse(auto_test.est_initial(1))
		self.assertFalse(auto_test.est_initial(3))
		self.assertFalse(auto_test.est_initial(4))
		
	def test_est_final(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertTrue(auto_test.est_final(4))
		self.assertFalse(auto_test.est_final(1))
		self.assertFalse(auto_test.est_final(3))
		self.assertFalse(auto_test.est_final(2))
		
	def test_image(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertTrue(2 in auto_test.image(1,"a"))
		self.assertTrue(2 in auto_test.image(4,"b"))
		self.assertFalse(4 in auto_test.image(1,"a"))
		self.assertFalse(1 in auto_test.image(2,"b"))
		
	def test_alphabet(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.alphabet(),{"a","b"})
		self.assertNotEqual(auto_test.alphabet(),{"a"})
		self.assertNotEqual(auto_test.alphabet(),{"b"})		
		self.assertNotEqual(auto_test.alphabet(),{"a","b","c"})
		
	def test_est_deterministe(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertFalse(auto_test.est_deterministe())
		auto_test.supprime_transition(1,3,"a")
		self.assertFalse(auto_test.est_deterministe())
		auto_test.supprime_transition(4,3,"b")
		self.assertTrue(auto_test.est_deterministe())
		
	def test_nombre_etat(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.nombre_etat(),4)
	
	def test_nombre_initial(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.nombre_initial(),1)
		
	def test_nombre_final(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.nombre_final(),1)
		
	def test_nombre_transitions(self):
		auto_test=automate()
		auto_test.pour_le_test()
		self.assertEqual(auto_test.nombre_transitions(),6)
	
	def test_nombre_epsilon(self):
		auto_test=automate()
		auto_test.pour_le_test()
		auto_test.ajoute_epsilon(1,4)
		self.assertEqual(auto_test.nombre_epsilon(),1)
		
		
if __name__=="__main__":
	print("\n")
	print(" ------------------------------------------")
	print("   debut du test sur la classe automate :")
	print(" ------------------------------------------")
	print("\n")
	unittest.main()