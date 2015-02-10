import sys
import os
import time
import dessinjuao
from dessinjuao import*
from PyQt4 import QtGui,QtCore
import automates
import determine
#import classe_etat_transition
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


def dessinauto(A,parent,abscisse,ordonne,hauteur,largeur):
    graphe = Graphe(A,400)
    view = QtGui.QGraphicsView(graphe,parent)
    view.setGeometry(abscisse,ordonne,hauteur,largeur)
    
def efface(parent,abscisse,ordonne,hauteur,largeur):
    view = QtGui.QGraphicsView(graphe,parent)
    view.setGeometry(abscisse,ordonne,hauteur,largeur)

def reloadf(file):#Cette methode servira a recharger ll automate de la session precedente a partir du fichier
    A=automate.automate()
    dictmethode=[]
    temp=[]
    with open(file,'r') as fichier:
        for ligne in fichier:
            dictmethode.append(ligne.replace('\n',''))
        #On a donc fini de recuperer nos methodes pour la session precedente
    #print(dictmethode)
        for contenu in dictmethode:
             if(contenu[1]=='AE'):
                 depart=contenu[0]
                 etat=Etat(depart,False)
                 A.ajoute_etat(etat)
             if (contenu[1]=='AT'):
                 depart=contenu[2]+contenu[3]
                 etat1 = Etat(depart,False)
                 etat2 = Etat(contenu[2],False)
                 lettre=contenu[3]
                 A.ajoute_etat(etat1)
                 A.ajoute_initial(etat2)
                 A.ajoute_transition(etat1, etat2, lettre)
             if(contenu[1]=='ST'):
                 A.supprime_transition(int(contenu[0]),int(contenu[2]),contenu[3])
             if (contenu[1]=='SE'):
                 A.supprmime_etat(int(contenu[0]))
             if(contenu[1]=='EI'):
                 depart=contenu[0]
                 etat=Etat(depart,False)
                 A.ajoute_initial(etat)
             if(contenu[1]=='EF'):
                 depart=contenu[0]
                 etat=Etat(depart,True)
                 A.ajoute_final(etat)
             if(contenu[1]=='ET'):
                 depart=contenu[0]
                 etat=Etat(depart,False)
                 A.ajoute_transition(etat,etat,'')
    return A

filefirst='save.txt'
filesecon='othersave.txt'


def affiche(A):
    print(A.initial)
dictmethod1=[]
dictmethod2=[]

