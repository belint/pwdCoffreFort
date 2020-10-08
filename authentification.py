import hashlib
import csv
from getpass import getpass
import os
import math
from Crypto.Cipher import AES
import ast
def main():
    # entrer les id et mdp
    print ("Connexion au coffre fort \n")
    registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
    if registered == 'connexion' :
        (identifiant, authentifie) = authentification()
    elif registered == 'inscription': 
        (identifiant, authentifie) = inscription()
    else :
        print("Mauvaise commande")
        authentifie = 0
    # print(authentifie)
    while (authentifie == 0) :
        registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
        if registered == 'connexion' :
            (identifiant, authentifie) = authentification()
        else: 
            (identifiant, authentifie) = inscription()
    
    print("Bienvenue " + identifiant + "\n")

    while (authentifie == 1):
        authentifie = action(identifiant)
    print ("AU REVOUARE")



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
    with open('mdpauth.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == identifiant :
                if row['mdp'] == mdphash :
                    authentifie = 1
                    encrypted = ast.literal_eval(row['key'])
                    print(type(encrypted))
                    salt = encrypted[0:16]
                    print(salt)
                    derived = hashlib.pbkdf2_hmac('sha256', mdp.encode('utf-8'), salt, 100000, dklen=48)
                    iv = derived[0:16]
                    key = derived[16:]
                    keyuser = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[16:])
                    print(keyuser)
                    break
                else : 
                    print("Identifiant ou mot de passe incorrect. Reessayez \n")
                    authentifie = 0
            else :
                authentifie = 0
    
    return (identifiant, authentifie)

def inscription():
    identifiant = str(input("Veuillez rentrez un identifiant : "))
    mdp = str(getpass("Veuillez rentrez un mot de passe : "))
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    id = {identifiant : mdphash}
    with open('mdpauth.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == identifiant :
                print("Cet identifiant existe déjà! Veuillez-vous connecter")
                authentifie = 0
                return (identifiant, authentifie)
    with open('mdpauth.csv', 'a', newline='') as csvfile:
        ### AJout dans le dictionnaire
        authentifie = 1
        keyuser = os.urandom(32)
        salt = os.urandom(16)
        derived = hashlib.pbkdf2_hmac('sha256', mdp.encode('utf-8'), salt, 100000, dklen=48)
        iv = derived[0:16]
        key = derived[16:]
        encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(keyuser)
        print(keyuser)
        print(salt)
        print(encrypted)

        fieldnames = ['id', 'mdp', 'key']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow({'id': identifiant, 'mdp': mdphash, 'key' : encrypted})
    return (identifiant, authentifie)


def action(identifiant):
    entree = str(input("Que souhaitez-vous faire ? \n Tapez \"enregistrer\" pour enregistrer un nouveau mot de passe \n Tapez \"consulter\" pour consulter un mot de passe \n Tapez \"deconnexion\" pour vous déconnecter \n"))
    if entree == 'enregistrer' :
        enregistrer(identifiant)
        return 1
    elif entree == 'consulter': 
        consulter(identifiant)
        return 1
    elif entree == 'deconnexion' : 
        return 0
    else :
        print("Mauvaise commande")
        return 1


def enregistrer(identifiant) :
    print("Fonction enregistrer")
    site = str(input("Veuillez rentrez le site associé au mot de passe : "))
    id = str(input("Veuillez rentrez l'id : "))
    mdp = str(getpass("Veuillez rentrez le mot de passe : "))
    # mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    # id = {identifiant : mdphash}
    with open('mdp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['user'] == identifiant and row['site'] == site:
                print("Vous avez déjà un mot de passe pour ce site")
                return 
    with open('mdp.csv', 'a', newline='') as csvfile:
        ### AJout dans le dictionnaire
        fieldnames = ['user', 'site', 'id', 'mdp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow({'user' : identifiant, 'site' : site, 'id': id, 'mdp': mdp})
        print("Le mot de passe a bien été ajouté ! \n")

def consulter(identifiant) : 
    print ("Fonction consulter")
    site = str(input("Veuillez rentrez le site associé au mot de passe à consulter : "))
    with open('mdp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['user'] == identifiant and row['site'] == site:
                print("L'id est : " + row['id'] + "\n")
                print("Le mot de passe est : " + row['mdp'] + "\n")
                return 
        print("Vous n'avez pas de mot de pass associé à ce site !")




main()