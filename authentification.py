# coding=UTF-8
import hashlib
import csv
from getpass import getpass
import os
import math
from Crypto.Cipher import AES
import ast
# from pythonfuzz.main import PythonFuzz


# @PythonFuzz
def main():
    # entrer les id et mdp
    print ("Connexion au coffre fort \n")
    registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
    if registered == 'connexion' :
        (identifiant, authentifie, key) = authentification()
    elif registered == 'inscription': 
        (identifiant, authentifie, key) = inscription()
    else :
        print("Mauvaise commande")
        authentifie = 0
    # print(authentifie)
    while (authentifie == 0) :
        registered = str(input("Voulez-vous vous connecter ou vous inscrire? (tapez \"connexion\" ou \"inscription\") : "))
        if registered == 'connexion' :
            (identifiant, authentifie, key) = authentification()
        elif registered == 'inscription' :
            (identifiant, authentifie, key) = inscription()
        else : 
            print("Mauvaise commande")
            authentifie = 0
    
    print("Bienvenue " + identifiant + "\n")
    #print(key)
    while (authentifie == 1):
        authentifie = action(identifiant, key)
    print ("AU REVOUARE")



def authentification():
    identifiant = str(input("Identifiant : "))
    mdp = str(getpass("password: "))
    keyuser = ''
    # print('Identifiant = ' + identifiant + '\n')
    # print('mdp = ' + mdp + '\n')
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    # print('mdp hashe = ' + mdphash)
    # print(mdphash)
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
                    return (identifiant, authentifie, keyuser)
    authentifie = 0
    print("Identifiant ou mot de passe incorrect. Reessayez \n")
    return (identifiant, authentifie, keyuser)

def inscription():
    identifiant = str(input("Veuillez rentrez un identifiant : "))
    mdp = str(getpass("Veuillez rentrez un mot de passe : "))
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
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
        #print(keyuser)
        #print(salt)
        #print(encrypted)

        fieldnames = ['id', 'mdp', 'key']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow({'id': identifiant, 'mdp': mdphash, 'key' : encrypted})
    return (identifiant, authentifie, encrypted)


def action(identifiant, key):
    entree = str(input("Que souhaitez-vous faire ? \n Tapez \"enregistrer\" pour enregistrer un nouveau mot de passe \n Tapez \"consulter\" pour consulter un mot de passe \n Tapez \"deconnexion\" pour vous déconnecter \n"))
    if entree == 'enregistrer' :
        enregistrer(identifiant, key)
        return 1
    elif entree == 'consulter': 
        consulter(identifiant, key)
        return 1
    elif entree == 'deconnexion' : 
        return 0
    else :
        print("Mauvaise commande")
        return 1


def enregistrer(identifiant, keyuser) :
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
        salt = os.urandom(16)
        derived = hashlib.pbkdf2_hmac('sha256', keyuser, salt, 100000, dklen=48)
        iv = derived[0:16]
        key = derived[16:]
        encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(mdp.encode('utf-8'))
        #print(keyuser)
        #print(salt)
        #print(encrypted)
        ### AJout dans le dictionnaire
        fieldnames = ['user', 'site', 'id', 'mdp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow({'user' : identifiant, 'site' : site, 'id': id, 'mdp': encrypted})
        print("Le mot de passe a bien été ajouté ! \n")

def consulter(identifiant, keyuser) : 
    print ("Fonction consulter")
    site = str(input("Veuillez rentrez le site associé au mot de passe à consulter : "))
    with open('mdp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['user'] == identifiant and row['site'] == site:
                encrypted = ast.literal_eval(row['mdp'])
                salt = encrypted[0:16]
                derived = hashlib.pbkdf2_hmac('sha256', keyuser, salt, 100000, dklen=48)
                iv = derived[0:16]
                key = derived[16:]
                mdp = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[16:])
                print(keyuser)
                print("L'id est : " + row['id'] + "\n")
                print("Le mot de passe est : " + mdp.decode() + "\n")
                return 
        print("Vous n'avez pas de mot de pass associé à ce site !")


if __name__ == "__main__":
    # execute only if run as a script
    main()