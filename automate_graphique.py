#!/usr/bin/python3


##########################################
## Representation graphique du automate ##
##########################################


#### La classe Graphe prend un automate comme parametre et:
## Affiche les instances de classe etat (qui sont deja contenues dans l'automate)
## Cree des instances de la classe Transition et les affiche

from PyQt4 import QtGui,QtCore
import classe_etat_transition
from classe_etat_transition import *
from automate import automate
import sys
import os


class Graphe(QtGui.QGraphicsScene):
  def __init__(self,autom,taille):
    super(Graphe,self).__init__(0,0,taille,taille)

    self.automate = autom
    self.transition = autom.transition
 
    self.organiser_etats()

    self.fleches = []
    self.taille = taille
    self.placer_etats()
    self.placer_fleches()


######### Fonctions de traitement des etats

## Organiser les listes d'etats
  def organiser_etats(self):
    self.etats_intermediaires = []
    for etat in self.automate.transition.keys():
      if etat not in self.automate.initial:
        self.etats_intermediaires.append(etat)

    self.etats = self.automate.initial + self.etats_intermediaires + self.automate.final

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

    [precedents_etat,successeurs_etat] = self.identifier_precedents_successeurs()

    #modifier les propriétés geométriques des états en fonction de tout l'automate
    # (espace disponible, nombre d'etats, relation entre les etats)
    self.diametre_etat = self.taille/8
    self.distance_etats = self.taille/4

     
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
               for precedent in precedents_etat[etat]:
                   if precedent.position_initial_x == 0:
                       precedents_places = False
                       break
               if precedents_places:
                   for precedent in precedents_etat[etat]:
                       assert(precedent in successeurs_etat.keys())
                       etat.position_initial_x = max([etat.position_initial_x,
                                                     precedent.position_initial_x + self.distance_etats])
                       nombre_etats_niveau = len(successeurs_etat[precedent]) 
                       if nombre_etats_niveau == 1:
                          etat.position_initial_y = precedent.position_initial_y
                       else:
                          etat.position_initial_y = precedent.position_initial_y + \
                                                    self.distance_etats* \
                                                    (-1)**(successeurs_etat[precedent].index(etat)) * \
                                                    int(nombre_etats_niveau/2)
                   etat.actualiser_geometrie() 
               else:
                   placement_fini = False
   

    #verifier si l'etat est correctment identifie comme final ou pas 
    for etat in self.automate.initial:
      etat.est_final = False
    for etat in self.automate.transition.keys():
      etat.est_final = False
    for etat in self.automate.final:
      etat.est_final = True

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




############# PREMIER TEST
####### A ORGANISER SUR  UN FICHIER TEST 
####### Pour tester, executer ./automate_graphique.py

application = QtGui.QApplication(sys.argv)

coleur = (255,255,255)
etat0 = Etat("B",coleur,50,0,0,False)
etat1 = Etat("A",coleur,50,0,0,False)
etat2 = Etat("1",coleur,40,0,0,True)
etat3 = Etat("34",coleur,40,0,0,False)
etat4 = Etat("2",coleur,40,0,0,True)

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
autom.ajoute_transition(etat1,etat1,'e')


graphe = Graphe(autom,400)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()


sys.exit(application.exec_())


