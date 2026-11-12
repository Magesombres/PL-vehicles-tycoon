"""Tests automatiques du jeu : python tests.py (aucune bibliothèque à installer).

Chaque fonction test_... vérifie une règle du jeu avec assert ; tester() les lance toutes.
"""

import contextlib
import io
import random
import shutil
import tempfile

import couleurs
import donnees
import histoire
import sauvegarde
from arene import Arene
from commande import Commande
from evenements import Evenement
from jeu import Jeu
from outils import barre
from pilotes import Joueur, Pilote
from vehicule import Vehicule

couleurs.actives = False  # on compare des textes sans codes couleur


# --- Véhicules -------------------------------------------------------------------

def test_piece_achetee_est_une_copie():
    """Modifier une pièce achetée ne modifie pas celle de la boutique."""
    modele = donnees.CATALOGUE[0]
    copie = modele.copie()
    copie.bonus["puissance"] = 999
    assert copie is not modele
    assert modele.bonus.get("puissance") != 999


def test_construction_vehicule():
    """Les pièces vont dans le bon emplacement, et le véhicule n'est complet qu'une fois rempli."""
    vehicule = Vehicule(donnees.MODELES["trottinette"])
    assert not vehicule.est_complet()
    assert not vehicule.poser(donnees.piece("Châssis bois"))  # pas d'emplacement châssis
    for nom in ("Roue bambou", "Roue bambou", "Moteur banane"):
        assert vehicule.poser(donnees.piece(nom))
    assert vehicule.est_complet()
    resistance = Vehicule.RESISTANCE_DE_BASE + sum(p.bonus.get("resistance", 0) for p in vehicule.pieces)
    assert vehicule.calculer_stats()["resistance"] == resistance


def test_demontage_rend_les_pieces():
    """Démonter vide le véhicule et rend toutes ses pièces."""
    vehicule = donnees.adversaire("kevin").vehicule
    pieces = vehicule.demonter()
    assert len(pieces) == 3
    assert vehicule.prochain_emplacement() == "roue"


def test_tous_les_adversaires_ont_un_vehicule_complet():
    """Les 24 adversaires du jeu se construisent sans pièce manquante."""
    adversaires = donnees.tous_les_adversaires()
    assert len(adversaires) == 24
    assert all(adv.vehicule.est_complet() for adv in adversaires)


# --- Commandes -------------------------------------------------------------------

def test_commande_verifie_les_exigences():
    """Une commande refuse un véhicule pas terminé ou du mauvais modèle."""
    commande = Commande("Client", "Un bateau.", 70, modele="Bateau")
    trottinette = Vehicule(donnees.MODELES["trottinette"])
    assert "le véhicule n'est pas terminé" in commande.verifier(trottinette)
    assert "il fallait un(e) Bateau" in commande.verifier(donnees.adversaire("kevin").vehicule)


def test_commande_bonus_de_tags():
    """Chaque pièce portant le tag bonus ajoute sa prime à la récompense."""
    vehicule = donnees.adversaire("kevin").vehicule  # porte un Moteur banane
    commande = Commande("Singe", "Une banane.", 20, tags_requis=["banane"], bonus_tags={"banane": 20})
    nb_bananes = sum(1 for p in vehicule.pieces if "banane" in p.tags)
    assert nb_bananes >= 1
    assert commande.verifier(vehicule) == []
    assert commande.calculer_recompense(vehicule) == 20 + 20 * nb_bananes


# --- POO -------------------------------------------------------------------------

def test_classes_abstraites():
    """On ne peut pas créer un Evenement ou un Pilote « tout court », seulement leurs enfants."""
    for creer in (lambda: Evenement("titre", "texte"), lambda: Pilote("nom")):
        try:
            creer()
        except TypeError:
            continue
        raise AssertionError("une classe abstraite a pu être instanciée")


