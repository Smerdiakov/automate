#!/usr/bin/python3

######################################################
## Test pour la representaton graphique du automate ##
######################################################

from automate_graphique import *
from classe_etat_transition import *
from PyQt4 import QtGui
import unittest



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
    self.autom.ajoute_transition(self.etat3,self.etat5,'')
    self.autom.ajoute_transition(self.etat5,self.etat4,'g')
    self.autom.ajoute_transition(self.etat5,self.etat6,'h')
    self.autom.ajoute_transition(self.etat6,self.etat6,'i')
    self.autom.ajoute_transition(self.etat6,self.etat2,'')


 
 
    application = QtGui.QApplication(sys.argv)

    self.graphe = Graphe(self.autom,500)
    self.graphe.solution = (self.etat0,self.etat3,self.etat5,self.etat6,self.etat2)
    self.graphe.afficher_solution()  
    visualisation_graphe = QtGui.QGraphicsView(self.graphe)
    visualisation_graphe.show()

    sys.exit(application.exec_())


  def test_organiser_etats(self):
    ## verifier si tous les etats ont ete listes
    self.assertEqual(len(self.graphe.etats), \
                     self.autom.nombre_etat())

    ## verifier si les etats sont bien identifies comme finaux ou pas
    for etat in self.graphe.etats:
      self.assertEqual(etat.est_final,self.autom.est_final(etat))

  def test_identifier_precedents_successeurs(self):
    self.graphe.identifier_precedents_successeurs()
    ## verifier si tous les etats sont dans les deux dictionnaires
    self.assertEqual(len(self.graphe.precedents_etat), \
                     len(self.graphe.successeurs_etat))
    ## verifier si l'etat initial n'a pas de predecesseurs
    #### et l'etat final n'a pas de successeurs
    self.assertEqual(len(self.graphe.precedents_etat[self.etat0]),0) #etat_initial 
    self.assertEqual(len(self.graphe.successeurs_etat[self.etat2]),0) #etat final
    self.assertEqual(len(self.graphe.successeurs_etat[self.etat4]),0) #etat final

    ## verifier (x est precedent de y) <=> (y est successeur de x)
    for depart in self.graphe.precedents_etat.keys():
      for arrivee in self.graphe.precedents_etat[depart]:
        assert (depart in self.graphe.successeurs_etat[arrivee])

    for arrivee in self.graphe.successeurs_etat.keys():
      for depart in self.graphe.successeurs_etat[arrivee]:
        assert (arrivee in self.graphe.precedents_etat[depart])

  def test_placer_etats(self):
    coordonnees = []
    for etat in self.graphe.etats:
      coordonnees.append([etat.centre_x,etat.centre_y]) 
    ## verifier s'il y a deux etats dans la meme position
    for coord in coordonnees: 
      complementaire = coordonnees
      complementaire.remove(coord) #seuleument la premiere fois que l'element apparaitre
      self.assertNotIn(coord,complementaire)


if __name__=="__main__":
	print("\n")
	print(" ------------------------------------------")
	print("   debut du test sur la classe graphe :")
	print(" ------------------------------------------")
	print("\n")
	unittest.main()
