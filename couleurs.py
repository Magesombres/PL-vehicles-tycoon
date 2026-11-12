"""Couleurs du terminal (codes ANSI), qu'on peut couper depuis le menu principal."""

import os
import sys

CODES = {"rouge": "31", "vert": "32", "jaune": "33", "bleu": "34", "violet": "35", "cyan": "36", "gras": "1"}

# Allumées seulement dans un vrai terminal : IDLE ou une sortie redirigée afficheraient les codes bruts.
actives = sys.stdout.isatty() and "idlelib" not in sys.modules

if os.name == "nt":
    os.system("")  # active les codes couleur dans le terminal Windows


def colorer(texte, *styles):
    """Entoure le texte des codes couleur demandés (ex. colorer("Boss", "violet", "gras"))."""
    if not actives:
        return str(texte)
    codes = ";".join(CODES[style] for style in styles)
    return f"\033[{codes}m{texte}\033[0m"
