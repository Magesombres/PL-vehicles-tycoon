"""Membre 3 — Jeu : garage (menu principal), menus et déroulement de l'histoire."""

from collections import Counter

import donnees
import histoire
from arene import Arene
from outils import demander_nombre, oui_non, pause, titre
from pilotes import Joueur
from vehicule import Vehicule

NB_COMMANDES_LIBRES = 2


class Jeu:
    def __init__(self, nom_joueur="Le gamin"):
        self.joueur = Joueur(nom_joueur)
        self.joueur.pieces = donnees.kit_de_depart()
        self.commandes = []
        self.evenements = histoire.tronc_commun()  # file d'événements en cours
        self.etape = 0
        self.branche = None
        self.branches_finies = []
        self.commande_histoire = None  # commande à livrer pour avancer l'histoire
        self.en_cours = True

    # --- Boucle principale -----------------------------------------------------

    def lancer(self):
        print(histoire.INTRO)
        pause()
        while self.en_cours:
            self.completer_commandes()
            self.verifier_histoire()
            self.garage()
        print("\nÀ plus, magnat du véhicule !")

    def garage(self):
        print(f"\n=== GARAGE ===  Thune : {self.joueur.argent} $")
        actif = self.joueur.vehicule
        print(f"Véhicule actif : {actif if actif else 'aucun'}")
        actions = [
            ("Constructeur", self.constructeur),
            ("Boutique", self.boutique),
            (f"Commandes ({len(self.commandes)} en attente)", self.menu_commandes),
            ("Arène", self.menu_arene),
            ("Inventaire", self.inventaire),
            ("Quitter", self.quitter),
        ]
        for i, (libelle, _) in enumerate(actions, 1):
            print(f"{i}. {libelle}")
        actions[demander_nombre(1, len(actions)) - 1][1]()

    def quitter(self):
        if oui_non("Vraiment quitter ? (pas de sauvegarde dans l'alpha)"):
            self.en_cours = False

    # --- Histoire ----------------------------------------------------------------

    def verifier_histoire(self):
        """Joue au plus un événement entre deux actions du garage."""
        if self.commande_histoire is not None or self.etape >= len(self.evenements):
            return
        if self.evenements[self.etape].jouer(self):  # polymorphisme : on ne connaît pas le type
            self.avancer_histoire()

    def avancer_histoire(self):
        self.etape += 1
        if self.etape < len(self.evenements):
            return
        if self.branche is None:
            self.choisir_branche()  # milieu de l'histoire
        else:
            self.terminer_branche()

    def choisir_branche(self):
        restantes = {b: pts for b, pts in self.joueur.reputation.items() if b not in self.branches_finies}
        self.branche = max(restantes, key=restantes.get)
        self.evenements = histoire.branche(self.branche)
        self.etape = 0
        titre("TON DESTIN SE PRÉCISE")
        print(histoire.ANNONCES[self.branche])
        pause()

    def terminer_branche(self):
        titre("FIN")
        print(histoire.FINS[self.branche])
        pause()
        self.branches_finies.append(self.branche)
        if len(self.branches_finies) < 4 and oui_non("Continuer l'aventure sur une autre voie ?"):
            self.choisir_branche()
        else:
            self.evenements, self.etape = [], 0
            print("Mode libre : continue à construire, vendre et combattre pour la thune.")

    def appliquer_effets(self, effets):
        """Effets d'un choix : {"argent": int, "reputation": {lettre: pts}, "message": str}."""
        if "message" in effets:
            print(effets["message"])
        self.joueur.argent += effets.get("argent", 0)
        for branche, points in effets.get("reputation", {}).items():
            self.joueur.reputation[branche] += points

    def ajouter_commande_histoire(self, commande):
        self.commande_histoire = commande
        self.commandes.insert(0, commande)

    # --- Constructeur ----------------------------------------------------------

    def constructeur(self):
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

    def boutique(self):
        while True:
            titre(f"BOUTIQUE  —  Thune : {self.joueur.argent} $")
            for i, p in enumerate(donnees.CATALOGUE, 1):
                print(f"{i:>2}. {p.prix:>4} $  {p}")
            print(" 0. Retour")
            choix = demander_nombre(0, len(donnees.CATALOGUE))
            if choix == 0:
                return
            modele_piece = donnees.CATALOGUE[choix - 1]
            if modele_piece.prix > self.joueur.argent:
                print("Pas assez de thune !")
                continue
            self.joueur.argent -= modele_piece.prix
            self.joueur.pieces.append(modele_piece.copie())
            print(f"Acheté : {modele_piece.nom}")

    # --- Commandes ---------------------------------------------------------------

    def completer_commandes(self):
        libres = [c for c in self.commandes if c is not self.commande_histoire]
        for _ in range(NB_COMMANDES_LIBRES - len(libres)):
            self.commandes.append(donnees.commande_aleatoire())

    def menu_commandes(self):
        titre("COMMANDES")
        for i, commande in enumerate(self.commandes, 1):
            marque = "  [HISTOIRE]" if commande is self.commande_histoire else ""
            print(f"{i}. {commande.resume()}{marque}")
        print("0. Retour")
        choix = demander_nombre(0, len(self.commandes))
        if choix:
            self.livrer(self.commandes[choix - 1])

    def livrer(self, commande):
        vehicule = self.choisir_vehicule("Quel véhicule livrer ?")
        if vehicule is None:
            return False
        problemes = commande.verifier(vehicule)
        if problemes:
            print(f"{commande.client} refuse :")
            for probleme in problemes:
                print(f"  - {probleme}")
            return False
        gain = commande.calculer_recompense(vehicule)
        self.joueur.argent += gain
        self.joueur.retirer_vehicule(vehicule)
        self.commandes.remove(commande)
        self.appliquer_effets({"reputation": commande.reputation})
        print(f"{commande.client} est ravi(e) ! +{gain} $")
        if commande is self.commande_histoire:
            self.commande_histoire = None
            self.avancer_histoire()
        return True

    # --- Arène -------------------------------------------------------------------

    def menu_arene(self):
        titre("ARÈNE")
        if self.joueur.vehicule is None:
            print("Il te faut un véhicule actif (Constructeur ou Inventaire).")
            return
        formats = list(Arene.FORMATS)
        for i, cle in enumerate(formats, 1):
            infos = Arene.FORMATS[cle]
            boost = ", ".join(f"{stat} x{mult}" for stat, mult in infos["boost"].items())
            print(f"{i}. {infos['nom']} ({boost}) — {infos['victoire']}")
        print("0. Retour")
        choix = demander_nombre(0, len(formats))
        if choix == 0:
            return
        arene = Arene(formats[choix - 1])

        adversaires = donnees.adversaires_arene()
        print("\nAdversaires :")
        for i, adv in enumerate(adversaires, 1):
            print(f"{i}. {adv.nom} (niv. {adv.niveau}) sur {adv.vehicule} — {adv.recompense} $")
        print("0. Retour")
        choix = demander_nombre(0, len(adversaires))
        if choix == 0:
            return
        adv = adversaires[choix - 1]
        if arene.combattre(self.joueur, adv) is self.joueur:
            self.gagner_combat(adv)

    def gagner_combat(self, adversaire):
        self.joueur.argent += adversaire.recompense
        print(f"Récompense : +{adversaire.recompense} $")

    # --- Inventaire -----------------------------------------------------------

    def inventaire(self):
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
                print(f"Vendu pour {prix} $.")
            else:
                self.joueur.pieces += vehicule.demonter()
                self.joueur.retirer_vehicule(vehicule)
                print("Démonté, pièces rangées.")

    def choisir_vehicule(self, question):
        if not self.joueur.vehicules:
            print("Tu n'as aucun véhicule terminé.")
            return None
        print(question)
        for i, v in enumerate(self.joueur.vehicules, 1):
            print(f"{i}. {v}")
        print("0. Annuler")
        choix = demander_nombre(0, len(self.joueur.vehicules))
        return self.joueur.vehicules[choix - 1] if choix else None
