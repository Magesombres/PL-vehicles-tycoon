"""Contenu de l'histoire : tronc commun, puis 4 branches (A, B, C, D) et leurs fins.

Chaque fonction crée des objets neufs à chaque appel.
"""

from arene import Arene
from commande import Commande
from donnees import adversaire
from evenements import EvenementChoix, EvenementCombat, EvenementCommande

INTRO = """
Tu as 17 ans. Tes journées : Minecraft, pignouf, pignoufff.
Un matin, tes parents te dégagent de la maison et te donnant 1 carton.
4 roues, 1 moteur.
Le chassis ? avec le carton. Une arme : Avec le papier journal.
Tu a toujours rêvé de construire des véhicules. Tu n'a jamais réflechie a les faire rouler.
« Tu veux manger ? Construis des trucs et vends-les. Bisous. »
La porte se referme. Ton garage, c'est dehors
Objectif : GAGNER UN MAX DE THUNE.
"""

def tronc_commun():
    return [
        EvenementChoix(
            "Dehors !",
            "Tu regardes ton carton de pièces. Comment construire ton premier véhicules ?",
            [
                ("Construire un truc qui va VITE. Mais t'a pas de frein. tant pis c'est pas toi qui roulera avec", {"reputation": {"A": 1}}),
                ("Construire un truc qui fait MAL. De toute facon il tapera pas sur toi.", {"reputation": {"B": 1}}),
                ("Lire le manuel. Il y a un manuel ?", {"reputation": {"C": 1}}),
                ("Demander du boulot au voisin louche.", {"reputation": {"D": 1}, "argent": 10,
                                                          "message": "Il te glisse 10 $ « pour plus tard »."}),
            ],
        ),
        EvenementCommande(
            "Premier client",
            "Mamie Josette toque à la cabane. Elle veut une voiture « solide, parce qu'elle conduis mal ».\n (ca se voyait a sa tête après...)\n",
            "Elle a l'air de beaucoup aimer les bananes.",
            Commande("Mamie Josette", "Une voiture solide pour aller au marché.", 60,
                     modele="Voiture", stats_min={"resistance": 30}, bonus_tags={"banane": 10},
                     reputation={"C": 1}),
        ),
        EvenementChoix(
            "Le voisin louche",
            "Le voisin te tend un colis qui fait un léger bruit de glouglou.\n« Tu le livres à l'autre bout de la ville ? 30 $. »",
            [
                ("Accepter sans poser de question. Il te faut de l'argent.", {"reputation": {"D": 2}, "argent": 30}),
                ("Demander si ça explose. Tu le donneras au autres.", {"reputation": {"B": 2},
                                              "message": "« Seulement si tu le secoues. » Intéressant."}),
                ("Analyser le liquide d'abord. Qui sait ? Ca pourrait être un bon carburant.", {"reputation": {"C": 2},
                                                   "message": "C'est du jus de banane fermenté. Fascinant."}),
                ("Le livrer en 4 minutes chrono. Top départ.", {"reputation": {"A": 2}, "argent": 30}),
            ],
        ),
        EvenementCombat(
            "Le caïd du quartier",
            "Kévin, 17 ans, roi autoproclamé du quartier, bloque la sortie de ton garage.\n"
            "« Ici, on règle tout à l'arène. »",
            adversaire("kevin"), Arene("combat"),
        ),
        EvenementChoix(
            "La grande question",
            "Kévin, vaincu, te pose une question très philosophique : « Mais tu veux devenir QUOI, au juste ? »",
            [
                ("Le plus rapide de l'univers.", {"reputation": {"A": 3}}),
                ("Le plus destructeur de l'univers.", {"reputation": {"B": 3}}),
                ("Le plus savant de l'univers.", {"reputation": {"C": 3}}),
                ("J'y ait pas réflechie.", {"reputation": {"D": 3}}),
            ],
        ),
    ]


def branche(lettre):
    return {"A": branche_a, "B": branche_b, "C": branche_c, "D": branche_d}[lettre]()


