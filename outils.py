"""Petites fonctions d'affichage et de saisie partagées par tout le jeu."""


def titre(texte):
    print(f"\n=== {texte} ===")


def demander_nombre(mini, maxi, invite="> "):
    """Redemande tant que le joueur ne tape pas un entier entre mini et maxi."""
    while True:
        reponse = input(invite).strip()
        if reponse.isdigit() and mini <= int(reponse) <= maxi:
            return int(reponse)
        print(f"Tape un nombre entre {mini} et {maxi}.")


def oui_non(question):
    while True:
        reponse = input(f"{question} (o/n) > ").strip().lower()
        if reponse in ("o", "oui"):
            return True
        if reponse in ("n", "non"):
            return False


def pause():
    input("(Entrée pour continuer)")
