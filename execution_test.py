#########################################
## test pour l'execution d'un automate ##
#########################################

from execution import *
from automate import *
import unittest
import random

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

# cet automate à epsilon-transition reconnait les mot a*b* ou b*a*
auto_eps = automate()
auto_eps.ajoute_initial(1)
auto_eps.ajoute_final(2)
auto_eps.ajoute_initial(3)
auto_eps.ajoute_final(4)
auto_eps.ajoute_transition(1,1,"a")
auto_eps.ajoute_transition(2,2,"b")
auto_eps.ajoute_transition(3,3,"b")
auto_eps.ajoute_transition(4,4,"a")
auto_eps.ajoute_epsilon(1,2)
auto_eps.ajoute_epsilon(3,4)

longueur_mots = 900

def mot_alea (liste_bits):
	mot = ""
	for bit in liste_bits:
		if bit == 0 :
			mot = mot + "a"
		else:
			mot = mot + "b"
	return mot
	
def liste_bits_alea (taille) :
	liste_bits = []
	for entier in range(taille):
		liste_bits.append(random.randint(0,1))
	return liste_bits
	
def nombre_de_zeros_mod_3 (liste_bits):
	nombre = 0
	for bit in liste_bits:
		if bit==0 :
			nombre = nombre +1
	nombre = nombre % 3
	return nombre


# pour vérifier la propriété de l'automate à epsilon-transitions	
def propriete_3(chaine,lettre_ref):
	booleen = True
	booleen_b = False
	for lettre in chaine :
		if lettre==lettre_ref:
			booleen_b = True
		else:
			if booleen_b:
				booleen = False
	return booleen
				
# pour créer des mots qui véirifent cette propriété :
def liste_propriete_3(long):
	bit = random.randint(0,1)
	changement = random.randint(1,long-1)
	liste = []
	for entier in range(changement):
		liste.append(bit)
	for entier in range(long-changement):
		liste.append(1-bit)
	return liste
		
				
class test_execution (unittest.TestCase):

	def test_auto_det (self):
		for test in range(100):
			liste = liste_bits_alea(longueur_mots)
			mot = mot_alea(liste)
			nombre = nombre_de_zeros_mod_3(liste)
			execut = execution(auto_det,mot)
			execut.execute()
			if execut.bool :
				self.assertEqual(nombre,0)
			else:
				self.assertNotEqual(nombre,0)

	def test_auto_ndet (self):
		for test in range(100):
			liste = liste_bits_alea(longueur_mots)
			mot = mot_alea(liste)
			execut = execution(auto_ndet,mot)
			execut.execute()
			if (((liste[longueur_mots-1]==0)or((liste[longueur_mots-1]==1)and(liste[longueur_mots-2]==0))) == execut.bool):
				pass
			else : 
				print("le test ne fonctionne pas pour ce mot : ")
				print(mot)
				self.assertTrue(((liste[longueur_mots-1]==0)or((liste[longueur_mots-1]==1)and(liste[longueur_mots-1]==1))) == execut.bool)
	
	def test_auto_eps(self):
		for test in range(100):
			liste = []
			if random.randint(0,1)==1:			
				liste = liste_bits_alea(longueur_mots)
			else:
				liste = liste_propriete_3(longueur_mots)
			mot = mot_alea(liste)
			execut = execution(auto_eps,mot)
			execut.execute()
			if (((propriete_3(mot,"a"))or(propriete_3(mot,"b"))) == execut.bool):
				pass
			else : 
				print("le test ne fonctionne pas pour ce mot : ")
				print(mot)
				self.assertTrue(((propriete_3(mot,"a"))or(propriete_3(mot,"b"))) == execut.bool)



if __name__=="__main__":
	print("\n")
	print(" ------------------------------------------")
	print("   debut du test sur la classe execution :")
	print(" ------------------------------------------")
	print("\n")
	unittest.main()