###################################
## déterminisation d'un automate ##
###################################

# la classe determinisation() prend un automate en argument
# et le déterminise.

# Attention : il faut créer 1 objet de la classe déterminisation pour chaque automate !

# Attention : les états de l'automate déterminisé seront étiquetés par des ensembles
# et non pas par des entiers. penser à etiqueter de nouveau si nécessaire. 

from automate import *

class determinisation :

	def __init__(self,automate_init):
		self.auto = automate_init
		self.auto_det = automate()
		
# LA FONCTION A UTILISER EN PRATIQUE ! #

	def determinise(self):
		self.determine()
		return self.auto_det
	
### partie 1 : la supression des epsilon-transitions ###
########################################################
	
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
			
### partie 2 : la déterminisation ###
#####################################

	def etat_initial(self):
		ensemble_de_depart = frozenset(self.auto.initial)
		self.auto_det.ajoute_initial(ensemble_de_depart)
		
	def etat_finaux(self):
		liste_etats_det = self.auto_det.liste_etats()
		liste_final = self.auto.final
		for etat_det in liste_etats_det :
			for etat in liste_final :
				if etat in etat_det:
					self.auto_det.ajoute_final(etat_det)
					
	def determine(self):
		self.suppr_epsilon()
		self.etat_initial()
		booleen = True
		alph = self.auto.alphabet()
		while booleen :
			booleen = False
			for lettre in alph:
				etats_existants = self.auto_det.liste_etats()
				for etat in etats_existants :
					etat_suivant = self.auto.image_liste_set(etat, lettre )
					if etat_suivant in etats_existants :
						self.auto_det.ajoute_transition(etat,etat_suivant,lettre)
					elif not(etat_suivant==frozenset()):					
						self.auto_det.ajoute_etat(etat_suivant)
						booleen = True
		self.etat_finaux()	
					
				
				
				
		