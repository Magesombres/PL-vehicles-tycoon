"""Membre 3 — Commande : un client, des exigences, une récompense."""


class Commande:
    def __init__(self, client, description, prix, modele=None, stats_min=None,
                 tags_requis=None, bonus_tags=None, reputation=None):
        self.client = client
        self.description = description
        self.prix = prix
        self.modele = modele                  # nom du modèle exigé, ou None
        self.stats_min = stats_min or {}      # ex. {"vitesse": 50}
        self.tags_requis = tags_requis or []  # ex. ["banane"]
        self.bonus_tags = bonus_tags or {}    # ex. {"banane": 20} $ par pièce taguée
        self.reputation = reputation or {}    # ex. {"D": 2}

    def verifier(self, vehicule):
        """Renvoie la liste des problèmes (vide si le véhicule convient)."""
        problemes = []
        if not vehicule.est_complet():
            problemes.append("le véhicule n'est pas terminé")
        if self.modele and vehicule.modele.nom != self.modele:
            problemes.append(f"il fallait un(e) {self.modele}")
        stats = vehicule.calculer_stats()
        for stat, mini in self.stats_min.items():
            if stats[stat] < mini:
                problemes.append(f"{stat} {stats[stat]} < {mini}")
        for tag in self.tags_requis:
            if tag not in vehicule.tags():
                problemes.append(f"il manque une pièce « {tag} »")
        return problemes

    def calculer_recompense(self, vehicule):
        """C'est la commande qui lit les tags : le bonus n'existe que pour elle."""
        total = self.prix
        for piece in vehicule.pieces:
            for tag in piece.tags:
                total += self.bonus_tags.get(tag, 0)
        return total

    def exigences(self):
        morceaux = []
        if self.modele:
            morceaux.append(self.modele)
        morceaux += [f"{stat} ≥ {mini}" for stat, mini in self.stats_min.items()]
        morceaux += [f"{tag} obligatoire" for tag in self.tags_requis]
        morceaux += [f"bonus {tag} +{bonus} $" for tag, bonus in self.bonus_tags.items()]
        return ", ".join(morceaux) or "aucune exigence"

    def resume(self):
        return f"{self.client} — « {self.description} » ({self.exigences()}) → {self.prix} $"
