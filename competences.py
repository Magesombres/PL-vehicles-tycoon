"""Compétences spéciales débloquées par les pièces "gear" qui portent un tag connu.

Un véhicule n'active que la première compétence trouvée parmi ses pièces équipées
(dans l'ordre des emplacements). COMBAT regroupe les capacités utilisables en
arène (4e choix dans le menu de combat) ; UTILITAIRES décrit celles qui agissent
hors combat (boutique, commandes...), appliquées directement dans jeu.py.
"""


def _turbo(pilote, cible):
    gain = pilote.stats_combat["vitesse"] * 2
    pilote.distance += gain
    return f"{pilote.nom} enclenche le TURBO et avance de {gain} m !"


def _canon(pilote, cible):
    pilote.capacite_utilisee = True
    degats = cible.subir(pilote.stats_combat["puissance"] * 2)
    return f"{pilote.nom} tire au CANON ! {cible.nom} perd {degats} PV."


def _bouclier(pilote, cible):
    pilote.protection = 3
    return f"{pilote.nom} lève un BOUCLIER renforcé."


def _lance_flammes(pilote, cible):
    pilote.capacite_utilisee = True
    degats = cible.subir(pilote.stats_combat["puissance"])
    cible.brulure += max(1, degats // 5)
    return f"{pilote.nom} balance un jet de FLAMMES ! {cible.nom} perd {degats} PV et prend feu."


def _sarbacane(pilote, cible):
    degats = cible.subir(5, ignorer_protection=True)
    return f"{pilote.nom} tire à la SARBACANE : {cible.nom} perd {degats} PV (ça passe toujours)."


def _barbe(pilote, cible):
    pilote.capacite_utilisee = True
    soin = max(1, pilote.stats_combat["resistance"] // 5)
    pilote.pv = min(pilote.stats_combat["resistance"], pilote.pv + soin)
    return f"{pilote.nom} invoque la BARBE DE GANDALF et regagne {soin} PV."


# tag -> {nom affiché, effet (pilote, cible) -> message, limite = usage unique par combat}
COMBAT = {
    "turbo": {"nom": "Turbo", "effet": _turbo, "limite": False},
    "canon": {"nom": "Canon", "effet": _canon, "limite": True},
    "bouclier": {"nom": "Bouclier renforcé", "effet": _bouclier, "limite": False},
    "flammes": {"nom": "Lance-flammes", "effet": _lance_flammes, "limite": True},
    "sarbacane": {"nom": "Sarbacane", "effet": _sarbacane, "limite": False},
    "barbe": {"nom": "Barbe de Gandalf", "effet": _barbe, "limite": True},
}

# tag -> description (purement informatif, l'effet est appliqué directement dans jeu.py)
UTILITAIRES = {
    "remorque": "+1 commande libre disponible en même temps.",
    "lol": "Réputation doublée à la livraison.",
}


def capacite_combat(vehicule):
    """(tag, pièce, info) de la 1ère compétence de combat équipée, sinon (None, None, None)."""
    if vehicule is None:
        return None, None, None
    for piece in vehicule.pieces:
        if piece is None:
            continue
        for tag in piece.tags:
            if tag in COMBAT:
                return tag, piece, COMBAT[tag]
    return None, None, None


def a_la_competence(vehicule, tag):
    """Le véhicule a-t-il une pièce équipée portant ce tag ?"""
    if vehicule is None:
        return False
    return any(piece is not None and tag in piece.tags for piece in vehicule.pieces)
