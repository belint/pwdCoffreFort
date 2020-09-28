import hashlib

def main():
    # entrer les id et mdp
    print ("Connexion au coffre fort \n")
    authentification()
    # chiffrer le mdp
    # ouvrir le fichier

def authentification():
    identifiant = str(input("Identifiant : "))
    mdp = str(input("Mot de passe : "))

    print('Identifiant = ' + identifiant + '\n')
    print('mdp = ' + mdp + '\n')
    mdphash = hashlib.sha256(mdp.encode('utf-8'))
    # print('mdp hashé = ' + mdphash)
    print(mdphash.hexdigest())
    id = {identifiant : mdphash}

main()