import sys
import os
import time
import auto_ludo
from PyQt4 import QtGui,QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Bouton(QtGui.QPushButton):
    def _init_(self,fenetremere,title):
        self.b=QtGui.QPushbutton(title,fenetremere)
    def position(self,abscisse,ordonne,width,height):
        self.setGeometry(abscisse,ordonne,width,height)
class Ui_form(object):
    def setup(self,Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(5,5)
        self.labelImage=QtGui.QLabel(Form)
        self.labelImage.setGeometry(QtCore.QRect(5,10,100,100))
        self.labelImage.setStyleSheet(_fromUtf8("background-color:rgb(180,180,180);"))
        self.labelImage.setText(_fromUtf8(""))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self,Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form","PyQt:dessin:qpixmap et formes",None,QtGui.QApplication.UnicodeUTF8))                                   

def enregistrer(A,file):#on stocke toutes les methodes appliquees a l automate dans dictmethode depuis qu'il est vide,puis on enregistre dans un fichier
        #On sait que toutes methodes appliquées sont dans A.method
        File=open(file,'w')
        for content in A.method:
            File.write(str(content)+'\n')#A la fin,toutes les methodes se trouvent dans le fichier

def convert(dictmethode):#Cette methode permet de convertir le contenu du fichier en un vrai dictionnaire
    result=[]
    for contenu in dictmethode:
        if (len(contenu)==9):
            first_element=contenu[2]+contenu[3]
            second_element=int(contenu[7])
            result.append([first_element,second_element])
        if (len(contenu)!=9):
            first_element=contenu[2]+contenu[3]
            second_element=int(contenu[7])
            third_element=int(contenu[10])
            fourth_element=contenu[14]
            result.append([first_element,second_element,third_element,fourth_element])
    return result

def reload(file):#Cette methode servira a recharger ll automate de la session precedente a partir du fichier 
    A=auto_ludo.automate()
    dictmethode=[]
    with open(file,'r') as fichier:
        for ligne in fichier:
            dictmethode.append(ligne.replace('\n',''))
        #On a donc fini de recuperer nos methodes pour la session precedente
        dictmethode=convert(dictmethode)
        for contenu in dictmethode:
            if(contenu[0]=='AE'):
               A.ajoute_etat(contenu[1])
            if(contenu[0]=='AI'):
               A.ajoute_initial(contenu[1])
            if(contenu[0]=='AF'):
               A.ajoute_etat(contenu[1])
            if(contenu[0]=='AT'):
               A.ajoute_transition(int(contenu[1]),int(contenu[2]),contenu[3])
            if(contenu[0]=='SE'):
               A.supprime_etat(int(contenu[1]),int(contenu[2]),contenu[3])
        return A

file='save.txt'
A=auto_ludo.automate()
B=auto_ludo.automate()
verif='false'

def affiche(A):
    print(A.initial)

class Fenetre(QtGui.QMainWindow,Ui_form):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__(None)
        self.setWindowTitle('Fenetre principale')
        self.resize(1000,1000)
        self.numberautomate=0
        #self.image="image.jpg"
        #self.label=QtGui.QLabel(self)
        #self.label.setGeometry(0,0,1000,1000)
        #self.label.setPixmap(QtGui.QPixmap(self.image))
        #On cree une zone de sous fenetre
        
        self.sffirst=QtGui.QMdiArea(self)
        self.sffirst.setGeometry(200,200,400,400)
        self.zone1=QtGui.QTextEdit(self.sffirst)
        self.zone2=QtGui.QTextEdit(self.sffirst)
        QSub1=self.sffirst.addSubWindow(self.zone1)
        QSub2=self.sffirst.addSubWindow(self.zone2)
        self.setCentralWidget(self.sffirst)
        self.sffirst.setViewMode(QtGui.QMdiArea.TabbedView)
        
        #On finit la creation des sous fenetres
        self.bouton_save=QtGui.QPushButton("Save",self)#pour enregistrer l automate
        self.bouton_save.setGeometry(20,20,100,100)
        self.bouton_load=QtGui.QPushButton("Load",self)#pour charger l automate
        self.bouton_load.setGeometry(300,20,100,100)
        self.bouton_quit=QtGui.QPushButton("Quit",self)#pour fermer la fenetre principale
        self.bouton_quit.setGeometry(160,20,100,100)
        self.bouton_recup=QtGui.QPushButton("recup",self)#pour recuperer l automate de la session precedente
        self.bouton_recup.setGeometry(440,20,100,100)
        #file='save.txt'
        #Cette liste contiendra l automate initial ainsi que toutes les methodes appliquees
        #File=open('save.txt','w')
        #File.write("ABRAHAM")
        #File.close()
        A=auto_ludo.automate()
        self.numberautomate+=1
        etat=1
        A.ajoute_initial(etat)
        etat=2
        A.ajoute_final(etat)
        etat=3
        A.ajoute_etat(etat)
        A.ajoute_transition(1,2,'A')
        enregistrer(A,file)
        #B=reload(file)
        
        #A.supprime_etat(3)
       # A.supprime_transition(1,2,'A')
        self.connect(self.bouton_quit,QtCore.SIGNAL("clicked()"),self.slot_quit)
        self.connect(self.bouton_save,QtCore.SIGNAL("clicked()"),self.slot_save)
        self.connect(self.bouton_load,QtCore.SIGNAL("clicked()"),self.slot_load)
        #On met les boutons pour l'affichage des diverses operations
        self.VAE=QtGui.QPushButton("L'état ajouté",self)
        self.VAE.setGeometry(780,200,150,20)

        self.VAT=QtGui.QPushButton("La transition ajoutée ",self)
        self.VAT.setGeometry(780,250,150,20)

        self.VST=QtGui.QPushButton("La transition supprimée",self)
        self.VST.setGeometry(780,300,150,20) 
       
        self.VSE=QtGui.QPushButton("L'état supprimé",self)
        self.VSE.setGeometry(780,350,150,20) 
        #On affiche l'opération proprement dite
        self.visuAE=QtGui.QLCDNumber(self)
        self.visuAE.setGeometry(960,200,40,20)

        self.visuAT=QtGui.QLCDNumber(self)
        self.visuAT.setGeometry(960,250,40,20)

        self.visuST=QtGui.QLCDNumber(self)
        self.visuST.setGeometry(960,300,40,20)

        self.visuSE=QtGui.QLCDNumber(self)
        self.visuSE.setGeometry(960,350,40,20)
        #On affiche ce qu'il faut
        self.connect(self.visuAE,QtCore.SIGNAL("clicked()"),self.actionvisuAE)
        self.connect(self.visuAT,QtCore.SIGNAL("clicked()"),self.actionvisuAT)
        self.connect(self.visuST,QtCore.SIGNAL("clicked()"),self.actionvisuST)
        self.connect(self.visuSE,QtCore.SIGNAL("clicked()"),self.actionvisuSE)
        #self.E_A=QtGui.QLcdNumber()
        #self.E_A.setGeometry(
        #On commence la mise en place de la zone de dessin
        Fen=QtGui.QWidget()
        Fen.resize(5,5)
        self.draw_zone=QtGui.QLabel("Zone de dessin",self)
        self.draw_zone.setGeometry(QtCore.QRect(200,200,400,400))
        self.draw_zone.setStyleSheet(_fromUtf8("background-color:rgb(180,180,180);"))
        self.draw_zone.setText(_fromUtf8(""))
        self.image=QtGui.QImage(self.draw_zone.size(),QtGui.QImage.Format_RGB32) # crée image RGB 32 bits même taille que la zone de dessin
        #-- opérations de dessin sur le QImage
        self.image.fill(QtGui.QColor(255,255,255)) # fond blanc
        # coordonnées centre du QPixmap (même taille que label)
        xo=self.image.width()/2
        yo=self.image.height()/2
        
        self.painter=QtGui.QPainter(self.image)
        self.pen=QtGui.QPen() # crayon par défaut pour le painter - ligne continue
        self.pen.setWidth(3) # fixe largeur crayon 
        self.pen.setColor(QtGui.QColor(0,255,0)) # fixe couleur crayon                
        self.painter.setPen(self.pen) # affecte le crayon defini au dessin - les paramètres s'appliquent seulement une fois setPen() appelé
        #On dessine ainsi un rectangle
        self.painter.drawEllipse(xo,yo,20,20)
        self.painter.fillRect(xo,yo,20,20,QtGui.QColor(255,255,0))
        self.pixmap=QtGui.QPixmap.fromImage(self.image) # chargement qu, QImage dans le QPixmap - fonction begin intégrée...
        self.draw_zone.setPixmap(self.pixmap) # met à jour le qpixmap affiché dans le qlabel
        #self.draw_zone.setWindowTitle("Zone de dessin")
        #self.draw_zone.resize(100,100)
        #self.labim=QtGui.QLabel(self.draw_zone)
        #self.labim.setGeometry(QtCore.QRect(5,5,80,80))
        self.message_zone=QtGui.QTextEdit(self)
        self.message_zone.setGeometry(900,0,100,100)
        #faire une fenetre dans ma fenetre principale qui glisse
        
    def slot_quit(self):#On fait le slot correspondant pour afficher le message correspondant au signal envoye par le fait de cliquer sur le bouton quit
        reponse=QtGui.QMessageBox.question(self,self.tr("Attention"),self.tr("Vous voulez sauvegarger avant de fermer?"),QtGui.QMessageBox.Ok)
        sys.exit()

    def slot_save(self):
        enregistrer(A,file)

    def slot_load(self):
        B=reload(file)
        affiche(B)
    def actionvisuAE(self):
        print("donnez l'état à ajouter")
        etat=input()#on demande
        if(isinstance(etat,int)):
            self.visuAE.display(etat)
        if(not isinstance(etat,int)):
            QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
    def actionvisuAT(self):
        print("Donnez le départ")
        depart=input()#on demande
        print("Donnez l'arrivée")
        arrivee=input()#on demande
        print("donnez la lettre")
        lettre=input()#on demande
        if(isinstance(depart,int)&isinstance(arrivee,int)& isinstance(lettre,str) ):
            self.visuAT.display(lettre)
        if(not(isinstance(depart,int)&isinstance(arrivee,int)& isinstance(lettre,str))):
            QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Vérifiez les données:les 2 premiers paramètres sont des entiers et le troisième est une lettre"))
    def actionvisuST(self):
        print("Donnez le départ")
        depart=input()#on demande
        print("Donnez l'arrivée")
        arrivee=input()#on demande
        print("donnez la lettre")
        lettre=input()#on demande
        if(isinstance(depart,int)&isinstance(arrivee,int)& isinstance(lettre,str) ):
            self.visuST.display(lettre)
        if(not(isinstance(depart,int)&isinstance(arrivee,int)& isinstance(lettre,str))):
            QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Vérifiez les données:les 2 premiers paramètres sont des entiers et le troisième est une lettre"))
    def actionvisuSE(self):
        print("donnez l'état à supprimer")
        etat=input()#on demande
        if(isinstance(etat,int)):
            self.visuSE.display(etat)
        if(not isinstance(etat,int)):
            QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
    

        #Affiche(automate) mais la fonction affiche automate n'est pas encore faite
        #print(B.transition)
application = QtGui.QApplication(sys.argv)
fenetreprincipale=Fenetre()
fenetreprincipale.show()
fenetreprincipale.raise_()
sys.exit(application.exec_())
