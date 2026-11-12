"""Petites fonctions d'affichage et de saisie partagées par tout le jeu."""

from couleurs import colorer


def titre(texte):
    """Affiche un titre de menu."""
    print("\n" + colorer(f"=== {texte} ===", "cyan", "gras"))


def thune(montant):
    """Un montant en dollars, en jaune."""
    return colorer(f"{montant} $", "jaune")


def barre(valeur, maxi, couleur=None, largeur=20):
    """Barre de progression [█████░░░░░] ; sans couleur imposée : vert, puis jaune, puis rouge."""
    ratio = max(0, min(1, valeur / maxi)) if maxi else 0
    pleins = round(ratio * largeur)
    if valeur > 0:
        pleins = max(1, pleins)  # il reste toujours un bloc tant que ce n'est pas à 0
    if couleur is None:
        couleur = "vert" if ratio > 0.5 else "jaune" if ratio > 0.25 else "rouge"
    return "[" + colorer("█" * pleins, couleur) + "░" * (largeur - pleins) + "]"


def demander_nombre(mini, maxi, invite="> "):
    """Redemande tant que le joueur ne tape pas un entier entre mini et maxi."""
    while True:
        reponse = input(invite).strip()
        if reponse.isdigit() and mini <= int(reponse) <= maxi:
            return int(reponse)
        print(colorer(f"Tape un nombre entre {mini} et {maxi}.", "rouge"))


def oui_non(question):
    """Pose une question fermée ; renvoie True pour oui."""
    while True:
        reponse = input(f"{question} (o/n) > ").strip().lower()
        if reponse in ("o", "oui"):
            return True
        if reponse in ("n", "non"):
            return False


def pause():
    """Attend que le joueur appuie sur Entrée."""
    input("(Entrée pour continuer)")