def branche_a():
    """A — T1 : vitesse."""
    return [
        EvenementCommande(
            "Pizza Turbo",
            "Luigi veut livrer ses pizzas encore chaudes… en Italie. Depuis ici.",
            Commande("Luigi, pizzaïolo pressé", "Une voiture qui va très vite.", 220,
                     modele="Voiture", stats_min={"vitesse": 120}, reputation={"A": 1}),
        ),
        EvenementCombat(
            "Le roi de la vitesse",
            "Speedy Gonzalès Jr t'a vu livrer Luigi. Il exige une course. Tout de suite.",
            adversaire("speedy"), Arene("course"),
        ),
        EvenementChoix(
            "Le mur du son",
            "T'a allumé ton moteur et avec tes conneries tout devient blanc.\nTu viens de passer le mur du son. Derrière, un panneau :\n« Mur de la lumière — 3 km ».",
            [
                ("Accélérer.", {"message": "Évidemment."}),
                ("Accélérer, mais en criant.", {"message": "Personne ne t'entend : tu vas trop vite."}),
                ("Vendre des photos du panneau.", {"argent": 100, "message": "Les touristes adorent. +100 $"}),
            ],
        ),
        EvenementCommande(
            "Le dernier client",
            "Un physicien essoufflé : « J'ai besoin d'une voiture plus rapide que… tout. Pour la science. »",
            Commande("Un physicien essoufflé", "Une voiture absurdement rapide.", 1000,
                     modele="Voiture", stats_min={"vitesse": 300}),
        ),
        EvenementChoix(
            "Une limite a la vitesse ?",
            "Pour toi, aucune limite à la vitesse. Mais pour la physique, si. Tu viens de passer le mur de la lumière.\n",
            [
                ("Bah tu vois rien ducoup", {"message": "Évidemment."}),
                ("Mais si tu vois,... de la lumière", {"message": "Enfin physyquement, tu vois rien. Mais tu est sur de voir de la lumière."}),
                ("Prends des notes", {"argent": 100, "message": "Tu vendras ta recherche +100 $"}),
            ],
        ),
        EvenementCombat(
            "Le mur de la vitesse",
            "Dans la lumière tu le vois descendre... devant toi il se tient, L'ultime MUR, Tu le défie sans hésiter",
            adversaire("Arnaud"), Arene("course"),
        )
    ]


def branche_b():
    """B — Du sang ! : puissance."""
    return [
        EvenementCombat(
            "Le Monster Truck",
            "Gérard a entendu parler de toi. Son Monster Truck a faim.",
            adversaire("gerard"), Arene("combat"),
        ),
        EvenementCommande(
            "Le général Patate",
            "Un général à moustache veut « un char. Un vrai. Avec des chenilles. Et du muscle. »",
            Commande("Général Patate", "Un char qui fait peur.", 400,
                     tags_requis=["chenilles"], stats_min={"puissance": 40}, reputation={"B": 1}),
        ),
        EvenementCombat(
            "La Moissonneuse de l'Apocalypse",
            "Un fermier a construit une moissonneuse de 40 tonnes. Survis-lui.",
            adversaire("moissonneuse"), Arene("endurance"),
        ),
        EvenementChoix(
            "Que'est-ce que la puissance ?",
            "Tu as beaucoup de puissance. Mais qu'est-ce que la puissance ?",
            [
                ("La puissance, c'est la puissance.", {"message": "Évidemment."}),
                ("Mais t'est pas philosophe, tu tape sur des gens, pas des poisons.", {"message": "Ouais pas besoin de réflechir."}),
                ("La puissance c'est pour protéger,... TA THUNE.", {"argent": 100, "message": "Votre patrimoine vous rapporte +100 $"}),
            ]
        ),
        EvenementCombat(
            "Toujours plus fort que soit",
            "C'est faux et tu vas le prouver",
            adversaire("Bezard"), Arene("combat"),
        ),
        EvenementChoix(
            "Le bouton rouge",
            "Ton dernier véhicule a un bouton rouge. Il n'est relié à rien. Enfin, normalement.",
            [
                ("Appuyer.", {}),
                ("Appuyer très fort.", {}),
                ("Demander à quoi il sert, puis appuyer.", {}),
            ],
        ),
    ]


