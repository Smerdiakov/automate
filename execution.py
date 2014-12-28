#############################
## execution d'un automate ##
#############################

# on fait une classe specifique pour l'execution de l'automate.
# ceci va nous permettre d'implémenter l'execution pas à pas de l'automate.

# la classe va prendre comme arguments :
#	- l'automate
#	- le mot avec lequel on va executer l'automate.

# la classe automate doit vérifier si le mot est reconnu par l'automate 
# (elle renvoie un booleen)
# et la cas échéant va renvoyer la suite des états à visiter pour que le mot soit accepté.

from automate import *

class execution :
	def __init__(self, auto_arg, mot_arg):
		self.auto = auto_arg
		self.mot = mot_arg
		self.suite_etats = []
		self.bool = False
	
	# sous-fonction auxiliaire récursive
	def auxiliaire (self, etat, position):
	
		self.suite_etats.append(etat)
		
		if (position == len(self.mot)):
			if self.auto.est_final(etat):
				self.bool = True
			else:
				self.suite_etats.pop()
		
		else:
			etats_suivants = self.auto.image(etat, self.mot[position])
			etat_suivant = 0
			l_etats_suiv = len(etats_suivants)
						
			while( not(self.bool) and (etat_suivant<l_etats_suiv)):
				self.auxiliaire(etats_suivants[etat_suivant],position+1)
				etat_suivant = etat_suivant+1
				
			if not(self.bool):
				self.suite_etats.pop()
	
	# la fonction d'execution :
	def execute(self):
	
		etats_initiaux = self.auto.initial
		etat_init = 0
		l_etats_init = len(etats_initiaux)
		
		while( not(self.bool) and (etat_init<l_etats_init)):
			self.auxiliaire(etats_initiaux[etat_init],0)
			etat_init = etat_init+1
		
	