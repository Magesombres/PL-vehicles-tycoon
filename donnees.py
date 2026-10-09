"""Toutes les données du jeu. Ajouter un modèle ou une pièce = ajouter une ligne ici."""

import random

from commande import Commande
from pilotes import Adversaire
from vehicule import Modele, Piece, Vehicule

MODELES = {
    "voiture": Modele("Voiture", ["roue", "roue", "roue", "roue", "moteur", "chassis"]),
    "bateau": Modele("Bateau", ["moteur", "coque", "poste de pilotage"]),
    "avion": Modele("Avion", ["moteur", "ailes", "coque"]),
    "velo": Modele("velo", ["roue", "roue", "armature"]),
    "cyclo-moteur": Modele("Cyclo-moteur", ["moteur", "roue", "roue", "chassis"]),
    "33 tonnes": Modele("33 tonnes", ["moteur", "roue", "roue", "roue", "roue", "chassis"]),
    "roller": Modele("Roller", ["moteur", "roller", "roller", "roller", "roller", "roller", "roller", "roller", "roller", "chassis"]),
    "velo dit 'vin'": Modele("Vélo dit 'vin'", ["Moteur", "roue", "roue", "chassis", "gear", "gear"]),
}

CATALOGUE = [
    # Moteurs
    Piece("Moteur banane", "moteur", 5, {"puissance": 2, "vitesse": 5, "poids": 1}, ["banane"]),
    Piece("Moteur de tondeuse a cheveux", "moteur", 14, {"puissance": 6, "vitesse": 9, "poids": 3}),
    Piece("Moteur V8", "moteur", 80, {"puissance": 30, "vitesse": 30, "poids": 15}),
    Piece("Moteur V12", "moteur", 100, {"puissance": 40, "vitesse": 40, "poids": 20}),
    Piece("Moteur F1", "moteur", 200, {"puissance": 100, "vitesse": 100, "poids": 50}),
    Piece("Moteur fusée", "moteur", 600, {"puissance": 2000, "vitesse": 500, "poids": 400}, ["fusee"]),
    Piece("Moteur de trotinette", "moteur", 20, {"puissance": 10, "vitesse": 15, "poids": 5}),
    Piece("Moteur d'avion de chasse", "moteur", 300, {"puissance": 200, "vitesse": 200, "poids": 100}),
    Piece("Petit mais puissant", "moteur", 50, {"puissance": 20, "vitesse": 25, "poids": 10}),
    Piece("Mot 'teur'", "moteur", 70, {"puissance": 25, "vitesse": 30, "poids": 15}),
    Piece("Les gambettes du démon", "moteur", 999, {"puissance": 800, "vitesse": 666, "poids": 10}, ["demon"]),
    # Roues
    Piece("Roue caoutchouc", "roue", 10, {"vitesse": 5, "resistance": 5, "poids": 2}),
    Piece("Roue bambou", "roue", 4, {"vitesse": 8, "resistance": 1}),
    Piece("Chenilles", "roue", 40, {"vitesse": 1, "resistance": 25, "poids": 10}, ["chenilles"]),
    Piece("Roue en or", "roue", 100, {"vitesse": 20, "resistance": 10, "poids": 5}, ["or"]),
    Piece("Roller", "roue", 30, {"vitesse": 15, "resistance": 2, "poids": 1}),
    Piece("pneu carrée", "roue", 20, {"vitesse": 5, "resistance": 5, "poids": 3}, ["carré"]),
    Piece("Chenille (l'animal)", "roue", 15, {"vitesse": 2, "resistance": 10, "poids": 5}, ["chenille"]),
    Piece("les petites roues", "roue", 5, {"vitesse": 3, "resistance": 1, "poids": 1}, ["petit"]),
    Piece("roue arriere de l'avant ", "roue", 250, {"vitesse": 500, "resistance": 1000, "poids": 2}, ["arriere"]),
    Piece("roue arriere de l'arriere ", "roue", 250, {"vitesse": 1000, "resistance": 500, "poids": 2}, ["arriere"]),
    
    # Châssis
    Piece("Châssis bois", "chassis", 15, {"resistance": 20, "poids": 10}),
    Piece("Châssis acier", "chassis", 60, {"resistance": 60, "poids": 30}),
    Piece("Châssis carton", "chassis", 2, {"resistance": 3, "poids": 1}, ["carton"]),
    Piece("Coque Rhinoshield", "chassis", 200, {"resistance": 200, "poids": 100}, ["rhinoshield"]),
    Piece("chasse des scies", "chassis", 100, {"resistance": 50, "poids": 20}, ["scie"]),
    Piece("Sacré châssis", "chassis", 500, {"resistance": 500, "poids": 200}, ["sacré"]),
    Piece("Le chat sept", "chassis", 300, {"resistance": 666, "poids": 150}, ["chat"]),
    # Bateaux et avions
    Piece("Coque gonflable", "coque", 20, {"resistance": 15, "vitesse": 5, "poids": 3}),
    Piece("Coque titane", "coque", 150, {"resistance": 100, "poids": 40}),
    Piece("Poste de pilotage basique", "poste de pilotage", 20, {"vitesse": 10}),
    Piece("Ailes en papier", "ailes", 8, {"vitesse": 25, "resistance": 1}, ["papier"]),
    Piece("Ailes alu", "ailes", 80, {"vitesse": 60, "resistance": 20, "poids": 15}),
    Piece("Aile de poulet", "ailes", 5, {"vitesse": 10, "resistance": 1}, ["poulet"]),
    Piece("La coke", "ailes", 100, {"vitesse": 100, "resistance": 50, "poids": 20}, ["coke"]),

    # Armatures
    Piece("Armature en bois", "armature", 10, {"resistance": 15, "poids": 5}),
    Piece("Armature métallique", "armature", 50, {"resistance": 50, "poids": 20}),

    # Gears
    Piece("Turbo", "gear", 100, {"vitesse": 20, "poids": 5}),
    Piece("Canon", "gear", 300, {"puissance": 250, "poids": 50}),
    Piece("Bouclier", "gear", 200, {"resistance": 100, "poids": 30}),
    Piece("Ailerons", "gear", 150, {"vitesse": 15, "poids": 10}),
    Piece("Lance-flammes", "gear", 250, {"puissance": 200, "poids": 40}),
    Piece("Remorque", "gear", 80, {"resistance": 50, "poids": 20}),
    Piece("la barbe de gandalf", "gear", 500, {"resistance": 1024, "poids": 8}, ["barbe"]),
    Piece("joueur de lol main et pieds", "gear", 1000, {"puissance": 500, "vitesse": 500, "resistance": 500, "poids": 50}, ["lol"]),
    Piece("Sarbacane Papier", "gear", 50, {"puissance": 10, "vitesse": 5, "poids": 1}, ["sarbacane"]),
    
    # Divers
]


