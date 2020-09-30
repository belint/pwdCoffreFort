import hashlib
import mdpauth
from getpass import getpass
def main():
    # entrer les id et mdp
    print ("Connexion au coffre fort \n")
    registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
    if registered == 'connexion' :
        (identifiant, authentifie) = authentification()
    else: 
        (identifiant, authentifie) = inscritpion()
    # print(authentifie)
    while (authentifie == 0) :
        registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
        if registered == 'connexion' :
            (identifiant, authentifie) = authentification()
        else: 
            (identifiant, authentifie) = inscritpion()
    
    print("Bienvenue " + identifiant + "\n")


def authentification():
    identifiant = str(input("Identifiant : "))
    mdp = str(getpass("password: "))
    
    # print('Identifiant = ' + identifiant + '\n')
    # print('mdp = ' + mdp + '\n')
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    # print('mdp hashe = ' + mdphash)
    # print(mdphash)
    id = {identifiant : mdphash}
    # print(id)
    # print(mdpauth.auth)
    # verifier que l'id est dans les les cles de mdpauth
    if identifiant in mdpauth.auth.keys() :
        if mdpauth.auth[identifiant] == mdphash :
            authentifie = 1
        else : 
            print("Identifiant ou mot de passe incorrect. Reessayez \n")
            authentifie = 0
    else :
        mdpauth.auth.update(id)
        authentifie = 0
    
    mdp = ""
    mdphash = ""
    return (identifiant, authentifie)

def inscritpion():
    identifiant = str(input("Veuillez rentrez un identifiant : "))
    mdp = str(getpass("Veuillez rentrez un mot de passe : "))
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    id = {identifiant : mdphash}
    if identifiant in mdpauth.auth.keys() :
        print("Cette identifiant existe déjà! Veuillez-vous connecter")
        authentifie = 0
    else:
        ### AJout dans le dictionnaire
        authentifie = 1
    identifiant = ""
    mdp = ""
    mdphash =""
    return (identifiant, authentifie)
main()
