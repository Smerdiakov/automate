########################
## La classe automate ##
########################

# les états de l'automate sont des ensembles
# la classe automate contient 3 champs :
#       la liste des états initiaux
#       la liste des états finaux
#       le dictionnaire des transitions
from copy import *
class automate :
        def __init__(self):
                self.initial=[]
                self.final=[]
                self.transition={}
                self.method=[]
                
# methodes d'ajout :
        def searcheetat(self,etat):
                result=-1
                for contenu in self.transition:
                        result=result+1
                        if contenu==etat :
                                break
                return self.transition[result]
                
        def ajoute_etat(self,etat):
                if(not(etat in self.transition)):
                        self.transition[etat]={}
                        self.method.append(['AE',etat,'F'])
                
        
        def ajoute_initial(self,etat):
                if(etat in self.transition):
                        pass
                else:
                        self.ajoute_etat(etat)
                        self.method.append(['AI',etat,'F'])
                        
                if etat in self.initial:
                        pass
                else :
                        self.initial.append(etat)
                        self.method.append(['AI',etat,'F'])
                        

        def ajoute_final(self,etat):
                if(etat in self.transition):
                        pass
                else:
                        self.ajoute_etat(etat)
                        self.method.append(['AF',etat,'T'])

                if etat in self.final:
                        pass
                else :
                        self.final.append(etat)
                        self.method.append(['AF',etat,'T'])

        def ajoute_transition(self, depart, arrivee, lettre):
                assert(depart in self.transition)       
                assert(depart in self.transition)
                if lettre in self.transition[depart]:
                        if arrivee in self.transition[depart][lettre]:
                                pass 
                        else :
                                self.transition[depart][lettre].append(arrivee)
                                self.method.append(['AT',depart,arrivee,lettre])
                                
                                        
                else :
                        self.transition[depart][lettre]=[arrivee]
                        self.method.append(['AT',depart,arrivee,lettre])
                        
                                        
                        
        
# methodes de suppression :

        def supprime_etat(self, etat):
                if etat in self.initial:
                        self.initial.remove(etat)
                        self.method.append(['SE',etat])
                if etat in self.final:
                        self.final.remove(etat)
                        self.method.append(['SE',etat])
                if etat in self.transition:
                        del self.transition[etat]
                for autre_etat in self.transition:
                        for lettre in self.transition[autre_etat]:
                                if etat in self.transition[autre_etat][lettre]:
                                        self.transition[autre_etat][lettre].remove(etat)
                                        self.method.append(['SE',etat])
                                        
        def supprime_transition(self,depart,arrivee,lettre):
                if depart in self.transition:
                        if lettre in self.transition[depart]:
                                if arrivee in self.transition[depart][lettre]:
                                        self.transition[depart][lettre].remove(arrivee)
                                        self.method.append(['ST',depart,arrivee,lettre])
                                        if (len(self.transition[depart][lettre])==0):
                                                del (self.transition[depart][lettre])
                                                self.method.append(['ST',depart,arrivee,lettre])
                                
# l'automate passé en argument est-il correct ?
        
        def est_correct(self):
                booleen = True
                if len(self.initial)==0:
                        return False
        
                for depart in self.transition:
                        for lettre in self.transition[depart]:
                                for arrivee in self.transition[depart][lettre]:
                                        booleen = booleen and (arrivee in self.transition)
                return booleen
                        
        # l'etat est-il un etat initial ?
        def est_initial(self, etat):
                return (etat in self.initial)
        
# l'etat est-il un etat final ?
        def est_final(self,etat):
                return (etat in self.final)
                
# l'automate est-il vide ?
        def est_vide(self):
                booleen = True
                booleen = booleen and (self.initial==[])
                booleen = booleen and (self.final==[])
                booleen = booleen and (self.transition=={})
                return booleen

# l'automate est-il sans epsilon-transition ?
        def est_sans_epsilon (self):
                for depart in self.transition:
                        for lettre in self.transition[depart]:
                                if (lettre == ""):
                                        return False
                                        
                return True
                
### Quelques methodes utiles ###
################################

# l'image d'un état par une lettre :
        def image(self, depart, lettre):
                assert(depart in self.transition)
                if lettre in self.transition[depart]:
                        return self.transition[depart][lettre]
                else :
                        return[]

# l'image d'une liste d'états par une lettre :
        def image_liste(self, liste_depart, lettre):
                liste_image=[]
                for depart in liste_depart :
                        images = self.image(depart,lettre)
                        for etat in images :
                                liste_image.append(etat)
                liste_image=supprime_doublons(liste_image)
                return liste_image
                
# les deux même fonction mais avec un type de retour "ensembliste"
        def image_set(self,depart,lettre):
                return frozenset(self.image(depart,lettre))
                
        def image_liste_set(self,liste_depart,lettre):
                return frozenset(self.image_liste(liste_depart,lettre))

# l'ensemble des etats que l'on peut atteindre par epsilon-transition :
        def image_epsilon(self, depart):
                liste_eps=[depart]
                liste_eps_precedent=[]
                while not(len(liste_eps)==len(liste_eps_precedent)):            
                        liste_eps_precedent=deepcopy(liste_eps) #copie profonde                 
                        liste_eps[len(liste_eps):]=self.image_liste(liste_eps,"")                                               
                        liste_eps=supprime_doublons(liste_eps)
                liste_eps.remove(depart)
                return liste_eps
                
