#!/usr/bin/python3

from PyQt4 import QtGui,QtCore
import sys
import os


def main():
  print("main")


if __name__ == '__main__': # pour eviter l'execution de la machine quand on lance l'éditeur
   main()



class Etat(QtGui.QGraphicsItemGroup):
  def __init__(self,etiq,col,diam,pos_x,pos_y,final):
    super(Etat,self).__init__(None)
  
    self.etiquette = etiq
    self.coleur = QtGui.QColor(col[0],col[1],col[2])
    self.diametre = diam
    self.position_x = pos_x
    self.position_y = pos_y
    self.est_final = final
    self.dessiner_cercle   

 
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
  
    self.setCursor(QtCore.Qt.OpenHandCursor)
 
    self.definir_configurations_graphiques()
    self.dessiner_cercle()
    self.dessiner_button_taille()

  #### ITERACTIONS AVEC LA SOURIS
  def hoverEnterEvent(self, e): 
    e.accept()
    self.button_augmenter.show()
    self.button_reduire.show()
   
  def hoverLeaveEvent(self, e):
    e.accept()
    self.button_augmenter.hide()
    self.button_reduire.hide()
 
  def mousePressEvent(self, e):
    if self.button_augmenter.isUnderMouse(): #augmenter taille
      self.setCursor(QtCore.Qt.OpenHandCursor)
      e.accept()
      self.changer_taille(1)
    if self.button_reduire.isUnderMouse(): #reduire taille
      self.setCursor(QtCore.Qt.OpenHandCursor)
      e.accept()
      self.changer_taille(-1)
    else: #deplacer
      e.accept()
      self.setCursor(QtCore.Qt.ClosedHandCursor)

  def mouseReleaseEvent(self, e): 
    e.accept()
    self.setCursor(QtCore.Qt.OpenHandCursor)


  ### DESSINER FIGURE   
  def definir_configurations_graphiques(self):
    self.font  = QtGui.QFont("Arial",.5*self.diametre)
    self.centre_x = self.position_x
    self.centre_y = self.position_y
    self.position_externe_x = self.centre_x - self.diametre/2.
    self.position_externe_y = self.centre_y - self.diametre/2.
    self.position_interne_x = self.centre_x - .9*self.diametre/2.
    self.position_interne_y = self.centre_y - .9*self.diametre/2.
    self.position_texte_x = self.centre_x - self.diametre/4
    self.position_texte_y = self.centre_y - self.diametre/2.5


  def dessiner_area_etat(self): #rectangle qui contient le cercle
    self.area_etat = QtGui.QGraphicsRectItem(QtCore.QRectF(\
       self.position_externe_x-15,self.position_externe_y-15,\
       self.diametre+30,self.diametre+30))
    self.addToGroup(self.area_etat)
    self.area_etat.setBrush(QtCore.Qt.white)
    self.area_etat.setOpacity(.01)
    self.area_etat.setAcceptHoverEvents(True)
   
  def dessiner_cercle(self):
    self.point_centre = QtGui.QGraphicsRectItem(self.centre_x,self.centre_y,0.0001,0.0001)   
    self.addToGroup(self.point_centre)

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

    self.texte = QtGui.QGraphicsTextItem(self.etiquette)
    self.texte.setPos(self.position_texte_x,self.position_texte_y)
    self.texte.setFont(self.font)
    self.addToGroup(self.texte)
    self.texte.setAcceptHoverEvents(False)


  def dessiner_button_taille(self):
    self.button_augmenter = QtGui.QGraphicsPixmapItem(\
        QtGui.QPixmap(os.getcwd() + "/images/arrow_augmenter.jpg"))
    self.button_augmenter.setPos(self.centre_x+15,self.centre_y-40)

    self.button_reduire = QtGui.QGraphicsPixmapItem(\
        QtGui.QPixmap(os.getcwd() + "/images/arrow_augmenter.jpg"))
    self.button_reduire.setPos(self.centre_x-20,self.centre_y+25)
    self.button_reduire.setRotation(180)

    buttons = [self.button_augmenter, self.button_reduire]

    for button in buttons:
      button.setScale(.05)
      self.addToGroup(button)
      button.hide()
      button.setCursor(QtCore.Qt.SizeBDiagCursor)
    
  ### MODIFIER FIGURE
  def changer_taille(self,direction):
    self.scale(1.05**direction,1.05**direction)
    self.diametre = 1.05**direction*self.diametre
    

class Graphe(QtGui.QGraphicsScene):
  def __init__(self):
    super(Graphe,self).__init__(0,0,500,400)

    coleur = (255,255,255)
    self.addItem(Etat("A",coleur,100,200,200,True))
    self.addItem(Etat("1",coleur,80,100,150,False))

    print ("sss")

application = QtGui.QApplication(sys.argv)
graphe = Graphe()
visualisation_graphe = QtGui.QGraphicsView(graphe)
visualisation_graphe.show()
sys.exit(application.exec_())
