"""Membre 2 — Arene : combat au tour par tour selon un format."""

from outils import titre


class Arene:
    FORMATS = {
        "combat": {"nom": "Combat", "boost": {"puissance": 2},
                   "victoire": "réduire la résistance adverse à 0"},
        "course": {"nom": "Course", "boost": {"vitesse": 2},
                   "victoire": "arriver le premier à 300 m"},
        "endurance": {"nom": "Endurance", "boost": {"resistance": 2},
                      "victoire": "tenir 6 tours"},
    }
    DISTANCE_COURSE = 300
    TOURS_ENDURANCE = 6
    TOURS_MAX = 30

    def __init__(self, format="combat"):
        self.format = format
        self.multiplicateurs = self.FORMATS[format]["boost"]

    def combattre(self, p1, p2):
        """p1 est le joueur. Renvoie le pilote gagnant, ou None en cas de match nul."""
        infos = self.FORMATS[self.format]
        titre(f"ARÈNE — {infos['nom']} : {p1.nom} VS {p2.nom}")
        print(f"Objectif : {infos['victoire']}.")
        if hasattr(p2, "replique"):
            print(f'{p2.nom} : « {p2.replique} »')
        p1.preparer_combat(self.multiplicateurs)
        p2.preparer_combat(self.multiplicateurs)

        for tour in range(1, self.TOURS_MAX + 1):
            print(f"\n--- Tour {tour} ---")
            self.afficher_etat(p1, p2)
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
        pilote.protege = False
        if action == "attaquer":
            degats = pilote.attaquer(cible)
            print(f"{pilote.nom} attaque ! {cible.nom} perd {degats} PV.")
        elif action == "foncer":
            degats = pilote.foncer(cible)
            print(f"{pilote.nom} fonce (+{pilote.stats_combat['vitesse']} m) "
                  f"et accroche {cible.nom} : -{degats} PV.")
        else:
            pilote.protege = True
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
