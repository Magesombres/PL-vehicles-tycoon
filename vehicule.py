"""Membre 1 — Piece, Modele, Vehicule : catalogue, construction, calcul des stats."""

STATS = ("puissance", "vitesse", "resistance", "poids", "valeur")


class Piece:
    """Une pièce qui se pose dans un emplacement. Tous les cas tiennent dans les attributs."""

    def __init__(self, nom, emplacement, prix, bonus=None, tags=None):
        self.nom = nom
        self.emplacement = emplacement
        self.prix = prix
        self.bonus = bonus or {}
        self.tags = tags or []

    def copie(self):
        """La boutique vend des copies : chaque pièce achetée est un objet distinct."""
        return Piece(self.nom, self.emplacement, self.prix, dict(self.bonus), list(self.tags))

    def __str__(self):
        effets = ", ".join(f"{valeur:+} {stat}" for stat, valeur in self.bonus.items())
        tags = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"{self.nom} ({self.emplacement}) : {effets}{tags}"


class Modele:
    """Un type de véhicule = la liste de ses emplacements. Nouveau type = nouvel objet."""

    def __init__(self, nom, emplacements):
        self.nom = nom
        self.emplacements = emplacements


class Vehicule:
    RESISTANCE_DE_BASE = 10
    TAUX_REVENTE = 0.8

    def __init__(self, modele, nom=None):
        self.modele = modele
        self.nom = nom or modele.nom
        self.pieces = [None] * len(modele.emplacements)

    def prochain_emplacement(self):
        """Type du premier emplacement vide (None si le véhicule est complet)."""
        for emplacement, piece in zip(self.modele.emplacements, self.pieces):
            if piece is None:
                return emplacement
        return None

    def poser(self, piece):
        """Pose la pièce dans le premier emplacement libre compatible. Renvoie True si posée."""
        for i, emplacement in enumerate(self.modele.emplacements):
            if self.pieces[i] is None and emplacement == piece.emplacement:
                self.pieces[i] = piece
                return True
        return False

    def demonter(self):
        """Retire toutes les pièces et les renvoie."""
        pieces = [p for p in self.pieces if p is not None]
        self.pieces = [None] * len(self.pieces)
        return pieces

    def est_complet(self):
        return all(p is not None for p in self.pieces)

    def tags(self):
        return {tag for piece in self.pieces if piece for tag in piece.tags}

    def calculer_stats(self):
        stats = dict.fromkeys(STATS, 0)
        stats["resistance"] = self.RESISTANCE_DE_BASE
        prix_total = 0
        for piece in self.pieces:
            if piece is None:
                continue
            prix_total += piece.prix
            for stat, valeur in piece.bonus.items():
                stats[stat] += valeur
        # Le poids freine le véhicule
        stats["vitesse"] = max(1, stats["vitesse"] - stats["poids"] // 4)
        stats["valeur"] += int(prix_total * self.TAUX_REVENTE)
        return stats

    def fiche(self):
        lignes = [f"{self.nom} ({self.modele.nom})"]
        for emplacement, piece in zip(self.modele.emplacements, self.pieces):
            lignes.append(f"   - {emplacement:<18} : {piece.nom if piece else '(vide)'}")
        stats = self.calculer_stats()
        lignes.append("   " + " | ".join(f"{stat} {valeur}" for stat, valeur in stats.items()))
        return "\n".join(lignes)

    def __str__(self):
        return f"{self.nom} ({self.modele.nom})"
