###################################
## déterminisation d'un automate ##
###################################

# la classe determinisation() prend un automate en argument
# et le déterminise.

from automate import *

class determinisation :

	def __init__(self,automate_init):
		self.auto = automate_init
		
# suppression des epsilon-transitions :
	def suppr_epsilon(self):
		liste_etat = self.auto.liste_etats()
		liste_initial = self.auto.initial
		for etat in liste_etat :
			self.suppr_epsilon_etat(etat)
		for etat in liste_initial:
			self.ajoute_init(etat)
		self.auto.supprime_lettre("")
		
# remplace une transition epsilon par son équivalent sans epsilon :	
	def suppr_epsilon_etat(self,etat):
		alph = self.auto.alphabet()
		for lettre in alph :
			self.suppr_epsilon_lettre(etat,lettre)
		
# la même chose mais lettre par lettre :
	def suppr_epsilon_lettre(self,etat,lettre):
		liste_suivants = self.auto.image_epsilon(etat)
		liste_precedent = self.auto.preimage(etat,lettre)
		for etat_suivant in liste_suivants:
			for etat_precedent in liste_precedent:
				self.auto.ajoute_transition(etat_precedent, etat_suivant, lettre)
				
# ajout d'états initiaux le long de la epsilon-image d'un etat initial :
	def ajoute_init(self, etat_initial):
		liste_etat = self.auto.image_epsilon(etat_initial)
		for etat in liste_etat:
			self.auto.ajoute_initial(etat)