"""Toutes les données du jeu. Ajouter un modèle ou une pièce = ajouter une ligne ici."""

import random

from commande import Commande
from pilotes import Adversaire
from vehicule import Modele, Piece, Vehicule

MODELES = {
    "voiture": Modele("Voiture", ["roue", "roue", "roue", "roue", "moteur", "chassis"]),
    "bateau": Modele("Bateau", ["moteur", "coque", "poste de pilotage"]),
    "avion": Modele("Avion", ["moteur", "ailes", "coque"]),
    "velo": Modele("Vélo", ["roue", "roue", "armature"]),
    "cyclo-moteur": Modele("Cyclo-moteur", ["moteur", "roue", "roue", "chassis"]),
    "33 tonnes": Modele("33 tonnes", ["moteur", "roue", "roue", "roue", "roue", "chassis"]),
    "roller": Modele("Roller", ["moteur", "roue", "roue", "roue", "roue", "roue", "roue", "roue", "roue", "chassis"]),
    "velo dit 'vin'": Modele("Vélo dit 'vin'", ["moteur", "roue", "roue", "chassis", "gear", "gear"]),
    "trottinette": Modele("Trottinette", ["roue", "roue", "moteur"]),
    "bouc": Modele("Le bouc à Bezard", ["chassis", "chassis", "roue", "roue", "roue", "roue", "gear", "gear"]),
    "MDL": Modele("MDL", ["moteur", "roue", "roue", "chassis", "core", "Divinity", "gear", "gear", "gear"]),
    "treu-treu": Modele("Treu-treu", ["moteur", "ailes", "coque"]),
    "costard-cravate": Modele("Costard-cravate", ["moteur", "chassis", "gear"]),
    "covid-truck": Modele("Covid-truck", ["roue", "roue", "roue", "roue", "moteur", "chassis", "gear", "gear", "gear"]),
}

