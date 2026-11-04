"""Sauvegardes : 5 emplacements, un fichier JSON par emplacement (dossier sauvegardes/)."""

import json
import os

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sauvegardes")
NB_EMPLACEMENTS = 5


def chemin(emplacement):
    """Chemin du fichier JSON d'un emplacement."""
    return os.path.join(DOSSIER, f"emplacement_{emplacement}.json")


def lire(emplacement):
    """Renvoie le contenu de la sauvegarde, ou None si l'emplacement est vide ou illisible."""
    try:
        with open(chemin(emplacement), encoding="utf-8") as fichier:
            return json.load(fichier)
    except (OSError, ValueError):
        return None


def ecrire(emplacement, donnees):
    """Écrit la sauvegarde (crée le dossier si besoin)."""
    os.makedirs(DOSSIER, exist_ok=True)
    with open(chemin(emplacement), "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, ensure_ascii=False, indent=2)


def effacer(emplacement):
    """Supprime la sauvegarde de cet emplacement."""
    if os.path.exists(chemin(emplacement)):
        os.remove(chemin(emplacement))


def resume(donnees):
    """Une ligne pour le menu principal."""
    if donnees is None:
        return "(vide)"
    joueur = donnees["joueur"]
    fins = len(donnees["branches_finies"])
    final = " + boss final" if donnees["final_battu"] else ""
    return (f"{joueur['nom']} — {donnees['runs_finies']} run(s) faite(s) — fins {fins}/4{final} — "
            f"{len(donnees['trophees'])} trophée(s) — {joueur['argent']} $")
