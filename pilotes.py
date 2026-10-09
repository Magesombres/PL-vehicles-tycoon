"""Membre 2 — Pilote, Joueur, Adversaire."""

import random

ACTIONS = {"1": "attaquer", "2": "foncer", "3": "proteger"}


class Pilote:
    """Classe mère : nom, véhicule, et tout ce qui sert en combat."""

    def __init__(self, nom, vehicule=None):
        self.nom = nom
        self.vehicule = vehicule
        # État de combat, réinitialisé par l'Arene à chaque match
        self.stats_combat = {}
        self.pv = 0
        self.distance = 0
        self.protege = False

    def preparer_combat(self, multiplicateurs):
        stats = self.vehicule.calculer_stats()
        for stat, mult in multiplicateurs.items():
            stats[stat] *= mult
        self.stats_combat = stats
        self.pv = stats["resistance"]
        self.distance = 0
        self.protege = False

    def choisir_action(self, cible, arene):
        """Redéfinie dans Joueur (clavier) et Adversaire (IA)."""
        raise NotImplementedError

    def subir(self, degats):
        if self.protege:
            degats //= 2
        degats = max(1, degats)
        self.pv = max(0, self.pv - degats)
        return degats

    def attaquer(self, cible):
        return cible.subir(self.stats_combat["puissance"] + random.randint(0, 5))

    def foncer(self, cible):
        """Avance (utile en course) et percute un peu l'adversaire au passage."""
        self.distance += self.stats_combat["vitesse"]
        return cible.subir(self.stats_combat["vitesse"] // 4)


class Joueur(Pilote):
    def __init__(self, nom, argent=120):
        super().__init__(nom)
        self.argent = argent
        self.pieces = []
        self.vehicules = []
        self.reputation = {"A": 0, "B": 0, "C": 0, "D": 0}  # cachée au joueur

    def choisir_action(self, cible, arene):
        print("1. Attaquer   2. Foncer   3. Se protéger")
        while True:
            choix = input("> ").strip()
            if choix in ACTIONS:
                return ACTIONS[choix]
            print("Choix invalide.")

    def retirer_vehicule(self, vehicule):
        self.vehicules.remove(vehicule)
        if self.vehicule is vehicule:
            self.vehicule = self.vehicules[0] if self.vehicules else None


class Adversaire(Pilote):
    def __init__(self, nom, vehicule, niveau=1, recompense=50, replique="..."):
        super().__init__(nom, vehicule)
        self.niveau = niveau
        self.recompense = recompense
        self.replique = replique

    def choisir_action(self, cible, arene):
        # Règle simple : se protège quand il est mal en point, sinon joue selon le format
        if self.pv < self.stats_combat["resistance"] * 0.3 and random.random() < 0.5:
            return "proteger"
        if arene.format == "course":
            return random.choice(["foncer", "foncer", "attaquer"])
        return random.choice(["attaquer", "attaquer", "foncer", "proteger"])