class Fenetre(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__(None)
        self.setWindowTitle('Fenetre principale')
        self.resize(1000,1000)
        self.numberautomate=0
       
        self.autocourant=automates.automate()#sera autofirst ou autosecon suivant la sous fenetre dans laquelle on se trouve
        self.zonecourant=QtGui.QMainWindow()
        self.repere=0#pour savoir si on est dans la sous fenetre 1 ou la sous fenetre 2
        self.sffirst=QtGui.QMdiArea(self)
        self.sffirst.setGeometry(200,200,400,400)
        self.zone1=QtGui.QMainWindow(self.sffirst)
        self.zone2=QtGui.QMainWindow(self.sffirst)
        QSub1=self.sffirst.addSubWindow(self.zone1)
        self.autofirst=automates.automate()
        QSub2=self.sffirst.addSubWindow(self.zone2)
        self.autosecon=automates.automate()
       
        self.setCentralWidget(self.sffirst)
        self.sffirst.setViewMode(QtGui.QMdiArea.TabbedView)
        self.view = QtGui.QGraphicsView()
        self.repere=1#pour savoir si on est dans la zone 1 ou la zone 2,1 correspondant à la zone 1,2correspondant à la zone 2
        self.view = QtGui.QGraphicsView(self.zonecourant)
        #On introduit une image de fond dans la seconde zone
        self.image="image.jpg"
        self.label=QtGui.QLabel(self.zone1)
        self.label.setGeometry(0,0,1000,1000)
        self.label.setPixmap(QtGui.QPixmap(self.image))
        #On introduit image dans la seconde zone d
        self.imag="image.jpg"
        self.label=QtGui.QLabel(self.zone2)
        self.label.setGeometry(0,0,1000,1000)
        self.label.setPixmap(QtGui.QPixmap(self.imag))
        
        self.bouton_zone1=QtGui.QPushButton("ZONE1",self)#pour choisir si on est dans la zone 1
        self.bouton_zone1.setGeometry(0,20,100,30)
        self.bouton_zone2=QtGui.QPushButton("ZONE2",self)#pour choisir si on est dans la zone2
        self.bouton_zone2.setGeometry(900,20,100,30)
        self.bouton_save=QtGui.QPushButton("Save",self)#pour enregistrer l automate
        self.bouton_save.setGeometry(20+140,20,100,30)
        self.bouton_quit=QtGui.QPushButton("Quit",self)#pour fermer la fenetre principale
        self.bouton_quit.setGeometry(160+260,20,100,30)
        self.bouton_reload=QtGui.QPushButton("reload",self)
        self.bouton_reload.setGeometry(580+140,20,100,30)
        
        self.connect(self.bouton_quit,QtCore.SIGNAL("clicked()"),self.slot_quit)
        self.connect(self.bouton_save,QtCore.SIGNAL("clicked()"),self.slot_save)
        self.connect(self.bouton_reload,QtCore.SIGNAL("clicked()"),self.slot_reload)
        self.connect(self.bouton_zone1,QtCore.SIGNAL("clicked()"),self.slot1)
        self.connect(self.bouton_zone2,QtCore.SIGNAL("clicked()"),self.slot2)
       
        #On met les boutons pour l'affichage des diverses operations
       
        
        self.VAE=QtGui.QPushButton("L'état ajouté",self)#Ce bouton sert à ajouter un état
        self.VAE.setGeometry(780,200,150,20)

        self.VAT=QtGui.QPushButton("La transition ajoutée ",self)#ajout d'une transition
        self.VAT.setGeometry(780,250,150,20)

        self.VST=QtGui.QPushButton("La transition supprimée",self)#suppression d'une transition
        self.VST.setGeometry(780,300,150,20) 
       
        self.VSE=QtGui.QPushButton("L'état supprimé",self)#suppression d'un etat
        self.VSE.setGeometry(780,350,150,20)

        self.VEI=QtGui.QPushButton("L'état initial ajouté",self)#ajout d'un état
        self.VEI.setGeometry(780,400,150,20)

        self.VEF=QtGui.QPushButton("L'état final ajouté",self)#ajout d'un état final
        self.VEF.setGeometry(780,450,150,20)

        self.VET=QtGui.QPushButton("La transition epsilon",self)#ajout d'une epsilon transition
        self.VET.setGeometry(780,500,150,20)

        
        #On met en place les labels qui nous permettent de vérifier l'opération effectuée
        self.visuAE=QtGui.QLabel(self)
        self.visuAE.setGeometry(960,200,40,20)

        self.visuAT=QtGui.QLabel(self)
        self.visuAT.setGeometry(960,250,40,20)
        
        self.visuST=QtGui.QLabel(self)
        self.visuST.setGeometry(960,300,40,20)

        self.visuSE=QtGui.QLabel(self)
        self.visuSE.setGeometry(960,350,40,20)

        self.visuEI=QtGui.QLabel(self)
        self.visuEI.setGeometry(960,400,40,20)

        self.visuEF=QtGui.QLabel(self)
        self.visuEF.setGeometry(960,450,40,20)

        self.visuET=QtGui.QLabel(self)
        self.visuET.setGeometry(960,500,40,20)

        #On effectue ce qu'il faut lorsqu'une opération est sollicitée
        self.connect(self.VAE,QtCore.SIGNAL("clicked()"),self.actionVAE)
        self.connect(self.VST,QtCore.SIGNAL("clicked()"),self.actionVST)
        self.connect(self.VAT,QtCore.SIGNAL("clicked()"),self.actionVAT)
        self.connect(self.VSE,QtCore.SIGNAL("clicked()"),self.actionVSE)
        self.connect(self.VEF,QtCore.SIGNAL("clicked()"),self.actionVEF)
        self.connect(self.VEI,QtCore.SIGNAL("clicked()"),self.actionVEI)
        self.connect(self.VET,QtCore.SIGNAL("clicked()"),self.actionVET)
        self.graphe=Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(self.graphe,self.zonecourant)
        self.view.setGeometry(200,200,400,400)
    def slot1(self):
        self.repere=1
    def slot2(self):
        self.repere=2
    def slot_reload(self):
         self.autofirst=reloadf(filefirst)
         self.autosecon=reloadf(filesecon)
         graphe = Graphe(self.autofirst,400)
         self.view = QtGui.QGraphicsView(graphe,self.zone1)
         self.view.setGeometry(100,100,400,400)
         self.view.show()
         graphe = Graphe(self.autosecon,400)
         self.view = QtGui.QGraphicsView(graphe,self.zone2)
         self.view.setGeometry(100,100,400,400)
         self.view.show()
    def slot_quit(self):#On fait le slot correspondant pour afficher le message correspondant au signal envoye par le fait de cliquer sur le bouton quit
        reponse=QtGui.QMessageBox.question(self,self.tr("Attention"),self.tr("Vous voulez sauvegarger avant de fermer?"),QtGui.QMessageBox.Ok)
        sys.exit()

    def slot_save(self):#fonction pour enregistrer les automates
        Filefirst=open(filefirst,'w')
        for content in dictmethod1: 
            Filefirst.write(str(content)+'\n')#A la fin,toutes les methodes se trouvent dans le fichier
        Filesecon=open(filesecon,'w')
        for content in dicmethod2:
            Filesecon.write(str(content)+'\n')#A la fin,toutes les methodes se trouvent dans le fichier      

    
    def actionVET(self):
        depart=input()
        checkinteger=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6') | (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        if((not(checkinteger))):
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
        if(checkinteger):
            if(self.repere==1):
                QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Les epsilon transition se visualisant dans la fenetre2"))
            if(self.repere==2):
                etat=Etat(depart,False)
                dictmethod2=dictmethod1
                dictmethod2.append([depart,"ET","F"])
                self.autosecon=self.autofirst
                self.autosecon.ajoute_etat(etat)
                self.autosecon.ajoute_transition(etat,etat,'')
                self.visuET.setText(depart)
                graphe = Graphe(self.autosecon,400)
                self.view = QtGui.QGraphicsView(graphe,self.zone2)
                self.view.setGeometry(100,100,400,400)
                self.view.show()
        
                  
                  
    def actionVEI(self):
        depart=input()
        checkinteger=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6') | (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        if((not (checkinteger))):
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
        if(self.repere==1):
   
            if(checkinteger):
           
                etat=Etat(depart,False)
                self.autofirst.ajoute_initial(etat)
                self.autocourant=self.autofirst
                self.zonecourant=self.zone1
                dictmethod1.append([depart,"EI","F"])
        if(self.repere==2):
            if(checkinteger):
                etat=Etat(depart,False)
                self.autosecon.ajoute_initial(etat)
                self.autocourant=self.autosecon
                self.zonecourant=self.zone2
                dictmethod2.append([depart,"EI","F"])
                
        self.visuEI.setText(depart)
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
        self.view.show()
        
    def actionVAE(self):
        depart=input()
        checkinteger=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6') | (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        if( (not (checkinteger))):
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
        if(self.repere==1):
                if(checkinteger):
                   etat=Etat(depart,False)
                   dictmethod1.append([depart,"AE"])
                   self.autofirst.ajoute_etat(etat)
                   self.autocourant=self.autofirst
                   self.zonecourant=self.zone1
                
                
        if(self.repere==2):
            if(checkinteger):
                etat=Etat(depart,False)
                self.autosecon.ajoute_etat(etat)
                self.autocourant=self.autosecon
                self.zonecourant=self.zone2
                dictmethod2.append([depart,"AE"])
                
        self.visuAE.setText(depart)
        
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
       
        self.view.show()
    def actionVEF(self):
    
        depart=input()
        print("donnez etat")
        checkinteger=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6') | (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        if(not (checkinteger)):
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
        if(self.repere==1):        
            if(checkinteger):
                etat=Etat(depart,True)
                self.autofirst.ajoute_final(etat)
                self.autocourant=self.autofirst
                self.zonecourant=self.zone1
                dictmethod1.append([depart,"EF"])
                
        if(self.repere==2):
            if(checkinteger):
                etat=Etat(depart,True)
                self.autosecon.ajoute_final(etat)
                self.autocourant=self.autosecon
                self.zonecourant=self.zone2
                dictmethod2.append([depart,"EF"])
        self.visuEF.setText(depart)
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
        self.view.show()
       
    def actionVST(self):
        #print("Donnez le départ")
        depart=input()#on demande
        print("Donnez l'arrivée")
        arrivee=input()#on demande
        print("donnez la lettre")
        lettre=input()#on demande
        checkintegerd=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6')| (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        checkintegera=( (arrivee[0]=='1') | (arrivee[0]=='2') | (arrivee[0]=='3') | (arrivee[0]=='0') | (arrivee[0]=='4') | (arrivee[0]=='5') | (arrivee[0]=='6') | (depart[0]=='7') | (arrivee[0]=='8') | (arrivee[0]=='9'))
        checkintegerl=( (lettre[0]=='1') | (lettre[0]=='2') | (lettre[0]=='3') | (lettre[0]=='0') | (lettre[0]=='4') | (lettre[0]=='5') | (lettre[0]=='6') | (lettre[0]=='7') | (lettre[0]=='8') | (lettre[0]=='9'))
        if((not(checkintegerd)) | (not(checkintegera)) | checkintegerl):
               QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Vérifiez les données:les 2 premiers paramètres sont des entiers et le troisième est une lettre"))
        if(checkintegerd & checkintegera & (not(checkintegerl))):
            if(self.repere==1):
               self.autofirst.supprime_transition(int(depart),int(arrivee),lettre)#on effectue notre opération
               self.autocourant=self.autofirst#on actualise l'automate
               self.zonecourant=self.zone1
               dictmethod1.append([int(depart),"ST",int(arrivee),lettre])
            if(self.repere==2):
               self.autosecon.supprime_transition(int(depart),int(arrivee),lettre)#on effectue notre opération
               self.autocourant=self.autosecon#on actualise l'automate
               self.zonecourant=self.zone2
               dictmethod2.append([int(depart),"ST",int(arrivee),lettre])
        self.visuST.setText(lettre)
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
        self.view.show() 
    def actionVAT(self):
        print("Donnez le départ")
        depart=input()#on demande
        print("Donnez l'arrivée")
        arrivee=input()#on demande
        print("donnez la lettre")
        lettre=input()#on demande
        checkintegerd=( (depart[0]=='1') | (depart[0]=='2') | (depart[0]=='3') | (depart[0]=='0') | (depart[0]=='4') | (depart[0]=='5') | (depart[0]=='6') | (depart[0]=='7') | (depart[0]=='8') | (depart[0]=='9'))
        checkintegera=( (arrivee[0]=='1') | (arrivee[0]=='2') | (arrivee[0]=='3') | (arrivee[0]=='0') | (arrivee[0]=='4') | (arrivee[0]=='5') | (arrivee[0]=='6') | (arrivee[0]=='7') | (arrivee[0]=='8') | (arrivee[0]=='9'))
        checkintegerl=( (lettre[0]=='1') | (lettre[0]=='2') | (lettre[0]=='3') | (lettre[0]=='0') | (lettre[0]=='4') | (lettre[0]=='5') | (lettre[0]=='6') | (lettre[0]=='7') | (lettre[0]=='8') | (lettre[0]=='9'))
        temp=QtGui.QGraphicsView(self.zonecourant)
        temp.setGeometry(100,100,400,400)
        temp.show()
        print(checkintegerl)
        print(checkintegera)
        print(checkintegerd)
        if( (not(checkintegerd)) | (not(checkintegera)) | checkintegerl):
            print('on rentre')
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Vérifiez les données:les 2 premiers paramètres sont des entiers et le troisième est une lettre"))
        if(checkintegerd & checkintegera & (not(checkintegerl))):
            if(self.repere==1):
               etat1 = Etat(depart,False)
               etat2 = Etat(arrivee,False)
               self.autofirst.ajoute_etat(etat1)
               self.autofirst.ajoute_initial(etat2)
               self.autofirst.ajoute_transition(etat1, etat2, lettre)
               self.autocourant=self.autofirst
               self.zonecourant=self.zone1
               dictmethod1.append([depart,"AT",arrivee,lettre])
               
            if(self.repere==2):
               etat1 = Etat(depart,False)
               etat2 = Etat(arrivee,False)
               self.autosecon.ajoute_etat(etat1)
               self.autosecon.ajoute_initial(etat2)
               self.autosecon.ajoute_transition(etat1, etat2, lettre)
               self.autocourant=self.autosecon
               self.zonecourant=self.zone2
               dictmethod2.append([depart,"AT",arrivee,lettre])
               
        self.visuAT.setText(lettre)
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
        self.view.show()
    def actionVSE(self):
        print("donnez etat")
        etat=input()
        checkinteger=( (etat[0]=='1') | (etat[0]=='2') | (etat[0]=='3') | (etat[0]=='0') | (etat[0]=='4') | (etat[0]=='5') | (etat[0]=='6') | (etat[0]=='8') | (etat[0]=='9'))
        if(not(checkinteger)):
            QtGui.QMessageBox.critical(self,self.trUtf8("Error"),self.trUtf8("Je vous rappelle qu'un état est un entier"))
        if(checkinteger):
            if(self.repere==1):
               self.autofirst.supprime_etat(int(etat))
               self.autocourant=self.autofirst
               self.zonecourant=self.zone1
               dictmethod1.append([etat,"SE"])
            if(self.repere==2):
               self.autosecon.supprime_etat(etat)
               self.autocourant=self.autosecon
               self.zonecourant=self.zone2
               dictmethod1.append([etat,"SE"])
        self.visuSE.setText(etat)
        graphe = Graphe(self.autocourant,400)
        self.view = QtGui.QGraphicsView(graphe,self.zonecourant)
        self.view.setGeometry(100,100,400,400)
        self.view.show()
application = QtGui.QApplication(sys.argv)
fenetreprincipale=Fenetre()
fenetreprincipale.show()
fenetreprincipale.raise_()
sys.exit(application.exec_())


					