# Pièces vendues à la boutique
CATALOGUE = [
    # Moteurs
    Piece("Moteur banane", "moteur", 5, {"puissance": 2, "vitesse": 5, "poids": 1}, ["banane"]),
    Piece("Moteur de tondeuse a cheveux", "moteur", 14, {"puissance": 6, "vitesse": 9, "poids": 3}),
    Piece("Moteur V8", "moteur", 80, {"puissance": 30, "vitesse": 30, "poids": 15}),
    Piece("Moteur V12", "moteur", 100, {"puissance": 40, "vitesse": 40, "poids": 20}),
    Piece("Moteur F1", "moteur", 200, {"puissance": 100, "vitesse": 100, "poids": 50}),
    Piece("Moteur fusée", "moteur", 1500, {"puissance": 2000, "vitesse": 500, "poids": 400}, ["fusee"]),
    Piece("Moteur de trottinette", "moteur", 20, {"puissance": 10, "vitesse": 15, "poids": 5}),
    Piece("Moteur d'avion de chasse", "moteur", 300, {"puissance": 200, "vitesse": 200, "poids": 100}),
    Piece("Petit mais puissant", "moteur", 50, {"puissance": 20, "vitesse": 25, "poids": 10}),
    Piece("Mot 'teur'", "moteur", 70, {"puissance": 25, "vitesse": 30, "poids": 15}),
    Piece("le smeg-moteur", "moteur", 250, {"puissance": 150, "vitesse": 150, "poids": 60}, ["smeg"]),
    # Roues
    Piece("Roue caoutchouc", "roue", 10, {"vitesse": 5, "resistance": 5, "poids": 2}),
    Piece("Roue bambou", "roue", 4, {"vitesse": 8, "resistance": 1}),
    Piece("Chenilles", "roue", 40, {"vitesse": 1, "resistance": 25, "poids": 10}, ["chenilles"]),
    Piece("Roue en or", "roue", 100, {"vitesse": 20, "resistance": 10, "poids": 5}, ["or"]),
    Piece("Roller", "roue", 30, {"vitesse": 15, "resistance": 2, "poids": 1}),
    Piece("pneu carré", "roue", 20, {"vitesse": 5, "resistance": 5, "poids": 3}, ["carré"]),
    Piece("Chenille (l'animal)", "roue", 15, {"vitesse": 2, "resistance": 10, "poids": 5}, ["chenille"]),
    Piece("les petites roues", "roue", 5, {"vitesse": 3, "resistance": 1, "poids": 1}, ["petit"]),
    Piece("smeg-roue", "roue", 60, {"vitesse": 30, "resistance": 30, "poids": 5}, ["smeg"]),

    # Châssis
    Piece("Châssis bois", "chassis", 15, {"resistance": 20, "poids": 10}),
    Piece("Châssis acier", "chassis", 60, {"resistance": 60, "poids": 30}),
    Piece("Châssis carton", "chassis", 2, {"resistance": 3, "poids": 1}, ["carton"]),
    Piece("Coque Rhinoshield", "chassis", 200, {"resistance": 200, "poids": 100}, ["rhinoshield"]),
    Piece("chasse des scies", "chassis", 100, {"resistance": 50, "poids": 20}, ["scie"]),
    Piece("Sacré châssis", "chassis", 500, {"resistance": 500, "poids": 200}, ["sacré"]),
    Piece("smeg-chassis", "chassis", 150, {"resistance": 150, "poids": 50}, ["smeg"]),
    # Bateaux et avions
    Piece("Coque gonflable", "coque", 20, {"resistance": 15, "vitesse": 5, "poids": 3}),
    Piece("Coque titane", "coque", 150, {"resistance": 100, "poids": 40}),
    Piece("Poste de pilotage basique", "poste de pilotage", 20, {"vitesse": 10}),
    Piece("Ailes en papier", "ailes", 8, {"vitesse": 25, "resistance": 1}, ["papier"]),
    Piece("Ailes alu", "ailes", 80, {"vitesse": 60, "resistance": 20, "poids": 15}),
    Piece("Aile de poulet", "ailes", 5, {"vitesse": 10, "resistance": 1}, ["poulet"]),
    Piece("La coke", "coque", 100, {"vitesse": 100, "resistance": 50, "poids": 20}, ["coke"]),

    # Armatures
    Piece("Armature en bois", "armature", 10, {"resistance": 15, "poids": 5}),
    Piece("Armature métallique", "armature", 50, {"resistance": 50, "poids": 20}),

    # Gears
    Piece("Turbo", "gear", 100, {"vitesse": 20, "poids": 5}, ["turbo"]),
    Piece("Canon", "gear", 300, {"puissance": 250, "poids": 50}, ["canon"]),
    Piece("Bouclier", "gear", 200, {"resistance": 100, "poids": 30}, ["bouclier"]),
    Piece("Ailerons", "gear", 150, {"vitesse": 15, "poids": 10}),
    Piece("Lance-flammes", "gear", 250, {"puissance": 200, "poids": 40}, ["flammes"]),
    Piece("Remorque", "gear", 80, {"resistance": 50, "poids": 20}, ["remorque"]),
    Piece("Sarbacane Papier", "gear", 50, {"puissance": 10, "vitesse": 5, "poids": 1}, ["sarbacane"]),
    Piece("la barbe de gandalf", "gear", 500, {"resistance": 1024, "poids": 8}, ["barbe"]),
    Piece("joueur de lol main et pieds", "gear", 1000, {"puissance": 500, "vitesse": 500, "resistance": 500, "poids": 50}, ["lol"]),
]

