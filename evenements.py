"""Julien L. — Evenement et ses sous-classes.

jouer(jeu) renvoie True quand l'étape d'histoire est validée, False sinon
(elle sera rejouée au prochain retour au garage).
"""

from outils import titre, demander_nombre, oui_non, pause


class Evenement:
    """Classe mère des événements d'histoire. Chaque enfant redéfinit jouer()."""

    def __init__(self, titre, texte):
        self.titre = titre
        self.texte = texte
        self.deja_vu = False

    def afficher(self):
        """Affiche le texte la première fois, puis un simple rappel."""
        titre(f"HISTOIRE — {self.titre}")
        if self.deja_vu:
            print("(rappel)")
        else:
            print(self.texte)
            self.deja_vu = True

    def jouer(self, jeu):
        """Joue l'événement. Renvoie True si l'étape d'histoire est validée."""
        raise NotImplementedError


class EvenementChoix(Evenement):
    """Une scène suivie d'un choix ; chaque option a des effets (thune, réputation, message)."""

    def __init__(self, titre, texte, options):
        """options : liste de (libellé, effets), effets étant un dict lu par Jeu.appliquer_effets."""
        super().__init__(titre, texte)
        self.options = options

    def jouer(self, jeu):
        """Propose les options et applique les effets de celle choisie."""
        self.afficher()
        for i, (libelle, _) in enumerate(self.options, 1):
            print(f"{i}. {libelle}")
        _, effets = self.options[demander_nombre(1, len(self.options)) - 1]
        jeu.appliquer_effets(effets)
        pause()
        return True


class EvenementCombat(Evenement):
    """Un combat d'histoire contre un adversaire, dans une arène donnée."""

    def __init__(self, titre, texte, adversaire, arene):
        super().__init__(titre, texte)
        self.adversaire = adversaire
        self.arene = arene

    def jouer(self, jeu):
        """Lance le combat ; l'étape n'est validée qu'en cas de victoire."""
        self.afficher()
        if jeu.joueur.vehicule is None:
            print(f"{self.adversaire.nom} t'attend. Construis d'abord un véhicule !")
            return False
        if not oui_non(f"Affronter {self.adversaire.nom} maintenant ?"):
            return False
        gagnant = self.arene.combattre(jeu.joueur, self.adversaire)
        if gagnant is jeu.joueur:
            jeu.gagner_combat(self.adversaire)
            return True
        print("Défaite... Améliore ton véhicule et reviens.")
        return False


class EvenementCommande(Evenement):
    """Une commande d'histoire, validée quand le joueur la livre."""

    def __init__(self, titre, texte, commande):
        super().__init__(titre, texte)
        self.commande = commande

    def jouer(self, jeu):
        """Ajoute la commande au menu Commandes ; l'histoire avance à la livraison."""
        self.afficher()
        print(f"Nouvelle commande : {self.commande.resume()}")
        print("(À livrer depuis le menu Commandes.)")
        jeu.ajouter_commande_histoire(self.commande)
        pause()
        return False  # l'étape est validée à la livraison (voir Jeu.livrer)
