###########################
# Union de deux automates #
###########################

# cette fonction prend en argument 2 automates A1 et A2 
# qui reconnaissent un ensemble de mots X1 et X1 et construit 
# un automate qui reconnait l'ensemble X1 union X2.

from automate import *

def reunion (auto1,auto2):
	auto_ou = automate()
	
	