# Pièces signature des boss : introuvables en boutique
PIECES_BOSS = [
    # Arnaud
    Piece("Les gambettes du démon", "moteur", 999, {"puissance": 666, "vitesse": 333, "poids": 10}, ["demon"]),
    Piece("roue arriere de l'avant", "roue", 250, {"vitesse": 50, "resistance": 1000, "poids": 2}, ["arriere"]),
    Piece("roue arriere de l'arriere", "roue", 250, {"vitesse": 100, "resistance": 500, "poids": 2}, ["arriere"]),
    Piece("Le chat sept", "chassis", 300, {"resistance": 666, "poids": 150}, ["chat"]),
    # Bezard
    Piece("rn", "roue", 80, {"puissance": 30, "vitesse": 10, "poids": 10}),
    Piece("lfi", "roue", 80, {"puissance": 30, "vitesse": 10, "poids": 10}),
    Piece("ecologiste les vert", "roue", 80, {"puissance": 30, "vitesse": 10, "poids": 10}),
    Piece("en marche", "roue", 80, {"puissance": 30, "vitesse": 10, "poids": 10}),
    Piece("la calvitie du démon", "chassis", 50, {"resistance": 4000, "poids": 0}, ["demon"]),
    Piece("le bus de Staline", "chassis", 300, {"resistance": 9000, "poids": 150}),
    Piece("barbe rousse", "gear", 40, {"resistance": 15, "poids": 3}),
    Piece("le communisme", "gear", 500, {"puissance": 450, "resistance": 1917, "poids": 20}),
    # Professeur Raoult
    Piece("roue du destin", "roue", 300, {"vitesse": 100, "resistance": 1000, "poids": 5}, ["destin"]),
    Piece("moteur confiné", "moteur", 3000, {"puissance": 400, "vitesse": 500, "poids": 50}),
    Piece("chassis médical", "chassis", 3000, {"resistance": 8000, "poids": 100}),
    Piece("raconter n'importe quoi", "gear", 500, {"puissance": 200, "poids": 5}),
    Piece("le test pcr", "gear", 500, {"resistance": 800, "poids": 5}, ["bouclier"]),
    Piece("doc de wish", "gear", 500, {"vitesse": 50, "poids": 1}),
    # Bally Bagayoko
    Piece("la force du titan", "moteur", 5000, {"puissance": 350, "vitesse": 1200, "poids": 100}),
    Piece("retenir les foules", "chassis", 5000, {"resistance": 12000, "poids": 200}),
    Piece("transport de poubelles enflammées", "gear", 3000, {"puissance": 150, "poids": 50}, ["flammes"]),
    # Vénère julien (MDL)
    Piece("moteur 67D", "moteur", 6700, {"puissance": 167, "vitesse": 667, "poids": 76}, ["Boss finale"]),
    Piece("chenilles Max", "roue", 999999, {"vitesse": 400, "resistance": 1000, "poids":-7}),
    Piece("armature en Lonsdaléite", "chassis", 9999999999, {"resistance": 6767, "poids":999}),
    Piece("Heart of the machine", "core", 99999999, {"puissance": 200, "resistance": 4000}),
    Piece("Divinité Suprême", "Divinity", 99999999, {"vitesse": 256, "puissance": 256, "resistance": 2000}),
    Piece("MDL suprême", "gear", 9999999, {"puissance": 100, "vitesse": 300, "poids": 11}, ["MDL"]),
    Piece("Grand chef suprême", "gear", 99999, {"puissance": 44, "vitesse": 312}, ["GCS"]),
    # Pièce ultime : offerte une seule fois, à la première victoire contre Vénère julien
    Piece("Divinité", "gear", 999999, {"puissance": 99999, "vitesse": 623994}, ["DIVIN"]),
    Piece("Infinité", "gear", 9999999, {"resistance": 1990}, ["INFINI"]),
]


def piece(nom):
    """Renvoie une copie neuve de la pièce (boutique ou boss) portant ce nom."""
    for p in CATALOGUE + PIECES_BOSS:
        if p.nom == nom:
            return p.copie()
    raise KeyError(nom)


def creer_vehicule(modele, noms_pieces, nom=None):
    """Construit un véhicule à partir d'une clé de MODELES et d'une liste de noms de pièces."""
    vehicule = Vehicule(MODELES[modele], nom)
    for nom_piece in noms_pieces:
        vehicule.poser(piece(nom_piece))
    return vehicule


