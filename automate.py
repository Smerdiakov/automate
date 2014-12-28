########################
## La classe automate ##
########################

# les etats de l'automate sont des ensembles
# la classe automate contient 3 champs :
# 	la liste des etats initiaux
# 	la liste des etats finaux
# 	le dictionnaire des transitions
# l'etiquette d'une epsilon-transition sera le string vide

class automate :
	def __init__(self):
		self.initial=[]
		self.final=[]
		self.transition={}
		
###  methodes d'ajout : ###
###########################

# ajout d'un etat	
	def ajoute_etat(self,etat):
		if(not(etat in self.transition)):
			self.transition[etat]={}

# ajout d'un etat initial
	def ajoute_initial(self,etat):
		if(etat in self.transition):
			pass
		else:
			self.ajoute_etat(etat)			
		if etat in self.initial:
			pass
		else :
			self.initial.append(etat)
			
# ajout d'un etat final
	def ajoute_final(self,etat):
		if(etat in self.transition):
			pass
		else:
			self.ajoute_etat(etat)		
		if etat in self.final:
			pass
		else :
			self.final.append(etat)
	
# ajout d'une transition
	def ajoute_transition(self, depart, arrivee, lettre):
		assert(depart in self.transition)	
		assert(depart in self.transition)
		if lettre in self.transition[depart]:
			if arrivee in self.transition[depart][lettre]:
				pass 
			else :
				self.transition[depart][lettre].append(arrivee)
		else :
			self.transition[depart][lettre]=[arrivee]
	
# quelques methodes d'ajouts massifs :
	def ajoute_liste_etat (self, liste_etat):
		for etat in liste_etat:
			self.ajoute_etat(etat)
			
	def ajoute_liste_initial (self, liste_etat):
		for etat in liste_etat:
			self.ajoute_initial(etat)
	
	def ajoute_liste_final (self, liste_etat):
		for etat in liste_etat:
			self.ajoute_final(etat)	
	
	def ajoute_liste_transition (self, liste_transition):
		# type liste_transition = [(etat, etat, lettre)]
		for transition in liste_transition:
			self.ajoute_transition(transition[0],transition[1],transition[2])


# ajoute une epsilon transition :
	def ajoute_epsilon(self,depart,arrive):
		self.ajoute_transition(depart,arrive,"")
		
# ajoute une liste de epsilon transition :
	def ajoute_liste_epsilon(self,liste_transition):
		for transition in liste_transition:
			self.ajoute_epsilon(transition[0],transition[1])
			
### methodes de suppression : ###
#################################

# suppression d'un etat
	def supprime_etat(self, etat):
		if etat in self.initial:
			self.initial.remove(etat)
		if etat in self.final:
			self.final.remove(etat)
		if etat in self.transition:
			del self.transition[etat]
		for autre_etat in self.transition:
			for lettre in self.transition[autre_etat]:
				if etat in self.transition[autre_etat][lettre]:
					self.transition[autre_etat][lettre].remove(etat)
					
# suppression d'une transition					
	def supprime_transition(self,depart,arrivee,lettre):
		if depart in self.transition:
			if lettre in self.transition[depart]:
				if arrivee in self.transition[depart][lettre]:
					self.transition[depart][lettre].remove(arrivee)
					if len(self.transition[depart][lettre])==0:
						del self.transition[depart][lettre]
						
# supprime une lettre de l'alphabet de l'automate (ainsi que les transitions associees):
	def supprime_lettre(self,lettre_a_supprimer):
		for etat in self.transition:
			if lettre_a_supprimer in self.transition[etat]:
				del self.transition[etat][lettre_a_supprimer]
	
# vide l'automate :
	def vide(self):
		self.initial=[]
		self.final=[]
		self.transition={}
		
### Quelques booleens : ###
###########################

# l'automate en argument est-il correct ?
	def est_correct(self):
		booleen = True
		if len(self.initial)==0:
			return False
		for depart in self.transition:
			for lettre in self.transition[depart]:
				for arrivee in self.transition[depart][lettre]:
					booleen = booleen and (arrivee in self.transition)
		for etat in self.initial:
			booleen = booleen and (etat in self.transition)
		for etat in self.final:
			booleen = booleen and (etat in self.transition)
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
					liste_images.append(etat)
		supprime_doublons(liste_image)
		return liste_image

# l'ensemble des etats que l'on peut atteindre par epsilon-transition :
	def image_epsilon(self, depart):
		liste_eps=[depart]
		liste_eps_precedent=[]
		while not(len(liste_eps)==len(liste_eps_precedent)):
			liste_eps_precedent=liste_eps
			liste_eps=self.image_liste(liste_eps,"")
		return liste_eps

# renvoie l'alphabet de l'automate :
	def alphabet(self):
		alph = set()
		for depart in self.transition:
			for lettre in self.transition[depart]:
				alph=alph|set(lettre)
		return alph

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
		
		
		
# supprime les doublons d'une liste :
def supprime_doublons(liste):
	liste_ref=[]
	for element in liste:
		if not (element in liste_ref):
			liste_ref.append(element)
	liste = liste_ref
	
			