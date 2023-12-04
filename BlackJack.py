import random


# Classe représentant la main de cartes d'un joueur ou de la banque
class Main_cartes(object):
    def __init__(self, est_banque=False):
        self.est_banque = est_banque
        self.main = []
        self.reveler_deuxieme_carte = False
    
    # Méthode pour afficher la main du joueur ou de la banque
    def __str__(self):
        result = ""
        if not self.est_banque:
            # Affichage de la main du joueur
            if len(self.main) == 0:
                result = "Votre main est vide"
            else:
                result = "La main du joueur est : " + ", ".join(self.main) + " (" + str(self.points()) + ")"
        else:
            # Affichage de la main de la banque
            if len(self.main) == 0:
                result = "La main de la banque est vide"
            else:
                main_revelee = self.main[:]  # Faites une copie de la main pour révéler la deuxième carte
                if self.reveler_deuxieme_carte is False:
                    main_revelee[1] = "Carte Cachée"
    
                if self.reveler_deuxieme_carte is True:
                    result = "La main de la banque est : " + ", ".join(main_revelee) + " (" + str(self.points()) + ")"
                else:
                    result = "La main de la banque est : " + ", ".join(main_revelee) + " (" + str(self.points() - cartes[self.main[1]]) + ")"
                    
        return str(result)

    # Méthode pour ajouter une carte à la main
    def ajouter(self, carte):
        self.main.append(carte)

    # Méthode pour calculer le total des points dans la main
    def points(self):
        somme = 0
        compteur_as = 0  # Compteur d'As dans la main

        for carte in self.main:
            somme += cartes[carte]
            if cartes[carte] == 11:
                compteur_as += 1

        # Vérification si la somme dépasse 21 et ajustement de la valeur des As si nécessaire
        while somme > 21 and compteur_as > 0:
            somme -= 10  # Réduire de 10 pour un As
            compteur_as -= 1

        return somme

    # Méthodes pour vérifier si la main dépasse 21 ou si elle est un blackjack
    def booleen(self):
        return self.points() > 21

    def blackjack(self):
        return self.points() == 21

    # Méthode pour vider la main
    def vider(self):
        self.main = []
        return self

    # Méthode pour révéler la première carte de la banque
    def devoiler(self):
        result = ""
        result += self.main[1]      
        print(f"La carte cachée est : {result}")
        
        return str(result)


# Classe représentant les gains et les pertes
class Gain_perte(object):
    def __init__(self, mon_dep, mon_act):
        self.montant_depart = mon_dep
        self.montant_actuel = mon_act

    # Méthode pour afficher les gains et pertes
    def __str__(self):
        gains = self.montant_actuel - self.montant_depart
        return f"Le montant de départ était : {self.montant_depart}€\nLes gains actuels sont : {gains}€"

    # Méthode pour vérifier si une mise est possible
    def mise_possible(self, mise):
        if self.montant_depart < mise:
            return False
        return True


# Méthode pour mélanger le paquet de cartes
def melanger_cartes(jeu, n):
    jeu = jeu * n
    random.shuffle(jeu)
    return jeu