def cle_modele(modele):
    """Clé de MODELES correspondant à cet objet Modele (pour la sauvegarde)."""
    for cle, m in MODELES.items():
        if m is modele:
            return cle
    raise KeyError(modele.nom)


def est_piece_boss(nom):
    """La pièce de ce nom est-elle réservée aux boss ?"""
    return any(p.nom == nom for p in PIECES_BOSS)


def kit_de_depart():
    """Les pièces offertes au début de chaque run."""
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
            creer_vehicule("voiture", ["Roue caoutchouc"] * 4 + ["Moteur de tondeuse a cheveux", "Châssis bois"], "La Twingo de l'enfer"),
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
        "lisa": lambda: Adversaire(
            "La Lisa mobile",
            creer_vehicule("33 tonnes", ["Moteur de trottinette"] + ["pneu carré"] * 4 + ["Coque Rhinoshield"], "indescamion"),
            3, 67, "Je sais pas ça dépend pourquoi j'ai tué la personne"),
        "julien": lambda: Adversaire(
            "Ride a bike",
            creer_vehicule("cyclo-moteur", ["Moteur d'avion de chasse"] + ["Chenille (l'animal)"] * 2 + ["chasse des scies"], "Le cyclo-démonteur"),
            6, 700, "Qui pisse face au vent s'en rince les dents"),
        "etham": lambda: Adversaire(
            "La coulombie",
            creer_vehicule("roller", ["Petit mais puissant"] + ["les petites roues"] * 8 + ["Sacré châssis"], "Lauralleur"),
            2, 100, "Tout pour les states"),
        "crombez": lambda: Adversaire(
            "la treu-treu 3000",
            creer_vehicule("treu-treu", ["Mot 'teur'", "Aile de poulet", "La coke"], "LA treu-treu a la colique"),
            8, 587, "Avec le linge les cours et les repas j'ai quand même le temps de te battre"),
        "Arnaud": lambda: Adversaire(
            "Le vélo sacré de Mr Arnaud",
            creer_vehicule("velo dit 'vin'", ["Les gambettes du démon", "roue arriere de l'avant","roue arriere de l'arriere", "Le chat sept","la barbe de gandalf","joueur de lol main et pieds"], "c'est mon destrier c'est tout"),
            11, 10000000, "C'est normal que ca marche pas ça à pas de pieds"),
        "Bezard": lambda: Adversaire(
            "LE bouc à Bezard",
            creer_vehicule("bouc", ["la calvitie du démon", "lfi","rn","ecologiste les vert","en marche", "barbe rousse","le bus de Staline","le communisme"], "le saint graal"),
            11, 19391945, "Je vais te prendre comme j'ai pris la Bastille"),
        "smegma": lambda: Adversaire(
            "LA smeg-mobile",
            creer_vehicule("voiture", ["smeg-roue"] * 4 + ["le smeg-moteur", "smeg-chassis"], "La polo 5 de zinzin"),
            7, 800, "Merci pour seub"),
        "Bally Bagayoko": lambda: Adversaire(
            "La blocus-mobile",
            creer_vehicule("costard-cravate", ["la force du titan","transport de poubelles enflammées","retenir les foules"], "les rots du peuples"),
            11, 64000000, "ARRETEZ!!!! RECULEZ!!!"),
        "Professeur Raoult": lambda: Adversaire(
            "Covid-truck",
            creer_vehicule("covid-truck", ["roue du destin"] * 4 + ["moteur confiné", "chassis médical", "raconter n'importe quoi", "le test pcr", "doc de wish"]),
            11, 7100000, "l'Hydroxychloroquine c'est bien"),
        "rapido-man": lambda: Adversaire(
            "rapido-man",
            creer_vehicule("roller", ["Moteur de tondeuse a cheveux"] + ["Roller"] * 8 + ["Châssis carton"], "roulette-rider"),
            1, 20, "La justice arrive sur des petites roues"),
        "ingénium": lambda: Adversaire(
            "tenia ida",
            creer_vehicule("roller", ["Moteur V8"] + ["Roue caoutchouc"] * 8 + ["Châssis acier"], "Le délégay des héros"),
            3, 140, "Ingenium. C'est le nom du héros qui va te vaincre !"),
        "sonic": lambda: Adversaire(
            "le hérisson bleu",
            creer_vehicule("trottinette", ["Roue en or","pneu carré","Moteur F1"], "Blue trot"),
            5, 500, "Faut que je speed!!!"),
        "Flash": lambda: Adversaire(
            "L'éclair rouge",
            creer_vehicule("bateau", ["Moteur fusée","Coque titane","Poste de pilotage basique"], "Flaship"),
            7, 700, " Je m'appelle Barry Allen et je suis l'homme le plus rapide du monde !"),
         "Usain Bolt": lambda: Adversaire(
            "L'éclair noir",
            creer_vehicule("avion", ["Moteur d'avion de chasse","Aile de poulet","Coque titane"], "La menace noire"),
            9, 900, " Wakanda Foreeeeeeveeeeeeeer !"),
        "flash mcqueen": lambda: Adversaire(
            "le rookie",
            creer_vehicule("voiture", ["Roue en or"] * 4 + ["Moteur fusée", "Coque Rhinoshield"], "vrouum vrouum"),
            10, 1000, " Katchaoww"),
        "Saddam Hussein Al-Majid": lambda: Adversaire(
            "Le boucher de Bagdad",
            creer_vehicule("33 tonnes", ["Moteur fusée"] + ["Roue en or"] * 4 + ["Coque Rhinoshield"], "Le palais roulant"),
            10, 1000, "Même mes jantes sont en or. Et toi, t'as quoi ?"),


        #Boss finale secréte
        "Vénère julien": lambda: Adversaire(
            "S'est fait N**é a la MDL",
            creer_vehicule("MDL", ["moteur 67D"] + ["chenilles Max"] * 2 + ["armature en Lonsdaléite", "Heart of the machine", "Divinité Suprême", "MDL suprême", "Infinité", "Grand chef suprême"], "La MDL de la mort qui tue"),
            67, 676767676, "SIX... SEEEEPT !"),
        
    }
    return fabriques[cle]()


