"""Membre 2 — Arene : combat au tour par tour selon un format."""

import random

from outils import titre

# Règles spéciales du format "event" : une est tirée au hasard à chaque arène.
# Seuls les véhicules portant une pièce avec ce tag reçoivent le boost.
EVENEMENTS = [
    {"nom": "Rush doré", "tag": "or", "boost": {"puissance": 2, "resistance": 2},
     "regle": "Les véhicules avec une pièce taguée 'or' sont 2x plus puissants et résistants."},
    {"nom": "Mode banane", "tag": "banane", "boost": {"vitesse": 3},
     "regle": "Les véhicules avec une pièce taguée 'banane' sont 3x plus rapides."},
    {"nom": "Chenilles enragées", "tag": "chenilles", "boost": {"puissance": 2, "resistance": 2},
     "regle": "Les véhicules à chenilles sont 2x plus puissants et résistants."},
    {"nom": "Nuit démoniaque", "tag": "demon", "boost": {"puissance": 3},
     "regle": "Les véhicules avec une pièce taguée 'demon' sont 3x plus puissants."},
]


class Arene:
    FORMATS = {
        "combat": {"nom": "Combat", "boost": {"puissance": 2},
                   "victoire": "réduire la résistance adverse à 0"},
        "course": {"nom": "Course", "boost": {"vitesse": 2},
                   "victoire": "arriver le premier à 300 m"},
        "endurance": {"nom": "Endurance", "boost": {"resistance": 2},
                      "victoire": "tenir 6 tours"},
        "event": {"nom": "Évènement", "boost": {},
                   "victoire": "réduire la résistance adverse à 0"},
    }
    DISTANCE_COURSE = 300
    TOURS_ENDURANCE = 6
    TOURS_MAX = 30

    def __init__(self, format="combat"):
        self.format = format
        self.evenement = random.choice(EVENEMENTS) if format == "event" else None
        self.multiplicateurs = self.evenement["boost"] if self.evenement else self.FORMATS[format]["boost"]

    def multiplicateurs_pour(self, pilote):
        """Les boosts de l'event ne s'appliquent qu'aux véhicules portant le tag demandé."""
        if self.evenement is None:
            return self.multiplicateurs
        if pilote.vehicule and self.evenement["tag"] in pilote.vehicule.tags():
            return self.multiplicateurs
        return {}

    def combattre(self, p1, p2):
        """p1 est le joueur. Renvoie le pilote gagnant, ou None en cas de match nul."""
        infos = self.FORMATS[self.format]
        titre(f"ARÈNE — {infos['nom']} : {p1.nom} VS {p2.nom}")
        print(f"Objectif : {infos['victoire']}.")
        if self.evenement:
            print(f"Règle du jour : {self.evenement['nom']} — {self.evenement['regle']}")
        if hasattr(p2, "replique"):
            print(f'{p2.nom} : « {p2.replique} »')
        p1.preparer_combat(self.multiplicateurs_pour(p1))
        p2.preparer_combat(self.multiplicateurs_pour(p2))

        for tour in range(1, self.TOURS_MAX + 1):
            print(f"\n--- Tour {tour} ---")
            self.afficher_etat(p1, p2)
            for pilote in (p1, p2):
                if pilote.brulure > 0:
                    degats = pilote.subir(pilote.brulure, ignorer_protection=True)
                    print(f"{pilote.nom} brûle : -{degats} PV.")
                    pilote.brulure -= 1
            gagnant = self.verifier_victoire(p1, p2)
            if gagnant:
                print(f"\n>>> {gagnant.nom} remporte le match !")
                return gagnant
            # Le plus rapide joue en premier
            ordre = sorted([p1, p2], key=lambda p: p.stats_combat["vitesse"], reverse=True)
            for pilote in ordre:
                cible = p2 if pilote is p1 else p1
                self.executer(pilote, cible, pilote.choisir_action(cible, self))
                gagnant = self.verifier_victoire(p1, p2)
                if gagnant:
                    print(f"\n>>> {gagnant.nom} remporte le match !")
                    return gagnant
            if self.format == "endurance" and tour >= self.TOURS_ENDURANCE:
                print(f"\n>>> {p1.nom} a tenu {tour} tours et remporte le match !")
                return p1
        print("\n>>> Tout le monde est fatigué. Match nul.")
        return None

    def executer(self, pilote, cible, action):
        pilote.protection = 1
        if action == "attaquer":
            degats = pilote.attaquer(cible)
            print(f"{pilote.nom} attaque ! {cible.nom} perd {degats} PV.")
        elif action == "foncer":
            degats = pilote.foncer(cible)
            print(f"{pilote.nom} fonce (+{pilote.stats_combat['vitesse']} m) "
                  f"et accroche {cible.nom} : -{degats} PV.")
        elif action == "capacite":
            tag, piece, info = pilote.capacite_disponible()
            print(info["effet"](pilote, cible))
        else:
            pilote.protection = 2
            print(f"{pilote.nom} se protège.")

    def verifier_victoire(self, p1, p2):
        if p2.pv <= 0:
            return p1
        if p1.pv <= 0:
            return p2
        if self.format == "course":
            for pilote in (p1, p2):
                if pilote.distance >= self.DISTANCE_COURSE:
                    return pilote
        return None

    def afficher_etat(self, p1, p2):
        for p in (p1, p2):
            ligne = f"{p.nom:<30} PV {p.pv}/{p.stats_combat['resistance']}"
            if self.format == "course":
                ligne += f"   Distance {p.distance}/{self.DISTANCE_COURSE} m"
            print(ligne)
