"""Point d'entrée : affiche le titre puis le menu principal (choix de la sauvegarde)."""

import sauvegarde
from jeu import Jeu
from outils import demander_nombre, oui_non, titre


def menu_principal():
    """Écran d'accueil : choix d'une des 5 sauvegardes, ou du mode admin."""
    choix_admin = sauvegarde.NB_EMPLACEMENTS + 1
    while True:
        titre("PL VEHICLES TYCOON — MENU PRINCIPAL")
        for emplacement in range(1, sauvegarde.NB_EMPLACEMENTS + 1):
            print(f"{emplacement}. Sauvegarde {emplacement} : {sauvegarde.resume(sauvegarde.lire(emplacement))}")
        print(f"{choix_admin}. Mode admin (pour tester le jeu : partie à part, non sauvegardée)")
        print("0. Quitter le jeu")
        emplacement = demander_nombre(0, choix_admin)
        if emplacement == 0:
            return
        if emplacement == choix_admin:
            Jeu(None, "Admin", admin=True).lancer()
        else:
            ouvrir(emplacement)


def ouvrir(emplacement):
    """Nouvelle partie si l'emplacement est vide, sinon continuer ou effacer."""
    donnees_save = sauvegarde.lire(emplacement)
    if donnees_save is None:
        nom = input("Nouvelle partie ! Ton nom (Entrée pour « Le gamin ») : ").strip() or "Le gamin"
        Jeu(emplacement, nom).lancer()
        return
    print("1. Continuer   2. Effacer la sauvegarde   0. Retour")
    choix = demander_nombre(0, 2)
    if choix == 1:
        try:
            jeu = Jeu.depuis_sauvegarde(emplacement, donnees_save)
        except (KeyError, IndexError, TypeError):
            print("Cette sauvegarde n'est plus compatible avec la version du jeu.")
            return
        jeu.lancer()
    elif choix == 2 and oui_non(f"Effacer définitivement la sauvegarde {emplacement} ?"):
        sauvegarde.effacer(emplacement)
        print("Sauvegarde effacée.")


if __name__ == "__main__":
    print(r"""                                                                                                                            
                                                                   ....:::-----------:::....                                
                                                      :=+++***###############***++==-----=+-::-:===-+=:                     
                                                  .+#@@@%%#*++++++++++++*****************+-::===-==---=++:                  
                                               .+#@%*++++++************************######-::====--+=----%%#=                
                                             +%%*++*******************##################*--======--==--*%%%%%=              
                                          -#%#++*****************######################%-:========-++#%%%%%%%%+:            
                                     :--*%%***************###########################%%=::======+%@@%%@@%%%%%%*+*           
                                  .-+*###***********#################################%+::====+--:--:%@%*+=--=++++*-         
                             :***********+=+++++++++++****==******++++*##%%%%%%%%#*-=:::=%@+####**##+:::::=++++++**=        
                        .-************************+=-=+****************++==-------::-::--++*+:::-:::::::-++++***+*#+        
                   :*************************=---++*+*+*********++=-----------::::=--:::=++*:::::::.:-*+*######+*+**        
               :**********++++**+=--------==------::--------------------:::---:::::::::::--::::-+*#############+#**#-       
            .**#**+----------+--------==-----------------==------------==--::::::::::::::-+###################**####@       
           =#+=##-----------=---=++====================--========--==+===:::::::::::::-+***###################+#*#*#%.      
           %#+=++***++==----+*+-----======================++++++=-=++===-:::::::---:-*****####**********#********+#+#       
          -%#****%@%@@%#=--++-..####%%%%%#*++==------==+++*@@*-*+##:+==--::::::--:=*%@@@#*#*#****************=**#*#*#       
          *#*#=#*%@@%%@@%%#@%%%.@@%@#@%@%@%@%%%+-##=+=**#*%%%#%#%@#%%%*=+=--::::-******+#%******************=***#%*%#       
          ##-+##+@@@%%@@%@%%@@%%@%@@@@@@@%@%@@#*%##++++==*+-%**%%%%#*=******=---##%%@%%###********************+%#*=%*       
         :#%%#**+%@@%@@@@@@%%%@@@@@@@@@@%@@@@*#%%****#***#%%%%#+=+*#####****++*#%@@%@%%@@%##***********#******%@%*%%-       
         *%%%%###=%@@@@@@@@@@@@@@@@@@@@@@@@%++--===-----=+######%%%########****@@%@%@%@@*%%%##****#********#%@@@@***.       
        *+#%%%%%%%%%#*+*#%@@@@@@%@@@@@@%#*+****+++++***#######%%%%%%##########%%@%%%%@#%@@%#%#********#=.  +@@@@@##+        
         -#+#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%######***#####%%%%%%%%####***####%##%%%%%%#%@%%%%%%##**##=           ...          
         =+++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*+=---------===--:-+#%#@@@%*=*%#%%###*%#*-                            
         ##*+#%##@%#%%@%%##%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%@@@@@@@@@@@%%*####%@%%%#%#*%@@%%%#.                             
          =##%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%++++*++++***####%@@%%#*%#*%#@##@#%@%%#+%*                              
              .=%**###@@%%#%%@@@%%%%##%%%%%@@%%%%##%*+===++++=+######%#%%##*%@@*@#*%%@@#%%###.                              
                      .-+*#**#****##%%%%%%%%%%%%#*++%%%%%%%%%%##******#%####@%%%%%%@@%@%%*##:                               
                                      ...:::--=====----::::::------:-@@@@@%%%%@@#@@%%%%#+%#.                                
                                                                      :@@@@%%%%*#%%##*%%#=                                  
                                                                        .*@@@%%%%%%%%%#.                                    
                                                                               ...                                          """)
    menu_principal()
