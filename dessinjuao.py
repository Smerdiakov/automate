#!/usr/bin/python3


##########################################
## Representation graphique du automate ##
##########################################


#### La classe Graphe prend un automate comme parametre et:
## Affiche les instances de classe etat (qui sont deja contenues dans l'automate)
## Cree des instances de la classe Transition et les affiche

from PyQt4 import QtGui,QtCore
import classeetattransition
from classeetattransition import *
from automates import automate
from executions import *
import sys
import os
import time

class Graphe(QtGui.QGraphicsScene):
  def __init__(self,autom,taille):
    super(Graphe,self).__init__(0,0,taille,taille)

    self.automate = autom#ensemble
    self.transition = autom.transition#liste des transitions
 
    self.organiser_etats()

    self.fleches = []#liste de objet flèche
    self.taille = taille#la taille de la fenetre 
    self.placer_etats()#etats avec coordonnées
    self.placer_fleches()#placer les flèches

    self.solution = [] #a definir

######### Fonctions de traitement des etats

## Organiser les listes d'etats
  def organiser_etats(self):
    self.etats = self.automate.liste_etats()
    self.etats_intermediaires = self.automate.liste_etats_intermediaires()


## Faire des dictionaires avec les precedents et les successeurs de chaque etat        
  def identifier_precedents_successeurs(self):
    preced = {}
    succes = {}
    for etat in self.etats:
      preced[etat] = []
      succes[etat] = []
    for depart in self.transition.keys():
      for lettre in self.transition[depart].keys():
        [arrivee] = self.automate.image(depart,lettre)
        if arrivee != depart:
          preced[arrivee].append(depart)
          succes[depart].append(arrivee)
    return [preced,succes]


## Configurer la taille et la position des etats et les placer sur l'automate
  def placer_etats(self):

    [self.precedents_etat,self.successeurs_etat] = self.identifier_precedents_successeurs()

    #modifier les propriétés geométriques des états en fonction de tout l'automate
    # (espace disponible, nombre d'etats, relation entre les etats)
    self.diametre_etat = self.taille/8
    self.distance_etats = self.taille/8
  
    for etat in self.automate.initial:
      etat.position_initial_x = self.distance_etats
      etat.position_initial_y = self.taille/2
      etat.actualiser_geometrie()

    ## Boucle de modification de la position (x,y) de tous les etats
    # Un etat peut etre place ssi tous ses precedents on deja ete places
    placement_fini = False
    while not(placement_fini):
        placement_fini = True
        for etat in self.etats_intermediaires + self.automate.final:
            if etat.position_initial_x == 0: 
               precedents_places = True
               for precedent in self.precedents_etat[etat]:
                   if precedent.position_initial_x == 0:
                       precedents_places = False
                       break
               if precedents_places:
                   for precedent in self.precedents_etat[etat]:
                       # L'etat est au moins un niveau au dessus de tous ses precesseurs
                       etat.niveau_graphe = max(etat.niveau_graphe,precedent.niveau_graphe+1)
                       assert(precedent in self.successeurs_etat.keys())
                       etat.position_initial_x = max([etat.position_initial_x,
                                                     precedent.position_initial_x + \
                                                     self.distance_etats + \
                                                     (1+(-1)**etat.niveau_graphe)*\
                                                     0.5*self.diametre_etat*(etat.niveau_graphe-1)])
                       #etat.position_initial_x=etat.position_initial_x+200 
                                                     #eviter des intersections entre fleches etats
                       nombre_etats_niveau = len(self.successeurs_etat[precedent]) 
                       if nombre_etats_niveau == 1:
                          etat.position_initial_y = precedent.position_initial_y
                       else:
                          etat.position_initial_y = precedent.position_initial_y + \
                                                    self.distance_etats* \
                                                    (-1)**(self.successeurs_etat[precedent].index(etat))*\
                                                    (int(nombre_etats_niveau/2)) +\
                                                    (0+(-1)**etat.niveau_graphe)*\
                                                    0.5*self.diametre_etat*(etat.niveau_graphe-1)
                          #etat.position_initial_y=etat.position_initial_y+200
                                                    #eviter des intersections entre fleches etats
                   etat.actualiser_geometrie() 
               else:
                   placement_fini = False
   
    for etat in self.etats:
      etat.diametre = self.diametre_etat
      etat.graphe.append(self) # L'etat connait l'automat ou il se trouve
      self.addItem(etat)
      etat.construire_etat()


################# Fonctions de traitement des Transitions

## Creer des instances de la classe Transition et les afficher
  def placer_fleches(self):
    self.fleches = []
    for depart in self.transition.keys():
     for lettre in self.transition[depart].keys():
       [arrivee] = self.automate.image(depart,lettre)
       dessin_transition = Transition(depart,arrivee,lettre)
       self.fleches.append(dessin_transition)
       self.addItem(dessin_transition)


################ Fonctions pour afficher la solution
##### animations, etc.
##### apres l'execution du methode 'execution' de execute.py
  def afficher_solution(self):
   temps = QtCore.QTime()
   temps.start()
   indice_etat = 0
   button = QtGui.QPushButton("Prochain etat")
   button.show()
   button.raise_()

   while indice_etat <  len(self.solution):
       etat = self.solution[indice_etat]
       print(temps.elapsed())
       print(indice_etat)
       etat.coleur  = QtGui.QBrush(QtCore.Qt.cyan)
       button.clicked.connect(etat.actualiser_coleur)
       indice_etat += 1
def main():
############# PREMIER TEST
####### A ORGANISER SUR  UN FICHIER TEST 
####### Pour tester, executer ./automate_graphique.py
  print("main automate")
  application = QtGui.QApplication(sys.argv)

  coleur = (255,255,255)
  etat0 = Etat("B",False)
  etat1 = Etat("A",False)
  etat2 = Etat("1",True)
  etat3 = Etat("34",False)
  etat4 = Etat("2",True)

  autom = automate()

  autom.ajoute_etat(etat0)
  autom.ajoute_etat(etat1)
  autom.ajoute_final(etat2)
  autom.ajoute_initial(etat3)
  autom.ajoute_final(etat4)
  autom.transition[etat3] = {}
  autom.transition[etat0] = {}
  autom.transition[etat1] = {}
  autom.ajoute_transition(etat3,etat0,'a')
  autom.ajoute_transition(etat0,etat1,'b')
  autom.ajoute_transition(etat1,etat2,'c')
  autom.ajoute_transition(etat0,etat4,'d')
  autom.ajoute_transition(etat1,etat1,'')


  graphe = Graphe(autom,400)
  visualisation_graphe = QtGui.QGraphicsView(graphe)
  visualisation_graphe.show()
  #visualisation_graphe.setStyleSheet("QGraphicsView{background-color:black}")



#  executer = execution(autom)
#  self.solut = executer.solution("abcd")
#  print(self.solut)

  solut = (graphe.etats[0],graphe.etats[1])
  graphe.solution = solut

  button = QtGui.QPushButton("Afficher la solution")
  button.show()
  button.raise_()
  button.clicked.connect(graphe.afficher_solution)

  sys.exit(application.exec_())



if __name__ == '__main__':
  main()

