"""Mode admin : un menu de triche pour tester tout le jeu sans refaire chaque run à la main."""

import donnees
import histoire
from outils import demander_nombre, titre

THUNE_ADMIN = 100000
VOIES = [
    (None, "Tronc commun"),
    ("A", "Branche A — T1 (vitesse)"),
    ("B", "Branche B — Du sang ! (puissance)"),
    ("C", "Branche C — Science"),
    ("D", "Branche D — Livraison"),
    ("final", "Boss final secret"),
]


def menu(jeu):
    """Menu admin. Une action qui renvoie True referme le menu pour relancer l'histoire."""
    actions = [
        ("Voir l'état de la partie (réputation cachée comprise)", afficher_etat),
        (f"Recevoir {THUNE_ADMIN} $", donner_thune),
        ("Recevoir le véhicule ultime (il devient le véhicule actif)", donner_vehicule_ultime),
        ("Débloquer toutes les pièces de boss en boutique", debloquer_pieces_boss),
        ("Aller à une étape de l'histoire", aller_a_une_etape),
        ("Marquer les 4 fins comme obtenues (la prochaine fin lance le boss final)", marquer_les_fins),
        ("Affronter n'importe quel adversaire (boss compris)", affronter),
    ]
    while True:
        titre("MENU ADMIN")
        for i, (libelle, _) in enumerate(actions, 1):
            print(f"{i}. {libelle}")
        print("0. Retour au garage")
        choix = demander_nombre(0, len(actions))
        if choix == 0:
            return
        if actions[choix - 1][1](jeu):
            return


def afficher_etat(jeu):
    """Affiche ce que le joueur ne voit pas d'habitude."""
    print(f"Voie : {jeu.branche or 'tronc commun'}, étape {jeu.etape + 1}/{len(jeu.evenements)}")
    if jeu.etape < len(jeu.evenements):
        print(f"Étape en cours : {decrire(jeu.evenements[jeu.etape])}")
    if jeu.commande_histoire:
        print(f"Commande d'histoire à livrer : {jeu.commande_histoire.resume()}")
    print(f"Réputation : {jeu.joueur.reputation}")
    print(jeu.bilan())


def donner_thune(jeu):
    """Ajoute de la thune au joueur."""
    jeu.joueur.argent += THUNE_ADMIN
    print(f"+{THUNE_ADMIN} $. Thune : {jeu.joueur.argent} $")


def donner_vehicule_ultime(jeu):
    """Construit une MDL avec la meilleure pièce de chaque emplacement, Divinité comprise."""
    noms = [meilleure_piece(emplacement).nom for emplacement in donnees.MODELES["MDL"].emplacements]
    vehicule = donnees.creer_vehicule("MDL", noms, "Véhicule ultime")
    jeu.joueur.vehicules.append(vehicule)
    jeu.joueur.vehicule = vehicule
    print(vehicule.fiche())


def meilleure_piece(emplacement):
    """La pièce de cet emplacement qui donne le plus de stats de combat."""
    pieces = [p for p in donnees.CATALOGUE + donnees.PIECES_BOSS if p.emplacement == emplacement]
    return max(pieces, key=lambda p: sum(p.bonus.get(s, 0) for s in ("puissance", "vitesse", "resistance")))


def debloquer_pieces_boss(jeu):
    """Ajoute à la boutique toutes les pièces de boss pas encore débloquées."""
    nouvelles = [p.nom for p in donnees.PIECES_BOSS if p.nom not in jeu.trophees]
    jeu.trophees += nouvelles
    print(f"{len(nouvelles)} pièce(s) débloquée(s) en boutique.")


def aller_a_une_etape(jeu):
    """Saute à l'étape choisie. Renvoie True si l'histoire doit reprendre tout de suite."""
    for i, (_, nom) in enumerate(VOIES, 1):
        print(f"{i}. {nom}")
    print("0. Annuler")
    choix = demander_nombre(0, len(VOIES))
    if choix == 0:
        return False
    lettre = VOIES[choix - 1][0]
    evenements = histoire.branche(lettre) if lettre else histoire.tronc_commun()
    for i, evenement in enumerate(evenements, 1):
        print(f"{i}. {decrire(evenement)}")
    print("0. Annuler")
    etape = demander_nombre(0, len(evenements))
    if etape == 0:
        return False
    if jeu.commande_histoire:  # l'ancienne commande d'histoire n'a plus de raison d'être
        jeu.commandes.remove(jeu.commande_histoire)
        jeu.commande_histoire = None
    jeu.branche = lettre
    jeu.evenements = evenements
    jeu.etape = etape - 1
    return True


def decrire(evenement):
    """Le type et le titre d'un événement, sur une ligne."""
    return f"[{type(evenement).__name__.replace('Evenement', '')}] {evenement.titre}"


def marquer_les_fins(jeu):
    """Fait comme si les 4 branches étaient finies."""
    jeu.branches_finies = ["A", "B", "C", "D"]
    print("Les 4 fins sont marquées : le boss final se lancera à la prochaine fin de branche.")
    print("(Pour y aller tout de suite : « Aller à une étape de l'histoire ».)")


def affronter(jeu):
    """Ouvre l'arène avec tous les adversaires du jeu."""
    jeu.menu_arene(donnees.tous_les_adversaires())
