#!/usr/bin/python3

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
    self.fleches = []

    self.etats_intermediaires = []
    for etat in self.automate.transition.keys():
      if etat not in self.automate.initial:
        self.etats_intermediaires.append(etat)


    self.etats = self.automate.initial + self.etats_intermediaires + self.automate.final
        
    self.taille = taille
    self.etats_par_dimension = int((self.automate.nombre_etat())**.5) + 1

    self.placer_etats()
    self.placer_fleches()


  def placer_fleches(self):
    self.fleches = []
    for etat_initial in self.transition.keys():
     for lettre in self.transition[etat_initial].keys():
       etat_final = self.transition[etat_initial][lettre][0]
       dessin_transition = Transition(etat_initial,etat_final,lettre)
       self.fleches.append(dessin_transition)
       self.addItem(dessin_transition)


  def identifier_precedents_successeurs(self):
    preced = {}
    succes = {}
    for etat in self.etats:
      preced[etat] = []
      succes[etat] = []
    for depart in self.transition.keys():
      for lettre in self.transition[depart].keys():
        [arrivee] = self.automate.image(depart,lettre)
        preced[arrivee].append(depart)
        succes[depart].append(arrivee)
    return [preced,succes]


  
  # configurer la taille et la position des etats et les placer sur l'automate
  def placer_etats(self):

    [precedents_etat,successeurs_etat] = self.identifier_precedents_successeurs()

    #modifier les propriétés geométriques des états en fonction de tout l'automate
    # (espace disponible, nombre d'etats, relation entre les etats)
    self.diametre_etat = self.taille/8
    self.distance_etats = self.taille/4


    for etat in self.etats:
      etat.graphe.append(self)       
      etat.diametre = self.diametre_etat
      etat.actualiser_geometrie()
    
      
    for etat in self.automate.initial:
      etat.position_initial_x = self.distance_etats
      etat.position_initial_y = self.taille/2
      etat.actualiser_geometrie()
   

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
      etat.graphe.append(self)       
      self.addItem(etat)
      etat.construire_etat()




application = QtGui.QApplication(sys.argv)


coleur = (255,255,255)
etat0 = Etat("B",coleur,50,0,0,False)
etat1 = Etat("A",coleur,50,0,0,False)
etat2 = Etat("1",coleur,40,0,0,True)
etat3 = Etat("34",coleur,40,0,0,False)
etat4 = Etat("2",coleur,40,0,0,True)

autom = automate()

autom.initial.append(etat3)
autom.transition[etat3] = {}
autom.transition[etat0] = {}
autom.transition[etat1] = {}
autom.ajoute_transition(etat3,etat0,'a')
autom.ajoute_transition(etat0,etat1,'b')
autom.ajoute_transition(etat1,etat2,'c')
autom.ajoute_transition(etat0,etat4,'d')
autom.final.append(etat2)
autom.final.append(etat4)


graphe = Graphe(autom,400)
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()


sys.exit(application.exec_())


