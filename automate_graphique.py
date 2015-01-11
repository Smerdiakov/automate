#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import classe_etat
from classe_etat import *
from automate import automate
import sys
import os
from math import sin,cos,atan,pi


class Graphe(QtGui.QGraphicsScene):
  def __init__(self,autom):
    super(Graphe,self).__init__(0,0,400,400)

    self.automate = autom
    self.transition = autom.transition
    self.fleches = []

    self.cles_transition = []
    for cle in self.automate.transition.keys():
      self.cles_transition.append(cle)

    self.etats = self.automate.initial + self.cles_transition + self.automate.final
    self.nombre_etats = len(self.etats)
        
    self.taille = 400
    self.etats_par_dimension = int((self.nombre_etats)**.5) + 1

    self.configurer_etats()
    self.creer_fleches()


  def creer_fleches(self):
    self.fleches = []
    for etat_initial in self.transition.keys():
     for lettre in self.transition[etat_initial].keys():
       etat_final = self.transition[etat_initial][lettre][0]
       geometrie_droite = self.calculer_droite(etat_initial,etat_final)
       self.transition[etat_initial][lettre].append(geometrie_droite)
       dessin_transition = Transition(geometrie_droite,lettre)
       self.fleches.append(dessin_transition)
       self.addItem(dessin_transition)
 
  def calculer_droite(self,etat_initial,etat_final):
    geometrie = []
    if etat_final.centre_x == etat_initial.centre_x:
      inclination = pi/2.
    else:
      inclination = atan((etat_final.centre_y - etat_initial.centre_y)/ \
                             (etat_final.centre_x - etat_initial.centre_x))
    if etat_final.centre_x < etat_initial.centre_x:
      inclination = inclination + pi
    geometrie.append(etat_initial.centre_x + \
                     etat_initial.diametre/2 * cos(inclination)) #x_initial
    geometrie.append(etat_initial.centre_y + \
                     etat_initial.diametre/2 * sin(inclination)) #y_initial
    geometrie.append(etat_final.centre_x + \
                     etat_final.diametre/2 * cos(inclination + pi)) #x_final
    geometrie.append(etat_final.centre_y + \
                     etat_final.diametre/2 * sin(inclination + pi)) #y_final
    geometrie.append(inclination)
    return geometrie



  # configurer la taille et la position des etats et les placer sur l'automate
  def configurer_etats(self):
    self.diametre_etat = self.taille/8
    self.position_etat = self.taille/self.etats_par_dimension

    for etat in self.automate.initial:
      etat.est_final = False
    for etat in self.automate.transition.keys():
      etat.est_final = False
    for etat in self.automate.final:
      etat.est_final = True

    for etat in self.etats:
#      etat.diametre = self.diametre_etat
      etat.graphe.append(self)       
      
#    for etat in self.automate.initial:
#      etat.position_x = self.position_etat
#      etat.position_y = self.taille/2

    compteur_x = 1
    compteur_y = 1
#    for etat in self.automate.transition.keys():
#      etat.position_x = compteur_x * self.position_etat
#      etat.position_y = compteur_y * self.position_etat
#      compteur_y +=1
#      if compteur_y > self.etats_par_dimension:
#        compteur_x +=1
#        compteur_y = 1
 
#    for etat in self.automate.final:
#      etat.position_x = compteur_x * self.position_etat
#      etat.position_y = compteur_y * self.position_etat
#      compteur_y +=1
#      if compteur_y > self.etats_par_dimension:
#        compteur_x +=1
#        compteur_y = 1

 
    for etat in self.etats:
      self.addItem(etat)
      etat.construire_etat()


application = QtGui.QApplication(sys.argv)


coleur = (255,255,255)
etat0 = Etat("B",coleur,50,200,100,False)
etat1 = Etat("A",coleur,50,200,200,False)
etat2 = Etat("1",coleur,40,100,150,True)
etat3 = Etat("34",coleur,40,10,15,False)

autom = automate()

autom.initial.append(etat3)
autom.transition[etat3] = {}
autom.transition[etat0] = {}
autom.transition[etat1] = {}
autom.ajoute_transition(etat3,etat0,'a')
autom.ajoute_transition(etat0,etat1,'b')
autom.ajoute_transition(etat1,etat2,'c')
autom.final.append(etat2)



graphe = Graphe(autom)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()


sys.exit(application.exec_())