# Méthode pour jouer une partie de blackjack
def jouer_partie(montant_depart, mise, paquet):
    joueur1 = Main_cartes()
    joueur1_argent = Gain_perte(montant_depart, montant_depart)
    croupier = Main_cartes(True)
    
    while not joueur1_argent.mise_possible(mise):
        mise = int(input("Entrez la mise pour cette partie : "))
        if not joueur1_argent.mise_possible(mise):
            print("ERREUR ! ")
        
    # Distribution des cartes initiales
    joueur1.ajouter(paquet[0][0])
    joueur1.ajouter(paquet[2][0])
    croupier.ajouter(paquet[1][0])
    croupier.ajouter(paquet[3][0])
    print(joueur1)
    print(croupier)

    i = 4  # Indice de la prochaine carte à piocher

    # Tour du joueur
    while not joueur1.booleen() and not joueur1.blackjack():
            
        action = input("\nVoulez-vous rester, tirer ou doubler ? (r/t/d) ")
        while mise * 2 > joueur1_argent.montant_actuel and action.lower() == 'd':
            print("Vous n'avez pas assez d'argent pour doubler ! ")
            action = input("\nVoulez-vous rester, tirer ou doubler ? (r/t/d) ")
            
        #Option Tirer + Doubler
        if action.lower() == 't' or action.lower() == 'd':
            nouvelle_carte = paquet[i][0]
            joueur1.ajouter(nouvelle_carte)
            print(f"Vous avez reçu une nouvelle carte : {nouvelle_carte}")
            print(joueur1)
            print(croupier)
            
            if action.lower() == 'd':
                mise = mise * 2
            
            i += 2
    
        #Option Rester        
        else:
            break
    
    # Dévoiler la carte cachée de la banque après le tour du joueur
    croupier.reveler_deuxieme_carte = True
    croupier.devoiler()
    print(croupier)

    i = 5  # Indice de la prochaine carte à piocher pour la banque

    # Tour de la banque
    while croupier.points() < 17 and not joueur1.blackjack() and not joueur1.booleen():
        nouvelle_carte = paquet[i][0]
        croupier.ajouter(nouvelle_carte)
        print(f"La banque a reçu une nouvelle carte : {nouvelle_carte}")
        print(croupier)
        i += 2

    # Résultat de la partie
    if joueur1.blackjack():
        print("Blackjack du joueur.\n")
        joueur1_argent.montant_actuel += mise * 1.5  # Le montant du joueur augmente de sa mise multipliée par 1.5.
        print(f"{joueur1_argent}")
        
    elif croupier.blackjack():
        print("Blackjack de la banque.\n")
        joueur1_argent.montant_actuel -= mise  # Le joueur diminue de sa mise
        print(f"{joueur1_argent}")
          
    elif croupier.booleen():
        print("La banque a dépassé 21. Le joueur gagne.\n")
        joueur1_argent.montant_actuel += mise  # Le joueur gagne sa mise
        print(f"{joueur1_argent}")
        
    elif joueur1.booleen():
        print("Le joueur a dépassé 21. La banque gagne.\n")
        joueur1_argent.montant_actuel -= mise  # Le joueur diminue de sa mise
        print(f"{joueur1_argent}")
        
    elif joueur1.points() > croupier.points() and joueur1.points() < 21:
        print("Le joueur gagne.\n")
        joueur1_argent.montant_actuel += mise  # Le joueur gagne sa mise
        print(f"{joueur1_argent}")
        
    elif joueur1.points() < croupier.points() and croupier.points() < 21:
        print("La banque gagne.\n")
        joueur1_argent.montant_actuel -= mise  # Le joueur perd sa mise
        print(f"{joueur1_argent}")
        
    else:
        print("Égalité (push).\n")  # Le montant du joueur reste inchangé.
        print(f"{joueur1_argent}")
    
    return joueur1_argent.montant_actuel


def play_again():
    start = input("Jouer encore ? (o/n) ")
    if start.lower() == 'o':
        return True
    print("\nAu revoir ! ")
    return False

print("\nSIMULATEUR DE BLACKJACK\n")

n = int(input("Combien de jeux de cartes voulez-vous jouer ? "))    
montant = int(input("Entrez le montant de départ : "))
while True:
    
    # Définition des cartes et de leurs valeurs
    paquet = [
        # Chaque carte est représentée par une liste avec son nom et sa valeur
        ["As de piques", 11], ["Deux de piques", 2], ["Trois de piques", 3], ["Quatre de piques", 4], ["Cinq de piques", 5],
        ["Six de piques", 6], ["Sept de piques", 7], ["Huit de piques", 8], ["Neuf de piques", 9], ["Dix de piques", 10],
        ["Valet de piques", 10], ["Dame de piques", 10], ["Roi de piques", 10], ["As de carreaux", 11], ["Deux de carreaux", 2],
        ["Trois de carreaux", 3], ["Quatre de carreaux", 4], ["Cinq de carreaux", 5], ["Six de carreaux", 6], ["Sept de carreaux", 7],
        ["Huit de carreaux", 8], ["Neuf de carreaux", 9], ["Dix de carreaux", 10], ["Valet de carreaux", 10], ["Dame de carreaux", 10],
        ["Roi de carreaux", 10], ["As de coeurs", 11], ["Deux de coeurs", 2], ["Trois de coeurs", 3], ["Quatre de coeurs", 4],
        ["Cinq de coeurs", 5], ["Six de coeurs", 6], ["Sept de coeurs", 7], ["Huit de coeurs", 8], ["Neuf de coeurs", 9],
        ["Dix de coeurs", 10], ["Valet de coeurs", 10], ["Dame de coeurs", 10], ["Roi de coeurs", 10], ["As de trèfles", 11],
        ["Deux de trèfles", 2], ["Trois de trèfles", 3], ["Quatre de trèfles", 4], ["Cinq de trèfles", 5], ["Six de trèfles", 6],
        ["Sept de trèfles", 7], ["Huit de trèfles", 8], ["Neuf de trèfles", 9], ["Dix de trèfles", 10], ["Valet de trèfles", 10],
        ["Dame de trèfles", 10], ["Roi de trèfles", 10]
    ]

    # Création d'un dictionnaire pour associer les noms des cartes à leurs valeurs
    cartes = {}
    for carte, valeur in paquet:
        cartes[carte] = valeur
     
    paquet = melanger_cartes(paquet, n)
    
    if montant != 0:
        mise = int(input("Entrez la mise pour cette partie : "))
        if mise > montant:
            print("ERREUR ! ")
                
        montant = jouer_partie(montant, mise, paquet)
        print(f"Montant actuel : {montant}\n")
        
        if montant != 0 and not play_again():
            break
    else:
        print("Vous n'avez plus d'argent à miser ! :(\nAu revoir ! ")
        break