# Triés par niveau. Les boss de branche et le boss final n'y sont pas.
ADVERSAIRES_ARENE = ["rapido-man", "kevin", "mamie_turbo", "robot", "ingénium", "gerard",
                     "sonic", "Flash", "Usain Bolt", "flash mcqueen", "Saddam Hussein Al-Majid"]
# Ceux de l'histoire, pour le mode admin.
ADVERSAIRES_HISTOIRE = ["etham", "lisa", "speedy", "douane", "moissonneuse", "julien", "smegma", "crombez",
                        "Arnaud", "Bezard", "Professeur Raoult", "Bally Bagayoko", "Vénère julien"]


def adversaires_arene():
    """Les adversaires de l'arène libre, recréés à neuf."""
    return [adversaire(cle) for cle in ADVERSAIRES_ARENE]


def tous_les_adversaires():
    """Tous les adversaires du jeu, boss compris, recréés à neuf (mode admin)."""
    return [adversaire(cle) for cle in ADVERSAIRES_ARENE + ADVERSAIRES_HISTOIRE]


# --- Commandes libres (hors histoire) ------------------------------------------

def commande_aleatoire():
    """Tire au hasard une commande libre (hors histoire)."""
    modeles = [
        lambda: Commande("Un livreur de sushis", "Un bateau, n'importe lequel.", 70, modele="Bateau"),
        lambda: Commande("Le facteur", "Une voiture qui roule un peu.", 60,
                         modele="Voiture", stats_min={"vitesse": 30}),
        lambda: Commande("Un singe savant", "N'importe quoi, du moment qu'il y a une banane.", 20,
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
