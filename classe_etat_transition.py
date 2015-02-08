#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import sys
import os
from math import pi,sin,cos,atan

def main():
  print("main etat")

if __name__ == '__main__':
  main()


class Transition(QtGui.QGraphicsItemGroup):
  def __init__(self,etat_initial,etat_final,lettre):
    super(Transition,self).__init__(None)

    self.lettre = lettre

    self.depart = etat_initial
    self.arrivee = etat_final

    self.dessiner_fleche()

  def dessiner_fleche(self):

     self.style_ligne = QtGui.QPen()
     self.style_ligne.setWidth(2)
     self.font  = QtGui.QFont("Arial",14)

     if self.lettre == "":
       self.style_ligne.setStyle(QtCore.Qt.DashLine)
       self.lettre = "ε"
     self.texte_fleche = QtGui.QGraphicsSimpleTextItem(self.lettre)

     if self.depart == self.arrivee:
        self.dessiner_fleche_circulaire(self.depart)
     else:
        geometrie_droite = self.calculer_droite(self.depart,self.arrivee) 
        self.dessiner_fleche_droite(geometrie_droite)

     self.fleche.setPen(self.style_ligne)
     self.tete1.setPen(self.style_ligne)
     self.tete2.setPen(self.style_ligne)
     self.texte_fleche.setFont(self.font)     

     self.addToGroup(self.fleche)
     self.addToGroup(self.tete1)
     self.addToGroup(self.tete2)
     self.addToGroup(self.texte_fleche)

  def dessiner_fleche_circulaire(self,etat):
      ## corps de la fleche 
      self.fleche  = QtGui.QGraphicsEllipseItem(etat.position_externe_x,\
                                                etat.position_externe_y - etat.diametre/2.,\
                                                etat.diametre,etat.diametre) 
      self.fleche.setStartAngle(-16*30) 
      self.fleche.setSpanAngle(16*240)
    
      ## tete de la fleche
      tete_initial_x = etat.centre_x + etat.diametre/2.*cos(pi/6.)
      tete_initial_y = etat.centre_y - etat.diametre/2.*sin(pi/6.)
      inclination = -pi/3
      self.dessiner_tete_fleche(tete_initial_x,tete_initial_y,inclination)

      # texte de la fleche
      position_texte_x = etat.centre_x
      position_texte_y = etat.centre_y - .9*etat.diametre
      self.texte_fleche.setPos(position_texte_x,position_texte_y)

  def dessiner_fleche_droite(self,geometrie_droite):    
      ## corps de la fleche 
      self.fleche  = QtGui.QGraphicsLineItem(geometrie_droite[0],geometrie_droite[1],\
                                           geometrie_droite[2],geometrie_droite[3])

      # tete de la fleche
      inclination = geometrie_droite[4]+pi
      tete_initial_x = geometrie_droite[2]
      tete_initial_y = geometrie_droite[3]
      self.dessiner_tete_fleche(tete_initial_x,tete_initial_y,inclination)

      # texte de la fleche
      position_texte_x = 0.5*(geometrie_droite[0] + geometrie_droite[2]) +\
                         25*cos(inclination+pi/2)
      position_texte_y =  0.5*(geometrie_droite[1] + geometrie_droite[3]) +\
                         (25 - 15*(int(cos(inclination) > 0))) *sin(inclination+pi/2)
      self.texte_fleche.setPos(position_texte_x,position_texte_y)


  def dessiner_tete_fleche(self,tete_initial_x,tete_initial_y,inclination):

      longueur_tete = 15
      ouverture_tete = pi/6

      tete_final_x_1 = tete_initial_x +\
                       longueur_tete*cos(inclination+ouverture_tete)
      tete_final_y_1 = tete_initial_y +\
                       longueur_tete*sin(inclination+ouverture_tete)
      tete_final_x_2 = tete_initial_x +\
                       longueur_tete*cos(inclination-ouverture_tete)
      tete_final_y_2 = tete_initial_y +\
                       longueur_tete*sin(inclination-ouverture_tete) 
 
      self.tete1  = QtGui.QGraphicsLineItem(tete_initial_x,tete_initial_y,\
                                            tete_final_x_1,tete_final_y_1)
      self.tete2  = QtGui.QGraphicsLineItem(tete_initial_x,tete_initial_y,\
                                            tete_final_x_2,tete_final_y_2)

  def calculer_droite(self,etat_initial,etat_final):
    
    geometrie = []
 
    if etat_initial != 0: # il ne s'agit pas de la fleche d'entree de l'automate
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
 
    else: 
      inclination = 0
      geometrie.append(etat_final.centre_x - 3*etat_final.diametre/2)
      geometrie.append(etat_final.centre_y)
      geometrie.append(etat_final.centre_x - etat_final.diametre/2)
      geometrie.append(etat_final.centre_y) #y_final
      geometrie.append(inclination)

    return geometrie


