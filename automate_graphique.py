#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import classe_etat
from automate import automate
import sys
import os

class Graphe(QtGui.QGraphicsScenene):
  def __init__(self,autom):
    super(Graphe,self).__init__(0,0,400,400)

    print ("zzz")
    self.automate = autom
    self.etats = self.automate.initial + self.automate.transition + self.automate.final
    self.nombre_etats = len(self.etats)
        
    self.taille = 400
    self.etats_par_dimension = int((self.nombre_etats)**.5) + 1

  # configurer la taille et la position des etats et les placer sur l'automate
  def configurer_etats(self):
    self.diametre_etat = self.taille/8
    self.position_etat = self.taille/self.etats_par_dimension

    for etat in self.automate.initial + self.automate.transition:
      etat.est_final = False
    for etat in self.automate.final:
      etat.est_final = True

    for etat in self.etats:
      etat.diametre = self.diametre_etat
      
    for etat in self.automate.initial:
      etat.position_x = self.position_etat
      etat.position_y = self.taille/2

    compteur_x = 1
    compteur_y = 1
    for etat in self.automate.transition + self.automate.final:
      etat.position_x = compteur_x * self.position_etat
      etat.position_y = compteur_y * self.position_etat
      compteur_y +=1
      if compteur_y > self.etats_par_dimension:
        compteur_x +=1
        compteur_y = 1
  
    for etat in self.etats:
      self.addItem(etat)


coleur = (255,255,255)
etat0 = Etat("B",coleur,100,200,200,True)
etat1 = Etat("A",coleur,100,200,200,True)
etat2 = Etat("1",coleur,80,100,150,False)

autom = automate()
autom.transition.append(etat0)
autom.transition.append(etat1)
autom.final.append(etat2)

print(autom)

application = QtGui.QApplication(sys.argv)
graphe = Graphe(autom)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()
sys.exit(application.exec_())