# un epsilon chemin d'un etat à un autre :

        def epsilon_chemin(self, depart, arrive):
                assert(arrive in self.image_epsilon(depart))
                return self.auxiliaire(depart,[],arrive)
                
                
# auxiliaire de epsilon chemin
        def auxiliaire(self,etat, liste, arrive):
                if etat in liste :
                        return []
                elif etat==arrive:
                        return liste
                else:
                        for etat_suivant in self.image(etat,""):
                                liste.append(etat)
                                if self.auxiliaire(etat_suivant,liste,arrive) ==[]:
                                        liste.pop()
                                else :
                                        return(liste)
                        
# préimage d'un état par une lettre : (l'ensemble des etats qui peuvent atteindre 
# l'état passé en arguement à l'aide de la lettre passée en argument :
        def preimage(self,etat,lettre):
                liste = []
                for etats in self.liste_etats():
                        if etat in self.image(etats,lettre):
                                liste.append(etats)
                return liste
                                

# renvoie l'alphabet de l'automate :
        def alphabet(self):
                alph = set()
                for depart in self.transition:
                        for lettre in self.transition[depart]:
                                if not(lettre == ""):
                                        alph=alph|set(lettre)
                return alph
                
# renvoie la liste des états de l'automate :
        def liste_etats(self):
                liste = []
                for etat in self.transition :
                        liste.append(etat)
                return(supprime_doublons(liste))

# renvoie la liste des états intermediaires de l'automate :
        def liste_etats_intermediaires(self):
                liste = []
                etats = self.liste_etats()
                for etat in etats:
                        if etat not in (self.initial + self.final):
                                liste.append(etat)
                return(supprime_doublons(liste))

                                

# l'automate est-il déterministe ?
        def est_deterministe(self):
                booleen = (len(self.initial)<=1)
                for depart in self.transition:
                        for lettre in self.transition[depart]:
                                booleen = (len(self.transition[depart][lettre])==1)
                return booleen

# nombre d'etats de l'automate :
        def nombre_etat(self):
                nombre=0
                for etat in self.transition:
                        nombre+=1
                return nombre
                
# nombre d'etats initiaux de l'automate :
        def nombre_initial(self):
                nombre=0
                for etat in self.initial:
                        nombre+=1
                return nombre
                
# nombre d'etats finaux de l'automate :
        def nombre_final(self):
                nombre=0
                for etat in self.final:
                        nombre+=1
                return nombre

#nombre de transition
        def nombre_transitions(self):
                nombre=0
                for etat in self.transition:
                        for lettre in self.transition[etat]:
                                nombre+=len(self.transition[etat][lettre])
                return nombre
                                
#nombre de epsilon transition
        def nombre_epsilon(self):
                nombre=0
                for etat in self.transition:
                        for lettre in self.transition[etat]:
                                if lettre=="":
                                        nombre+=len(self.transition[etat][lettre])
                return nombre
                
# creation de l'automate qui sera utilisé pour les tests :
        def pour_le_test(self):
                self.vide()
                self.ajoute_etat(1)
                self.ajoute_initial(2)
                self.ajoute_etat(3)
                self.ajoute_final(4)
                self.ajoute_transition(1,2,"a")
                self.ajoute_transition(1,3,"a")
                self.ajoute_transition(2,2,"a")
                self.ajoute_transition(4,2,"b")
                self.ajoute_transition(4,3,"b")
                self.ajoute_transition(2,4,"b")
                self.ajoute_transition(2,1,"")
                
# change l'étiquetage des états de l'automate
# le test de cette methode est fait dans execution_test.py              
        def nouvelles_etiquettes(self):
                auto_local = automate()
                correspondance = {}
                nouvel_entier =1
                
                for depart in self.transition:
                        if not depart in correspondance :
                                correspondance[depart]=nouvel_entier
                                nouvel_entier = nouvel_entier +1
                                
                        for lettre in self.transition[depart]:
                                for arrivee in self.transition[depart][lettre]:
                                
                                        if not arrivee in correspondance :
                                                correspondance[arrivee]=nouvel_entier
                                                nouvel_entier = nouvel_entier +1
                                                        
                                        auto_local.ajoute_transition(correspondance[depart],correspondance[arrivee],lettre)
                                        
                for etat in self.initial:
                        if not etat in correspondance :
                                correspondance[etat]=nouvel_entier
                                nouvel_entier = nouvel_entier +1
                        auto_local.ajoute_initial(correspondance[etat])
                        
                for etat in self.final:
                        if not etat in correspondance :
                                correspondance[etat]=nouvel_entier
                                nouvel_entier = nouvel_entier +1
                        auto_local.ajoute_final(correspondance[etat])
                        
                self = auto_local
                
                
# supprime les doublons d'une liste :
# supprime les doublons d'une liste :
def supprime_doublons(liste):
        liste_ref=[]
        for element in liste:
                if not (element in liste_ref):
                        liste_ref.append(element)
        return liste_ref

                


                

