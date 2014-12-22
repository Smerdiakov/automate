#############################
## execution d'un automate ##
#############################

# on fait une classe specifique pour l'execution de l'automate.
# ceci va nous permettre d'implémenter l'execution pas à pas de l'automate.

# la classe va prendre comme arguments :
#	- l'automate
#	- le mot avec lequel on va executer l'automate.

# la classe automate doit vérifier si le mot est reconnu par l'automate 
# et la cas échéant va renvoyer la suite des états à visiter pour que le mot soit accepté.

import automate

class execution :
	def __init__(self, auto_arg, mot_arg):
		self.automate.auto = auto_arg
		self.mot = mot_arg
		self.suite = []
	
	