def test_polymorphisme_des_evenements():
    """Chaque événement de l'histoire redéfinit jouer()."""
    voies = [histoire.tronc_commun()] + [histoire.branche(b) for b in ("A", "B", "C", "D", "final")]
    for evenements in voies:
        assert evenements
        for evenement in evenements:
            assert isinstance(evenement, Evenement)
            assert type(evenement).jouer is not Evenement.jouer


def test_thune_jamais_negative():
    """La propriété argent bloque la thune à 0."""
    joueur = Joueur("Testeur")
    joueur.argent -= 1000
    assert joueur.argent == 0
    joueur.argent += 50
    assert joueur.argent == 50


# --- Arène -----------------------------------------------------------------------

def test_course_plus_longue_contre_un_haut_niveau():
    """En course, la distance à parcourir vaut 300 m par niveau de l'adversaire."""
    random.seed(0)
    arene = Arene("course")
    adversaire = donnees.adversaire("gerard")
    with contextlib.redirect_stdout(io.StringIO()):
        arene.combattre(donnees.adversaire("kevin"), adversaire)
    assert arene.distance_cible == Arene.DISTANCE_PAR_NIVEAU * adversaire.niveau


def test_le_plus_fort_gagne():
    """Le boss final écrase Kévin dans tous les formats."""
    for format_arene in Arene.FORMATS:
        random.seed(0)
        boss = donnees.adversaire("Vénère julien")
        with contextlib.redirect_stdout(io.StringIO()):
            gagnant = Arene(format_arene).combattre(boss, donnees.adversaire("kevin"))
        assert gagnant is boss, format_arene


def test_barre_de_pv():
    """La barre est pleine à 100 %, vide à 0, et garde un bloc tant qu'il reste des PV."""
    assert barre(10, 10) == "[" + "█" * 20 + "]"
    assert barre(0, 10) == "[" + "░" * 20 + "]"
    assert barre(1, 1000).count("█") == 1


# --- Progression et sauvegarde ---------------------------------------------------

def test_trophee_seulement_contre_un_boss():
    """Un boss lâche une de ses pièces ; un adversaire normal ne donne rien."""
    jeu = Jeu(None, admin=True)
    with contextlib.redirect_stdout(io.StringIO()):
        jeu.gagner_trophee(donnees.adversaire("kevin"))
        assert jeu.trophees == []
        jeu.gagner_trophee(donnees.adversaire("Bezard"))
    assert len(jeu.trophees) == 1
    assert donnees.est_piece_boss(jeu.trophees[0])
    assert jeu.butin == jeu.trophees  # la pièce attend au garage de la prochaine run


def test_sauvegarde_aller_retour():
    """Une partie sauvegardée puis rechargée est identique."""
    dossier_normal = sauvegarde.DOSSIER
    sauvegarde.DOSSIER = tempfile.mkdtemp()
    try:
        jeu = Jeu(1, "Testeur")
        jeu.joueur.argent = 777
        vehicule = donnees.adversaire("kevin").vehicule
        jeu.joueur.vehicules.append(vehicule)
        jeu.joueur.vehicule = vehicule
        jeu.trophees.append("Divinité")
        jeu.branches_finies.append("B")
        jeu.sauvegarder()
        recharge = Jeu.depuis_sauvegarde(1, sauvegarde.lire(1))
        assert recharge.exporter() == jeu.exporter()
    finally:
        shutil.rmtree(sauvegarde.DOSSIER)
        sauvegarde.DOSSIER = dossier_normal


def tester():
    """Lance tous les tests et affiche le résultat de chacun."""
    tests = [(nom, f) for nom, f in globals().items() if nom.startswith("test_")]
    echecs = 0
    for nom, test in tests:
        try:
            test()
            print(f"OK     {nom}")
        except Exception as erreur:
            echecs += 1
            print(f"ÉCHEC  {nom} : {type(erreur).__name__} {erreur}")
    print(f"\n{len(tests) - echecs}/{len(tests)} tests réussis.")


if __name__ == "__main__":
    tester()
