import subprocess
import os

while True:
    commande = input(os.getcwd()+" > ")
    if commande == "exit":
        break
    commande = commande.split(" ")
    if len(commande) == 2 and commande[0] == "cd":
        try:
            os.chdir(commande[1])
        except:
            print("le chemin spécifié est introuvable")
    else:
        resultat = subprocess.run(commande,shell=True,capture_output=True,universal_newlines=True)
        if resultat.returncode != 0:
            print("Erreur,commande non reconnu")
        else:
           print(resultat.stdout)