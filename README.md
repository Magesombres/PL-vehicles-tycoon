# PL-vehicles-tycoon

Jeu textuel en Python (projet POO de NSI) : construis des véhicules, affronte d'autres
véhicules, fais des choix à travers l'histoire et **GAGNE UN MAX DE THUNE**.

## Lancer le jeu

```
python main.py
```

Python 3, aucune bibliothèque à installer.

## Menu principal et sauvegardes

Au lancement, on choisit une des **5 sauvegardes**. Chaque ligne affiche le nom du joueur,
le nombre de runs faites, les fins obtenues, les trophées et la thune. La partie est
sauvegardée automatiquement à chaque retour au garage, dans `sauvegardes/emplacement_N.json`.

## Mode admin (pour tester le jeu)

Au menu principal, choisir **6. Mode admin**. C'est une partie à part : rien n'est sauvegardé
et les 5 sauvegardes ne sont pas touchées. Le garage gagne une entrée **7. Menu admin** :

- voir l'état de la partie (étape en cours, réputation cachée, fins, trophées) ;
- recevoir 100 000 $ ;
- recevoir le véhicule ultime, qui bat tous les adversaires ;
- débloquer toutes les pièces de boss en boutique ;
- aller à n'importe quelle étape de l'histoire (tronc commun, branches A à D, boss final) ;
- marquer les 4 fins comme obtenues ;
- affronter n'importe quel adversaire, boss compris.

Pour voir le boss final et la Divinité en 1 minute : passer l'intro et le premier choix, puis
au garage 7 → 3 (véhicule ultime) → 5 (aller à une étape) → 6 (boss final) → 2 (le combat),
répondre `o` et attaquer avec 1.

## Déroulement d'une run

1. **Tronc commun** : tes parents te mettent dehors, premier client, premier combat.
   Chaque choix donne des points de réputation cachés (A, B, C, D).
2. **Branche** : la réputation la plus haute décide de ta voie (parmi celles pas encore finies).
   - A — T1 (vitesse) : jusqu'à la vitesse de la lumière
   - B — Du sang ! (puissance) : destruction d'une planète
   - C — Science (exploration) : des voitures dans l'espace
   - D — Livraison (clients louches) : avis de recherche « cible prioritaire »
3. Chaque branche se termine par un boss puis une fin : **la run est finie**. La suivante
   repart de zéro (thune, pièces, véhicules), mais la sauvegarde garde :
   - le compteur de runs,
   - les fins obtenues,
   - les **trophées** : chaque boss vaincu lâche une de ses pièces au hasard. Elle devient
     achetable en boutique pour toutes les runs, et un exemplaire t'attend au garage au début
     de la run suivante.
4. **Boss final secret** : il se débloque une fois les 4 fins obtenues (donc au moins 4 runs).
   Le battre pour la première fois donne la pièce ultime : la **Divinité**.

Le garage est le menu de jeu : Constructeur, Boutique, Commandes, Arène, Inventaire.
En course, la distance à parcourir dépend du niveau de l'adversaire (300 m par niveau).

## Fichiers

| Fichier | Contenu |
|---|---|
| `main.py` | Point d'entrée et menu principal (choix de la sauvegarde) |
| `sauvegarde.py` | Lecture et écriture des 5 sauvegardes (JSON) |
| `admin.py` | Menu du mode admin (triche pour tester le jeu) |
| `vehicule.py` | `Piece`, `Modele`, `Vehicule` : construction et calcul des stats |
| `pilotes.py` | `Pilote`, `Joueur`, `Adversaire` : actions de combat, IA |
| `arene.py` | `Arene` : combat au tour par tour (combat, course, endurance, event) |
| `commande.py` | `Commande` : exigences d'un client, récompense, bonus de tags |
| `evenements.py` | `Evenement`, `EvenementChoix`, `EvenementCombat`, `EvenementCommande` |
| `jeu.py` | `Jeu` : menus du garage et déroulement de l'histoire |
| `competences.py` | Capacités spéciales débloquées par les tags des pièces |
| `donnees.py` | Modèles, pièces (boutique et boss), adversaires, commandes aléatoires |
| `histoire.py` | Textes et événements de l'histoire, annonces et fins |
| `outils.py` | Saisie et affichage |

## Architecture POO

13 classes, 2 hiérarchies d'héritage :

- `Joueur` et `Adversaire` héritent de `Pilote`. `choisir_action()` est redéfinie :
  le joueur tape au clavier, l'adversaire décide seul.
- `EvenementChoix`, `EvenementCombat` et `EvenementCommande` héritent de `Evenement`.
  `Jeu` appelle `evenement.jouer(self)` sans connaître le type de l'événement.

Ajouter un véhicule ou une pièce ne demande aucune nouvelle classe, juste une ligne dans
`donnees.py` :

```python
"sous-marin": Modele("Sous-marin", ["moteur", "coque", "periscope"]),
Piece("Moteur banane", "moteur", 5, {"puissance": 2, "vitesse": 5, "poids": 1}, ["banane"]),
```
