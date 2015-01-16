######################################################
## Test pour la representaton graphique du automate ##
######################################################

from automate_graphique import *
from classe_etat_transittion import *
from PyQt4 import QtGui
import unittest


############  Creation d'un automate
coleur = (255,255,255)
etat0 = Etat("0",False)
etat1 = Etat("1",False)
etat2 = Etat("2",True)
etat3 = Etat("3",False)
etat4 = Etat("4",True)
etat5 = Etat("5",False)
etat6 = Etat("6",False)

autom = automate()

autom.ajoute_initial(etat0)
autom.ajoute_etat(etat1)
autom.ajoute_final(etat2)
autom.ajoute_etat(etat3)
autom.ajoute_final(etat4)
autom.ajoute_initial(etat5)
autom.ajoute_initial(etat6)

#autom.transition[etat3] = {}
#autom.transition[etat0] = {}
#autom.transition[etat1] = {}

autom.ajoute_transition(etat0,etat3,'a')
autom.ajoute_transition(etat0,etat1,'b')
autom.ajoute_transition(etat1,etat2,'c')
autom.ajoute_transition(etat3,etat4,'d')
autom.ajoute_transition(etat1,etat1,'e')
autom.ajoute_transition(etat3,etat5,'f')
autom.ajoute_transition(etat5,etat4,'g')
autom.ajoute_transition(etat5,etat6,'h')
autom.ajoute_transition(etat6,etat6,'i')
autom.ajoute_transition(etat6,etat2,'j')

application = QtGui.QApplication(sys.argv)

graphe = Graphe(autom,500)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()


sys.exit(application.exec_())