def branche_c():
    """C — Science : exploration."""
    return [
        EvenementCommande(
            "Professeure Tournesol",
            "Une scientifique veut explorer la fosse des Mariannes. « Il me faut un bateau qui résiste à TOUT. »",
            Commande("Professeure Tournesol", "Un bateau indestructible.", 300,
                     modele="Bateau", stats_min={"resistance": 100}, reputation={"C": 1}),
        ),
        EvenementChoix(
            "L'expérience",
            "La professeure veut mettre un moteur banane dans un accélérateur de particules.",
            [
                ("Pour la science !", {"argent": 150, "message": "Tu découvres le boson de banane. Prime : 150 $."}),
                ("Écrire un article dessus.", {"argent": 80, "message": "Publié dans « Nature (des fruits) ». +80 $"}),
                ("Manger la banane.", {"message": "Elle avait un goût de neutrino. Pas très bon a mon avis."}),
            ],
        ),
        EvenementCommande(
            "L'agence spatiale",
            "Une agence spatiale (pas la NASA, la NASB) veut un avion assez puissant pour quitter l'atmosphère.",
            Commande("Agence spatiale NASA-B", "Un avion qui va dans l'espace.", 1500,
                     modele="Avion", stats_min={"puissance": 1000}),
        ),
        EvenementChoix(
            "L'espace",
            "Tu as quitté l'atmosphère. Tu es dans l'espace. Il n'y a pas de gravité. Il n'y a pas d'air. Il n'y a que toi. \n Attends ... Il n'y a aucun concurrent, OUVRE TON GARAGE SPATIAL !",
            [
                ("Choisir la lune.", {"message": "Mais ou a tu la tete ?"}),
                ("L'espace entier", {"message": "Tu as raison, l'espace est grand."}),
                ("Mars c'est bien.", {"message": "Fera un peu chaud. Et froid."}),
                ("Pourquoi se limiter a une galaxie ?", {"message": "L'espace sera a toi"}),
            ],
        ),
        EvenementCombat(
            "Apres espace",
            "L'espace, les dimensions, tu comprends pas trop tout ca. Mais tu vas devoir utiliser tes 2 neurones au garrot pour prouver a la NASB que l'espace t'appartiens",
            adversaire("Prof Raoult"), Arene("combat"),
        )
    ]


def branche_d():
    """D — Livraison : clients louches."""
    return [
        EvenementCommande(
            "Monsieur X",
            "Un homme en lunettes noires (de nuit) veut une voiture « qui ne laisse pas de traces ». En carton, donc.",
            Commande("Monsieur X", "Une voiture discrète en carton.", 150,
                     modele="Voiture", tags_requis=["carton"], bonus_tags={"banane": 30},
                     reputation={"D": 1}),
        ),
        EvenementChoix(
            "Le colis qui fait tic-tac",
            "Monsieur X te confie un colis. Il fait tic-tac. « C'est une horloge. Ne l'ouvre pas. »",
            [
                ("Le livrer.", {"argent": 200, "message": "C'était bien une horloge. Probablement. +200 $"}),
                ("L'ouvrir.", {"argent": 50, "message": "C'est une horloge. Tu as l'air bête. +50 $ quand même."}),
                ("Le mettre dans le moteur.", {"message": "Ton moteur donne maintenant l'heure."}),
            ],
        ),
        EvenementCombat(
            "Course-poursuite",
            "Sirènes ! La brigade des douanes volantes te prend en chasse. Sème-les !",
            adversaire("douane"), Arene("course"),
        ),
    ]


ANNONCES = {
    "A": "Le monde entier parle de toi : « le gamin qui va trop vite ». Branche T1.",
    "B": "On murmure ton nom avec crainte. Les assureurs pleurent. Branche Du sang !",
    "C": "Des scientifiques font la queue devant ta cabane. Branche Science.",
    "D": "Ton téléphone sonne. Numéro masqué. Encore. Branche Livraison.",
}

FINS = {
    "A": "Tu appuies sur l'accélérateur. Le paysage devient une ligne, puis un point, puis rien.\n"
         "Tu as atteint la VITESSE DE LA LUMIÈRE. Tes parents ne te verront plus jamais : tu es déjà parti hier.",
    "B": "Le bouton rouge était relié à quelque chose. La planète d'à côté n'existe plus.\n"
         "Dans les décombres, une main métallique se lève : « I'll be back. »",
    "C": "Le premier embouteillage de l'espace a lieu en orbite basse, à cause de toi.\n"
         "Des voitures dans l'espace. La science est fière. Les astronautes beaucoup moins.",
    "D": "En passant devant la poste, tu vois une affiche : « CIBLE PRIORITAIRE ».\n"
         "C'est ta tête. Tu ne sais absolument pas pourquoi. Le colis faisait toujours tic-tac.",
}
