"""Membre 3 — Evenement et ses sous-classes.

jouer(jeu) renvoie True quand l'étape d'histoire est validée, False sinon
(elle sera rejouée au prochain retour au garage).
"""

from outils import titre, demander_nombre, oui_non, pause


class Evenement:
    def __init__(self, titre, texte):
        self.titre = titre
        self.texte = texte
        self.deja_vu = False

    def afficher(self):
        titre(f"HISTOIRE — {self.titre}")
        if self.deja_vu:
            print("(rappel)")
        else:
            print(self.texte)
            self.deja_vu = True

    def jouer(self, jeu):
        raise NotImplementedError


class EvenementChoix(Evenement):
    def __init__(self, titre, texte, options):
        """options : liste de (libellé, effets), effets étant un dict lu par Jeu.appliquer_effets."""
        super().__init__(titre, texte)
        self.options = options

    def jouer(self, jeu):
        self.afficher()
        for i, (libelle, _) in enumerate(self.options, 1):
            print(f"{i}. {libelle}")
        _, effets = self.options[demander_nombre(1, len(self.options)) - 1]
        jeu.appliquer_effets(effets)
        pause()
        return True


class EvenementCombat(Evenement):
    def __init__(self, titre, texte, adversaire, arene):
        super().__init__(titre, texte)
        self.adversaire = adversaire
        self.arene = arene

    def jouer(self, jeu):
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
    def __init__(self, titre, texte, commande):
        super().__init__(titre, texte)
        self.commande = commande

    def jouer(self, jeu):
        self.afficher()
        print(f"Nouvelle commande : {self.commande.resume()}")
        print("(À livrer depuis le menu Commandes.)")
        jeu.ajouter_commande_histoire(self.commande)
        pause()
        return False  # l'étape est validée à la livraison (voir Jeu.livrer)
