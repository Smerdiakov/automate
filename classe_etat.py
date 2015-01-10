#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import sys
import os


if __name__ == '__main__':
  main()


class Transition(QtGui.QGraphicsItemGroup):
  def __init__(self,geometrie_droite):
    super(Transition,self).__init__(None)

    
    self.fleche  = QtGui.QGraphicsLineItem(geometrie_droite[0],\
                                           geometrie_droite[1],\
                                           geometrie_droite[2],\
                                           geometrie_droite[3])
    self.addToGroup(self.fleche)


class Etat(QtGui.QGraphicsItemGroup):
  def __init__(self,etiq,col,diam,pos_x,pos_y,final):
    super(Etat,self).__init__(None)
  
    self.etiquette = etiq
    self.coleur = QtGui.QColor(col[0],col[1],col[2])
    self.diametre = diam
    self.position_x = pos_x
    self.position_y = pos_y
    self.est_final = final


  def construire_etat(self):
    self.dessiner_cercle   
 
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
  
    self.setCursor(QtCore.Qt.OpenHandCursor)
 
    self.definir_configurations_graphiques()
    self.dessiner_cercle()

  #### ITERACTIONS AVEC LA SOURIS
  def mousePressEvent(self, e):
    e.accept()
    self.setCursor(QtCore.Qt.ClosedHandCursor)
    print(super(Etat,self))   
 
  def mouseReleaseEvent(self, e): 
    e.accept()
    self.setCursor(QtCore.Qt.OpenHandCursor)


  ### DESSINER FIGURE   
  def definir_configurations_graphiques(self):
    #Propietes des cercles
    self.centre_x = self.position_x
    self.centre_y = self.position_y
    self.position_externe_x = self.centre_x - self.diametre/2.
    self.position_externe_y = self.centre_y - self.diametre/2.
    self.position_interne_x = self.centre_x - .9*self.diametre/2.
    self.position_interne_y = self.centre_y - .9*self.diametre/2.

    #propietes des etiquettes
    taille_font = .5*self.diametre
    self.font  = QtGui.QFont("Arial",-1)
    self.font.setPixelSize(taille_font)
    taille_texte = len(self.etiquette)*taille_font
    self.position_texte_x = self.position_externe_x + self.diametre/2-taille_texte/4
    self.position_texte_y = self.position_externe_y + self.diametre/2-taille_font/2
 
  def dessiner_cercle(self):
    self.cercle_ext = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
       self.position_externe_x,self.position_externe_y,\
       self.diametre,self.diametre))
    self.addToGroup(self.cercle_ext)
    self.cercle_ext.setBrush(QtCore.Qt.gray)
    self.cercle_ext.setOpacity(0.3)
    self.cercle_ext.setAcceptHoverEvents(True)

    if self.est_final:
      self.cercle_int = QtGui.QGraphicsEllipseItem(QtCore.QRectF(\
        self.position_interne_x,self.position_interne_y,\
        .9*self.diametre,.9*self.diametre))
      self.addToGroup(self.cercle_int)
      self.cercle_int.setBrush(QtCore.Qt.gray)
      self.cercle_int.setOpacity(0.2)

    self.texte = QtGui.QGraphicsSimpleTextItem(self.etiquette)
    self.texte.setPos(self.position_texte_x,self.position_texte_y)
    self.texte.setFont(self.font)
    self.addToGroup(self.texte)
    self.texte.setAcceptHoverEvents(False)
   


def main():
  print("main")

