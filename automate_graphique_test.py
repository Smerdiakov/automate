#!/usr/bin/python3

######################################################
## Test pour la representaton graphique du automate ##
######################################################

from automate_graphique import *
from classe_etat_transition import *
from PyQt4 import QtGui
import unittest



application = QtGui.QApplication(sys.argv)

graphe = Graphe(autom,500)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()


sys.exit(application.exec_())


class test_automate_graphique (unittest.TestCase):

############  Creation d'un automate
  def setUp(self):
    self.coleur = (255,255,255)
    self.etat0 = Etat("0",False)
    self.etat1 = Etat("1",False)
    self.etat2 = Etat("2",True)
    self.etat3 = Etat("3",False)
    self.etat4 = Etat("4",True)
    self.etat5 = Etat("5",False)
    self.etat6 = Etat("6",False)

    self.autom = automate()

    self.autom.ajoute_initial(self.etat0)
    self.autom.ajoute_etat(self.etat1)
    self.autom.ajoute_final(self.etat2)
    self.autom.ajoute_etat(self.etat3)
    self.autom.ajoute_final(self.etat4)
    self.autom.ajoute_etat(self.etat5)
    self.autom.ajoute_etat(self.etat6)


    self.autom.ajoute_transition(self.etat0,self.etat3,'a')
    self.autom.ajoute_transition(self.etat0,self.etat1,'b')
    self.autom.ajoute_transition(self.etat1,self.etat2,'c')
    self.autom.ajoute_transition(self.etat3,self.etat4,'d')
    self.autom.ajoute_transition(self.etat1,self.etat1,'e')
    self.autom.ajoute_transition(self.etat3,self.etat5,'f')
    self.autom.ajoute_transition(self.etat5,self.etat4,'g')
    self.autom.ajoute_transition(self.etat5,self.etat6,'h')
    self.autom.ajoute_transition(self.etat6,self.etat6,'i')
    self.autom.ajoute_transition(self.etat6,self.etat2,'j')

  def organiser_etats_test(self):
    self.organiser_etats()
    ## verifier si tous les etats ont ete listes
    self.assertEqual(len(self.etats), \
                     len(self.autom.transition) + len(self.autom.final))

  def identifier_precedents_successeurs(self):
    self.identifier_precedents_successeurs()
    ## verifier si tous les etats sont dans les deux dictionnaires
    self.assertEqual(len(self.autom.precedents_etat), \
                     len(self.autom.successeurs_etat)
    ## verifier si l'etat initial n'a pas de predecesseurs
    #### et l'etat final n'a pas de successeurs
    self.assert(len(self.autom.precedents_etat[etat0],0)) #etat initial
    self.assert(len(self.autom.successeurs_etat[etat2],0)) #etat final
    self.assert(len(self.autom.successeurs_etat[etat4],0)) #etat final

    ## verifier (x est precedent de y) <=> (y est successeur de x)
    for depart in self.autom.precedents_etat.keys():
      for arrivee in self.autom.precedents_etat[depart]:
        assert (depart in self.autom.successeurs_etat[arrivee])

    for arrivee in self.autom.successeurs_etat.keys():
      for depart in self.autom.successeurs_etat[arrivee]:
        assert (arrivee in self.autom.precedents_etat[depart])

  def placer_etats_test(self):
    coordonnes = []
    for etat in self.autom.etats:
      coordonnes.append([etat.centre_x,etat.centre_y]) 
    ## verifier s'il y a deux etats dans la meme position
    for coord in self.autom.etats:
      complementaire = coordonnes
      complementaire.remove(coord) #seuleument la premiere fois que l'element apparaitre
      self.assertNotIn(coord,complementaire)
   
