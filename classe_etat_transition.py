#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import sys
import os
from math import pi,sin,cos,atan

if __name__ == '__main__':
  main()


class Transition(QtGui.QGraphicsItemGroup):
  def __init__(self,etat_initial,etat_final,lettre):
    super(Transition,self).__init__(None)

    style_ligne = QtGui.QPen()
    style_ligne.setWidth(2)
  

    geometrie_droite = self.calculer_droite(etat_initial,etat_final) 


    # corps de la fleche 
    self.fleche  = QtGui.QGraphicsLineItem(geometrie_droite[0],geometrie_droite[1],\
                                           geometrie_droite[2],geometrie_droite[3])

    # tete de la fleche
    inclination = geometrie_droite[4]+pi
    longueur_tete = 15
    ouverture_tete = pi/6

    tete_initial_x = geometrie_droite[2]
    tete_initial_y = geometrie_droite[3]
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

  
    # texte de la fleche
    moyenne_x = 0.5*(geometrie_droite[0] + geometrie_droite[2])
    moyenne_y = 0.5*(geometrie_droite[1] + geometrie_droite[3])
    position_texte_x = moyenne_x + 15*cos(inclination+pi/2)
    position_texte_y = moyenne_y + 15*sin(inclination+pi/2)
    self.texte_fleche = QtGui.QGraphicsSimpleTextItem(lettre)
    self.texte_fleche.setPos(position_texte_x,position_texte_y)


    self.fleche.setPen(style_ligne)
    self.tete1.setPen(style_ligne)
    self.tete2.setPen(style_ligne)

    self.addToGroup(self.fleche)
    self.addToGroup(self.tete1)
    self.addToGroup(self.tete2)
    self.addToGroup(self.texte_fleche)


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



class Etat(QtGui.QGraphicsItemGroup):
  def __init__(self,etiq,col,diam,pos_x,pos_y,final):
    super(Etat,self).__init__(None)
  
    self.etiquette = etiq
    self.coleur = QtGui.QColor(col[0],col[1],col[2])
    self.diametre = diam
    self.position_initial_x = pos_x
    self.position_initial_y = pos_y
    self.position_x = pos_x
    self.position_y = pos_y
    self.est_final = final
    self.graphe = [] #identifier l'instance de Graphe que contient l'etat 
 
  def construire_etat(self):
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
    self.setCursor(QtCore.Qt.OpenHandCursor)
    self.definir_configurations_graphiques()
    self.dessiner_cercle()

  #### ITERACTIONS AVEC LA SOURIS
  def mousePressEvent(self, e):
    e.accept()
    self.setCursor(QtCore.Qt.ClosedHandCursor)
    graphe = self.graphe[0]
    for fleche in graphe.fleches:
      graphe.removeItem(fleche)

  def mouseReleaseEvent(self, e): 
    e.accept()
    self.setCursor(QtCore.Qt.OpenHandCursor)
    self.actualiser_geometrie()
    self.graphe[0].creer_fleches()


  ### DESSINER FIGURE   
  def definir_configurations_graphiques(self):
    #Proprietes des cercles
    self.centre_x = self.position_x
    self.centre_y = self.position_y
    self.position_externe_x = self.centre_x - self.diametre/2.
    self.position_externe_y = self.centre_y - self.diametre/2.
    self.position_interne_x = self.centre_x - .9*self.diametre/2.
    self.position_interne_y = self.centre_y - .9*self.diametre/2.

    #proprietes des etiquettes
    taille_font = .5*self.diametre
    self.font  = QtGui.QFont("Arial",-1)
    self.font.setPixelSize(taille_font)
    taille_texte = len(self.etiquette)*taille_font
    self.position_texte_x = self.position_externe_x + self.diametre/2-taille_texte/4
    self.position_texte_y = self.position_externe_y + self.diametre/2-taille_font/2


  def actualiser_geometrie(self):
    self.position_x = self.position_initial_x + self.x()
    self.position_y = self.position_initial_y + self.y()
    self.definir_configurations_graphiques()
 
  def dessiner_cercle(self):
    self.cercle_ext = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
                            self.position_externe_x,self.position_externe_y,\
                            self.diametre,self.diametre))
    self.cercle_ext.setBrush(QtCore.Qt.gray)
    self.cercle_ext.setOpacity(0.3)
    self.cercle_ext.setAcceptHoverEvents(True)
    self.addToGroup(self.cercle_ext)

    if self.est_final:
      self.cercle_int = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
                              self.position_interne_x,self.position_interne_y,\
                              .9*self.diametre,.9*self.diametre))
      self.cercle_int.setBrush(QtCore.Qt.gray)
      self.cercle_int.setOpacity(0.2)
      self.addToGroup(self.cercle_int)

    self.texte = QtGui.QGraphicsSimpleTextItem(self.etiquette)
    self.texte.setPos(self.position_texte_x,self.position_texte_y)
    self.texte.setFont(self.font)
    self.texte.setAcceptHoverEvents(False)
    self.addToGroup(self.texte)

def main():
  print("main")

