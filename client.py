import socket 
import threading
from rsa import *
from interface import *

user = User();

gui_thread = threading.Thread(target=user.main)
gui_thread.start()


user.enterText('Génération des clé en cours...')
key = genRsaKeyPair(512)
user.setUserKey(key)
user.enterText('Entrez votre pseudo et la clé publique de votre interlocuteur')

# Choosing Nickname
while True:
    if user.completed() == True:
        break
print("sal")
'''
    On se connecte au server
    Le client a besoin de deux thread, un qui va recevoir constamment
    les données du serveur et le deuxieme qui va envoyer nos messages 

'''
''''''
#Connection To Server
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',5555))

'''
    Fonction qui va constamment recevoir les messages et les afficher sur l'écran
    Si on recoit le message 'NICK' on envoie notre pseudo
    sinon il y a une erreur alors on arrete la connexion avec le serveur
    et notre boucle
'''
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            first_word = message.split(' ', 1)[0]
            
            if message == 'NICK':
                client.send(user.nickname.encode('ascii'))
            elif first_word == '-':
                split_m = message.split(' ', 2)
                if split_m[1] != user.nickname+":":
                    dec_m = rsa_dec(int(split_m[2]),user.myKey[1])
                    user.enterText(split_m[0] + split_m[1] + " " + str(dec_m))
                else:
                    user.enterText(split_m[0] + split_m[1] + " " + user.message)
            else: 
                user.enterText(message)
        except:
            # Close Connection When Error
            print("Une erreur !\n, Avez vous bien renseigné une bonne clé ?")
            client.close()
            break

'''
    La fonction v attendre que l'on envoie un message
'''
# Sending Messages to Server
def write():
    while True:
        if user.text != "":
            user.message = user.text 
            enc_m = rsa_enc(user.message,user.notMyKey)
            message = '- {}: {}'.format(user.nickname, enc_m)
            client.send(message.encode('ascii'))
            user.text = ""
'''
    Deux threads qui vont lancer les deux fonctions
'''
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
