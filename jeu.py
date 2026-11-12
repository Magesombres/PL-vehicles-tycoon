"""Julien L. — Jeu : garage (menu principal), menus et déroulement de l'histoire."""

import random
from collections import Counter

import admin
import competences
import donnees
import histoire
import sauvegarde
from arene import Arene
from couleurs import colorer
from outils import demander_nombre, oui_non, pause, thune, titre
from pilotes import Joueur
from vehicule import Vehicule

NB_COMMANDES_LIBRES = 2


class Jeu:
    """La partie : progression gardée d'une run à l'autre, état de la run en cours et menus du garage."""

    def __init__(self, emplacement, nom_joueur="Le gamin", admin=False):
        self.emplacement = emplacement  # numéro de sauvegarde (1 à 5)
        self.admin = admin  # mode admin : menu de triche en plus, rien n'est sauvegardé
        # Progression gardée d'une run à l'autre
        self.runs_finies = 0
        self.branches_finies = []
        self.final_battu = False
        self.trophees = []  # noms des pièces de boss débloquées en boutique
        self.butin = []  # trophées gagnés pendant cette run, offerts au début de la suivante
        self.joueur = Joueur(nom_joueur)
        self.nouvelle_run()
        self.en_cours = True

    def nouvelle_run(self):
        """Remet à zéro tout ce qui appartient à une run : thune, pièces, véhicules, histoire."""
        self.joueur = Joueur(self.joueur.nom)
        self.joueur.pieces = donnees.kit_de_depart() + [donnees.piece(nom) for nom in self.butin]
        self.butin = []
        self.commandes = []
        self.evenements = histoire.tronc_commun()  # file d'événements en cours
        self.etape = 0
        self.branche = None
        self.commande_histoire = None  # commande à livrer pour avancer l'histoire
        self.intro_a_afficher = True

    # --- Sauvegarde ----------------------------------------------------------------

    def exporter(self):
        """Convertit la partie en dictionnaire pour la sauvegarde JSON."""
        j = self.joueur
        return {
            "runs_finies": self.runs_finies,
            "branches_finies": self.branches_finies,
            "final_battu": self.final_battu,
            "trophees": self.trophees,
            "butin": self.butin,
            "joueur": {
                "nom": j.nom,
                "argent": j.argent,
                "reputation": j.reputation,
                "pieces": [p.nom for p in j.pieces],
                "vehicules": [{"modele": donnees.cle_modele(v.modele), "nom": v.nom,
                               "pieces": [p.nom for p in v.pieces]} for v in j.vehicules],
                "actif": j.vehicules.index(j.vehicule) if j.vehicule else None,
            },
            "branche": self.branche,
            "etape": self.etape,
        }

    @classmethod
    def depuis_sauvegarde(cls, emplacement, donnees_save):
        """Recrée une partie à partir d'un dictionnaire de sauvegarde."""
        jeu = cls(emplacement, donnees_save["joueur"]["nom"])
        jeu.runs_finies = donnees_save["runs_finies"]
        jeu.branches_finies = donnees_save["branches_finies"]
        jeu.final_battu = donnees_save["final_battu"]
        jeu.trophees = donnees_save["trophees"]
        jeu.butin = donnees_save.get("butin", [])
        d = donnees_save["joueur"]
        j = jeu.joueur
        j.argent = d["argent"]
        j.reputation = d["reputation"]
        j.pieces = [donnees.piece(nom) for nom in d["pieces"]]
        j.vehicules = [donnees.creer_vehicule(v["modele"], v["pieces"], v["nom"]) for v in d["vehicules"]]
        j.vehicule = j.vehicules[d["actif"]] if d["actif"] is not None else None
        # Les événements sont recréés : on reprend à la même étape (une commande d'histoire
        # en attente sera simplement reproposée).
        jeu.branche = donnees_save["branche"]
        jeu.etape = donnees_save["etape"]
        jeu.evenements = histoire.branche(jeu.branche) if jeu.branche else histoire.tronc_commun()
        jeu.intro_a_afficher = jeu.branche is None and jeu.etape == 0
        return jeu

    def sauvegarder(self):
        """Écrit la partie dans son emplacement de sauvegarde (sauf en mode admin)."""
        if not self.admin:
            sauvegarde.ecrire(self.emplacement, self.exporter())

    # --- Boucle principale -----------------------------------------------------

    def lancer(self):
        """Boucle principale : histoire puis garage, jusqu'au retour au menu principal."""
        while self.en_cours:
            if self.intro_a_afficher:
                titre(f"RUN {self.runs_finies + 1}")
                print(histoire.INTRO)
                pause()
                self.intro_a_afficher = False
            self.completer_commandes()
            self.verifier_histoire()
            self.sauvegarder()  # sauvegarde automatique à chaque retour au garage
            if self.en_cours:
                self.garage()
        self.sauvegarder()
        print("\nFin du mode admin." if self.admin else "\nPartie sauvegardée. À plus, magnat du véhicule !")

    def garage(self):
        """Menu de jeu d'une run."""
        print(f"\n{colorer('=== GARAGE ===', 'cyan', 'gras')}  Thune : {thune(self.joueur.argent)}   "
              f"(run {self.runs_finies + 1})")
        actif = self.joueur.vehicule
        print(f"Véhicule actif : {actif if actif else 'aucun'}")
        actions = [
            ("Constructeur", self.constructeur),
            ("Boutique", self.boutique),
            (f"Commandes ({len(self.commandes)} en attente)", self.menu_commandes),
            ("Arène", self.menu_arene),
            ("Inventaire", self.inventaire),
            ("Menu principal", self.quitter),
        ]
        if self.admin:
            actions.append(("Menu admin", lambda: admin.menu(self)))
        for i, (libelle, _) in enumerate(actions, 1):
            print(f"{i}. {libelle}")
        actions[demander_nombre(1, len(actions)) - 1][1]()

    def quitter(self):
        """Retour au menu principal (la partie est sauvegardée, sauf en mode admin)."""
        etat = "la partie admin sera perdue" if self.admin else "la partie est sauvegardée"
        if oui_non(f"Retourner au menu principal ? ({etat})"):
            self.en_cours = False

    # --- Histoire ----------------------------------------------------------------

    def verifier_histoire(self):
        """Joue au plus un événement entre deux actions du garage."""
        if self.commande_histoire is not None or self.etape >= len(self.evenements):
            return
        if self.evenements[self.etape].jouer(self):  # polymorphisme : on ne connaît pas le type
            self.avancer_histoire()

    def avancer_histoire(self):
        """Passe à l'étape suivante ; en fin de liste, choisit ou termine une branche."""
        self.etape += 1
        if self.etape < len(self.evenements):
            return
        if self.branche is None:
            self.choisir_branche()  # milieu de l'histoire
        else:
            self.terminer_branche()

    def choisir_branche(self):
        """La branche avec le plus de réputation (parmi celles pas finies) devient la voie du joueur."""
        restantes = {b: pts for b, pts in self.joueur.reputation.items() if b not in self.branches_finies}
        if not restantes:  # les 4 fins sont déjà obtenues : toutes les branches sont rejouables
            restantes = self.joueur.reputation
        self.demarrer_branche(max(restantes, key=restantes.get))

    def demarrer_branche(self, lettre):
        """Charge les événements de la branche et l'annonce."""
        self.branche = lettre
        self.evenements = histoire.branche(lettre)
        self.etape = 0
        titre("TON DESTIN SE PRÉCISE")
        print(histoire.ANNONCES[lettre])
        pause()

    def terminer_branche(self):
        """Affiche la fin, note la progression, puis lance le boss final ou finit la run."""
        titre("FIN")
        print(histoire.FINS[self.branche])
        pause()
        if self.branche == "final":
            if not self.final_battu:
                self.debloquer_trophee("Divinité", "PIÈCE ULTIME")  # une seule fois par sauvegarde
            self.final_battu = True
        elif self.branche not in self.branches_finies:
            self.branches_finies.append(self.branche)
        if len(self.branches_finies) == 4 and not self.final_battu:
            self.demarrer_branche("final")  # les 4 fins obtenues : boss final secret
            return
        self.finir_run()

    def finir_run(self):
        """Clôt la run, affiche le bilan et prépare la suivante."""
        self.runs_finies += 1
        titre(f"FIN DE LA RUN {self.runs_finies}")
        print(f"Thune à la fin de la run : {self.joueur.argent} $")
        print(self.bilan())
        self.nouvelle_run()
        if not oui_non("Enchaîner sur une nouvelle run ?"):
            self.en_cours = False

    def bilan(self):
        """Progression gardée d'une run à l'autre."""
        fins = ", ".join(self.branches_finies) or "aucune"
        final = " + boss final" if self.final_battu else ""
        return (f"Runs faites : {self.runs_finies}\n"
                f"Fins obtenues : {len(self.branches_finies)}/4 ({fins}){final}\n"
                f"Trophées ({len(self.trophees)}) : {', '.join(self.trophees) or 'aucun'}")

    def appliquer_effets(self, effets):
        """Effets d'un choix : {"argent": int, "reputation": {lettre: pts}, "message": str}."""
        if "message" in effets:
            print(effets["message"])
        self.joueur.argent += effets.get("argent", 0)
        for branche, points in effets.get("reputation", {}).items():
            self.joueur.reputation[branche] += points

    def ajouter_commande_histoire(self, commande):
        """Met une commande d'histoire en tête de liste ; l'histoire attend sa livraison."""
        self.commande_histoire = commande
        self.commandes.insert(0, commande)

    # --- Constructeur ----------------------------------------------------------

    def constructeur(self):
        """Choisir un modèle, puis remplir chaque emplacement avec une pièce de l'inventaire."""
        titre("CONSTRUCTEUR")
        modeles = list(donnees.MODELES.values())
        for i, modele in enumerate(modeles, 1):
            print(f"{i}. {modele.nom} : {', '.join(modele.emplacements)}")
        print("0. Retour")
        choix = demander_nombre(0, len(modeles))
        if choix == 0:
            return
        vehicule = Vehicule(modeles[choix - 1])

        while not vehicule.est_complet():
            emplacement = vehicule.prochain_emplacement()
            # Regroupe les pièces identiques : {nom: [pièces]}
            compatibles = {}
            for p in self.joueur.pieces:
                if p.emplacement == emplacement:
                    compatibles.setdefault(p.nom, []).append(p)
            print(f"\nEmplacement à remplir : {emplacement}")
            if not compatibles:
                print("Aucune pièce pour cet emplacement. Passe à la boutique ! (pièces rangées)")
                self.joueur.pieces += vehicule.demonter()
                return
            groupes = list(compatibles.values())
            for i, groupe in enumerate(groupes, 1):
                print(f"{i}. {groupe[0]}  (x{len(groupe)})")
            print("0. Annuler la construction")
            choix = demander_nombre(0, len(groupes))
            if choix == 0:
                self.joueur.pieces += vehicule.demonter()
                print("Construction annulée, pièces rangées.")
                return
            piece = groupes[choix - 1][0]
            self.joueur.pieces.remove(piece)
            vehicule.poser(piece)

        print("\nVéhicule terminé !")
        print(vehicule.fiche())
        nom = input("Donne-lui un nom (Entrée pour garder le nom du modèle) : ").strip()
        if nom:
            vehicule.nom = nom
        self.joueur.vehicules.append(vehicule)
        if self.joueur.vehicule is None:
            self.joueur.vehicule = vehicule

    # --- Boutique ----------------------------------------------------------------

    def pieces_boutique(self):
        """Le catalogue, plus les trophées débloqués sur cette sauvegarde."""
        return donnees.CATALOGUE + [donnees.piece(nom) for nom in self.trophees]

    def boutique(self):
        """Choix du rayon (un rayon par type d'emplacement)."""
        while True:
            titre(f"BOUTIQUE  —  Thune : {self.joueur.argent} $")
            types = []
            for p in self.pieces_boutique():
                if p.emplacement not in types:
                    types.append(p.emplacement)
            for i, emplacement in enumerate(types, 1):
                print(f"{i}. {emplacement}")
            print(" 0. Retour")
            choix = demander_nombre(0, len(types))
            if choix == 0:
                return
            self.boutique_rayon(types[choix - 1])

    def boutique_rayon(self, emplacement):
        """Achat des pièces d'un rayon."""
        pieces = [p for p in self.pieces_boutique() if p.emplacement == emplacement]
        while True:
            titre(f"BOUTIQUE — {emplacement}  —  Thune : {self.joueur.argent} $")
            for i, p in enumerate(pieces, 1):
                marque = "  (trophée)" if p.nom in self.trophees else ""
                print(f"{i:>2}. {p.prix:>4} $  {p}{marque}")
            print(" 0. Retour")
            choix = demander_nombre(0, len(pieces))
            if choix == 0:
                return
            modele_piece = pieces[choix - 1]
            if modele_piece.prix > self.joueur.argent:
                print(colorer("Pas assez de thune !", "rouge"))
                continue
            self.joueur.argent -= modele_piece.prix
            self.joueur.pieces.append(modele_piece.copie())
            print(colorer(f"Acheté : {modele_piece.nom}", "vert"))

    # --- Commandes ---------------------------------------------------------------

    def completer_commandes(self):
        """Complète la liste avec des commandes libres tirées au hasard."""
        limite = NB_COMMANDES_LIBRES
        if competences.a_la_competence(self.joueur.vehicule, "remorque"):
            limite += 1
        libres = [c for c in self.commandes if c is not self.commande_histoire]
        for _ in range(limite - len(libres)):
            self.commandes.append(donnees.commande_aleatoire())

    def menu_commandes(self):
        """Liste les commandes et propose d'en livrer une."""
        titre("COMMANDES")
        for i, commande in enumerate(self.commandes, 1):
            marque = "  [HISTOIRE]" if commande is self.commande_histoire else ""
            print(f"{i}. {commande}{marque}")
        print("0. Retour")
        choix = demander_nombre(0, len(self.commandes))
        if choix:
            self.livrer(self.commandes[choix - 1])

    def livrer(self, commande):
        """Vérifie le véhicule, paie et applique la réputation. Renvoie True si la commande est livrée."""
        vehicule = self.choisir_vehicule("Quel véhicule livrer ?")
        if vehicule is None:
            return False
        problemes = commande.verifier(vehicule)
        if problemes:
            print(colorer(f"{commande.client} refuse :", "rouge"))
            for probleme in problemes:
                print(f"  - {probleme}")
            return False
        gain = commande.calculer_recompense(vehicule)
        self.joueur.argent += gain
        self.joueur.retirer_vehicule(vehicule)
        self.commandes.remove(commande)
        reputation = commande.reputation
        if competences.a_la_competence(vehicule, "lol"):
            reputation = {branche: points * 2 for branche, points in reputation.items()}
            print("Compétence LOL : réputation doublée !")
        self.appliquer_effets({"reputation": reputation})
        print(f"{commande.client} est ravi(e) ! +{thune(gain)}")
        if commande is self.commande_histoire:
            self.commande_histoire = None
            self.avancer_histoire()
        return True

    # --- Arène -------------------------------------------------------------------

    def menu_arene(self, adversaires=None):
        """Arène libre : choix du format, puis de l'adversaire, puis combat."""
        titre("ARÈNE")
        if self.joueur.vehicule is None:
            print("Il te faut un véhicule actif (Constructeur ou Inventaire).")
            return
        formats = list(Arene.FORMATS)
        for i, cle in enumerate(formats, 1):
            infos = Arene.FORMATS[cle]
            if infos["boost"]:
                detail = ", ".join(f"{stat} x{mult}" for stat, mult in infos["boost"].items())
            else:
                detail = "règle surprise tirée au sort"
            print(f"{i}. {infos['nom']} ({detail}) — {infos['victoire']}")
        print("0. Retour")
        choix = demander_nombre(0, len(formats))
        if choix == 0:
            return
        arene = Arene(formats[choix - 1])

        adversaires = adversaires or donnees.adversaires_arene()
        print("\nAdversaires :")
        for i, adv in enumerate(adversaires, 1):
            print(f"{i}. {adv} — {thune(adv.recompense)}")
        print("0. Retour")
        choix = demander_nombre(0, len(adversaires))
        if choix == 0:
            return
        adv = adversaires[choix - 1]
        if arene.combattre(self.joueur, adv) is self.joueur:
            self.gagner_combat(adv)

    def gagner_combat(self, adversaire):
        """Paie la récompense et, contre un boss, donne un trophée."""
        self.joueur.argent += adversaire.recompense
        print(f"Récompense : +{thune(adversaire.recompense)}")
        self.gagner_trophee(adversaire)

    def gagner_trophee(self, adversaire):
        """Un boss vaincu lâche une de ses pièces au hasard, débloquée en boutique pour de bon."""
        pieces_boss = {p.nom for p in adversaire.vehicule.pieces if donnees.est_piece_boss(p.nom)}
        if not pieces_boss:
            return  # pas un boss
        nouvelles = sorted(pieces_boss - set(self.trophees))
        if nouvelles:
            self.debloquer_trophee(random.choice(nouvelles), "TROPHÉE")
        else:
            nom = random.choice(sorted(pieces_boss))
            self.butin.append(nom)
            print(f"Tu récupères un(e) {nom} dans l'épave (tous ses trophées sont déjà débloqués).")
            print("Il t'attendra au garage au début de ta prochaine run.")

    def debloquer_trophee(self, nom, intitule):
        """Débloque la pièce en boutique et la met de côté pour le début de la prochaine run."""
        if nom not in self.trophees:  # le mode admin peut l'avoir déjà débloquée
            self.trophees.append(nom)
        self.butin.append(nom)
        print(f"{colorer(f'{intitule} : {nom} !', 'violet', 'gras')} Débloqué en boutique pour toutes tes runs,")
        print("et un exemplaire t'attendra au garage au début de ta prochaine run.")

    # --- Inventaire -----------------------------------------------------------

    def inventaire(self):
        """Pièces, véhicules et trophées ; choisir, vendre ou démonter un véhicule."""
        while True:
            titre(f"INVENTAIRE  —  Thune : {self.joueur.argent} $")
            print("Pièces :")
            compte = Counter(p.nom for p in self.joueur.pieces)
            for nom, nombre in compte.items():
                print(f"  {nombre} x {nom}")
            if not compte:
                print("  (aucune)")
            print("Véhicules :")
            for v in self.joueur.vehicules:
                marque = "  <- actif" if v is self.joueur.vehicule else ""
                print(v.fiche() + marque)
            if not self.joueur.vehicules:
                print("  (aucun)")
            print(f"Trophées débloqués : {', '.join(self.trophees) or 'aucun'}")
            print("\n1. Choisir le véhicule actif  2. Vendre un véhicule  3. Démonter un véhicule  0. Retour")
            choix = demander_nombre(0, 3)
            if choix == 0:
                return
            vehicule = self.choisir_vehicule("Lequel ?")
            if vehicule is None:
                continue
            if choix == 1:
                self.joueur.vehicule = vehicule
            elif choix == 2:
                prix = vehicule.calculer_stats()["valeur"]
                self.joueur.argent += prix
                self.joueur.retirer_vehicule(vehicule)
                print(f"Vendu pour {thune(prix)}.")
            else:
                self.joueur.pieces += vehicule.demonter()
                self.joueur.retirer_vehicule(vehicule)
                print("Démonté, pièces rangées.")

    def choisir_vehicule(self, question):
        """Demande au joueur un de ses véhicules (None s'il annule)."""
        if not self.joueur.vehicules:
            print("Tu n'as aucun véhicule terminé.")
            return None
        print(question)
        for i, v in enumerate(self.joueur.vehicules, 1):
            print(f"{i}. {v}")
        print("0. Annuler")
        choix = demander_nombre(0, len(self.joueur.vehicules))
        return self.joueur.vehicules[choix - 1] if choix else None