class Etat(QtGui.QGraphicsItemGroup):
  def __init__(self,etiq,final):
    super(Etat,self).__init__(None)
  
    self.etiquette = etiq
    self.coleur = QtGui.QBrush(QtCore.Qt.gray)
    self.diametre = 10
    self.position_initial_x = 0
    self.position_initial_y = 0
    self.position_x = 0
    self.position_y = 0
    self.est_final = final
    self.graphe = [] #identifier l'instance de Graphe que contient l'etat 
    self.niveau_graphe = 1 #profondeur de l'etat dans le graphe 

  def construire_etat(self):
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
    self.setCursor(QtCore.Qt.OpenHandCursor)
    self.definir_configurations_graphiques()
    self.dessiner_cercle()

  #### ITERACTIONS AVEC LA SOURIS

## faire bouger l'etat
  def mousePressEvent(self, e):
    e.accept()
    self.setCursor(QtCore.Qt.ClosedHandCursor)
    graphe = self.graphe[0]
    for fleche in graphe.fleches:
      graphe.removeItem(fleche)

## placer l'etat
  def mouseReleaseEvent(self, e): 
    e.accept()
    self.setCursor(QtCore.Qt.OpenHandCursor)
    self.actualiser_geometrie()
    self.graphe[0].placer_fleches()

  ### DESSINER FIGURE   
  def definir_configurations_graphiques(self):
    #Proprietes des cercles
    self.centre_x = self.position_x
    self.centre_y = self.position_y
## cercle_exterieur
    self.position_externe_x = self.centre_x - self.diametre/2.  #coin gauche supérieur
    self.position_externe_y = self.centre_y - self.diametre/2.
## cercle_interieur
    self.position_interne_x = self.centre_x - .9*self.diametre/2.
    self.position_interne_y = self.centre_y - .9*self.diametre/2.

    #proprietes des etiquettes
    taille_font = .5*self.diametre
    self.font  = QtGui.QFont("Arial",-1)
    self.font.setPixelSize(taille_font)
    taille_texte = len(self.etiquette)*taille_font
    self.position_texte_x = self.position_externe_x + self.diametre/2-taille_texte/4
    self.position_texte_y = self.position_externe_y + self.diametre/2-taille_font/2


## identifier la nouvelle position du etat et actualiser ses variables
  def actualiser_geometrie(self):
    self.position_x = self.position_initial_x + self.x()
    self.position_y = self.position_initial_y + self.y()
    self.definir_configurations_graphiques()

## Pour l'affichage de la solution
  def actualiser_coleur(self):
    self.cercle_ext.setBrush(self.coleur)
    if self.est_final:
      self.cercle_int.setBrush(self.coleur)

##
  def dessiner_cercle(self):
    self.cercle_ext = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
                            self.position_externe_x,self.position_externe_y,\
                            self.diametre,self.diametre))
    self.cercle_ext.setBrush(self.coleur)
    self.cercle_ext.setOpacity(1.)
    self.cercle_ext.setAcceptHoverEvents(True)
    self.addToGroup(self.cercle_ext)
  
    ## etat final --> deux cercles
    if self.est_final: 
      self.cercle_int = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
                              self.position_interne_x,self.position_interne_y,\
                              .9*self.diametre,.9*self.diametre))
      self.cercle_int.setBrush(self.coleur)
      self.cercle_int.setOpacity(1.)
      self.addToGroup(self.cercle_int)

    self.texte = QtGui.QGraphicsSimpleTextItem(self.etiquette)
    self.texte.setPos(self.position_texte_x,self.position_texte_y)
    self.texte.setFont(self.font)
    self.texte.setAcceptHoverEvents(False)
    self.addToGroup(self.texte)



