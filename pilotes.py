"""Ethan V. — Pilote, Joueur, Adversaire."""

import random

import competences

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
        self.protection = 1  # diviseur des dégâts subis (1 = aucune protection)
        self.brulure = 0  # dégâts qui retombent automatiquement chaque tour
        self.capacite_utilisee = False  # pour les capacités à usage unique par combat

    def preparer_combat(self, multiplicateurs):
        """Calcule les stats de combat (boosts du format compris) et remet les PV au maximum."""
        stats = self.vehicule.calculer_stats()
        for stat, mult in multiplicateurs.items():
            stats[stat] *= mult
        self.stats_combat = stats
        self.pv = stats["resistance"]
        self.distance = 0
        self.protection = 1
        self.brulure = 0
        self.capacite_utilisee = False

    def choisir_action(self, cible, arene):
        """Redéfinie dans Joueur (clavier) et Adversaire (IA)."""
        raise NotImplementedError

    def capacite_disponible(self):
        """Capacité spéciale utilisable maintenant (tag, pièce, infos), ou None."""
        tag, piece, info = competences.capacite_combat(self.vehicule)
        if info is None:
            return None
        if info["limite"] and self.capacite_utilisee:
            return None
        return tag, piece, info

    def subir(self, degats, ignorer_protection=False):
        """Retire des PV (divisés par la protection) et renvoie les dégâts réellement subis."""
        if not ignorer_protection:
            degats //= self.protection
        degats = max(1, degats)
        self.pv = max(0, self.pv - degats)
        return degats

    def attaquer(self, cible):
        """Frappe la cible avec la puissance du véhicule, plus un peu de hasard."""
        return cible.subir(self.stats_combat["puissance"] + random.randint(0, 5))

    def foncer(self, cible):
        """Avance (utile en course) et percute un peu l'adversaire au passage."""
        self.distance += self.stats_combat["vitesse"]
        return cible.subir(self.stats_combat["vitesse"] // 4)


class Joueur(Pilote):
    """Le pilote contrôlé au clavier : thune, pièces, véhicules et réputation cachée."""

    def __init__(self, nom, argent=120):
        super().__init__(nom)
        self.argent = argent
        self.pieces = []
        self.vehicules = []
        self.reputation = {"A": 0, "B": 0, "C": 0, "D": 0}  # cachée au joueur

    def choisir_action(self, cible, arene):
        """Le joueur choisit son action au clavier."""
        capacite = self.capacite_disponible()
        invite = "1. Attaquer   2. Foncer   3. Se protéger"
        if capacite:
            invite += f"   4. {capacite[2]['nom']}"
        print(invite)
        while True:
            choix = input("> ").strip()
            if choix in ACTIONS:
                return ACTIONS[choix]
            if choix == "4" and capacite:
                return "capacite"
            print("Choix invalide.")

    def retirer_vehicule(self, vehicule):
        """Retire un véhicule (vendu, livré ou démonté) et change le véhicule actif si besoin."""
        self.vehicules.remove(vehicule)
        if self.vehicule is vehicule:
            self.vehicule = self.vehicules[0] if self.vehicules else None


class Adversaire(Pilote):
    """Un pilote contrôlé par l'IA, avec un niveau, une récompense et une réplique."""

    def __init__(self, nom, vehicule, niveau=1, recompense=50, replique="..."):
        super().__init__(nom, vehicule)
        self.niveau = niveau
        self.recompense = recompense
        self.replique = replique

    def choisir_action(self, cible, arene):
        """L'IA choisit son action toute seule."""
        # Règle simple : utilise sa capacité si dispo, se protège si mal en point, sinon selon le format
        if self.capacite_disponible() and random.random() < 0.4:
            return "capacite"
        if self.pv < self.stats_combat["resistance"] * 0.3 and random.random() < 0.5:
            return "proteger"
        if arene.format == "course":
            return random.choice(["foncer", "foncer", "attaquer"])
        return random.choice(["attaquer", "attaquer", "foncer", "proteger"])