def piece(nom):
    """Renvoie une copie neuve de la pièce du catalogue portant ce nom."""
    for p in CATALOGUE:
        if p.nom == nom:
            return p.copie()
    raise KeyError(nom)


def creer_vehicule(modele, noms_pieces, nom=None):
    vehicule = Vehicule(MODELES[modele], nom)
    for nom_piece in noms_pieces:
        vehicule.poser(piece(nom_piece))
    return vehicule


def kit_de_depart():
    return [piece("Roue caoutchouc") for _ in range(4)] + [piece("Moteur banane"), piece("Châssis bois"), piece("Sarbacane Papier")]


# --- Adversaires -----------------------------------------------------------

def adversaire(cle):
    """Fabrique un adversaire neuf (véhicule et PV remis à zéro)."""
    fabriques = {
        "kevin": lambda: Adversaire(
            "Kévin du quartier",
            creer_vehicule("trottinette", ["Roue bambou", "Roue bambou", "Moteur banane"], "Trottinette tunée"),
            1, 40, "Ma banane est plus jaune que la tienne."),
        "mamie_turbo": lambda: Adversaire(
            "Mamie Turbo",
            creer_vehicule("voiture", ["Roue caoutchouc"] * 4 + ["Moteur de tondeuse", "Châssis bois"], "La Twingo de l'enfer"),
            2, 70, "De mon temps, on gagnait à pied !"),
        "robot": lambda: Adversaire(
            "Robot aspirateur rebelle",
            creer_vehicule("trottinette", ["Chenilles", "Chenilles", "Moteur V12"], "Roomba-X"),
            3, 120, "BIP. ASPIRATION DE TA DIGNITÉ EN COURS."),
        "gerard": lambda: Adversaire(
            "Gérard",
            creer_vehicule("voiture", ["Chenilles"] * 4 + ["Moteur V12", "Châssis acier"], "Monster Truck"),
            4, 250, "Mon truck mange des voitures au petit-déj."),
        "speedy": lambda: Adversaire(
            "Speedy Gonzalès Jr",
            creer_vehicule("voiture", ["Roue bambou"] * 4 + ["Moteur V12", "Châssis carton"], "Flèche en carton"),
            4, 200, "¡Ándale! Tu me vois ? Non ? Normal."),
        "moissonneuse": lambda: Adversaire(
            "Fermier Apocalyptique",
            creer_vehicule("voiture", ["Chenilles"] * 4 + ["Moteur V12", "Châssis acier"], "Moissonneuse de l'Apocalypse"),
            5, 400, "La récolte sera… TOI."),
        "douane": lambda: Adversaire(
            "Brigade des douanes volantes",
            creer_vehicule("avion", ["Moteur V12", "Ailes alu", "Coque titane"], "Avion de patrouille"),
            5, 300, "Contrôle de routine ! Vous transportez des bananes ?"),
    }
    return fabriques[cle]()


ADVERSAIRES_ARENE = ["kevin", "mamie_turbo", "robot", "gerard"]


def adversaires_arene():
    return [adversaire(cle) for cle in ADVERSAIRES_ARENE]


# --- Commandes libres (hors histoire) ------------------------------------------

def commande_aleatoire():
    modeles = [
        lambda: Commande("Un livreur de sushis", "Un bateau, n'importe lequel.", 70, modele="Bateau"),
        lambda: Commande("Le facteur", "Une voiture qui roule un peu.", 60,
                         modele="Voiture", stats_min={"vitesse": 30}),
        lambda: Commande("Un singe savant", "N'importe quoi, du moment qu'il y a une banane.", 40,
                         tags_requis=["banane"], bonus_tags={"banane": 20}),
        lambda: Commande("Un pilote du dimanche", "Un avion qui ne se plie pas.", 90,
                         modele="Avion", stats_min={"resistance": 20}, reputation={"C": 1}),
        lambda: Commande("Un fermier", "Un véhicule à chenilles pour son champ.", 200,
                         tags_requis=["chenilles"], reputation={"B": 1}),
        lambda: Commande("Un type en imper", "Une voiture en carton. Ne pose pas de questions.", 50,
                         modele="Voiture", tags_requis=["carton"], reputation={"D": 1}),
        lambda: Commande("Une fan de course", "Une voiture vraiment rapide.", 150,
                         modele="Voiture", stats_min={"vitesse": 50}, reputation={"A": 1}),
    ]
    return random.choice(modeles)()
