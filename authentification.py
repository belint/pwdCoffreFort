import hashlib
import csv
from getpass import getpass
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
        fieldnames = ['id', 'mdp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow({'id': identifiant, 'mdp': mdphash})
    return (identifiant, authentifie)
main()
