import hashlib
import mdpauth
def main():
    # entrer les id et mdp
    print ("Connexion au coffre fort \n")
    (identifiant, authentifié) = authentification()
    # print(authentifié)
    while (authentifié == 0) :
        print("Identifiant ou mot de passe incorrect. Réessayez \n")
        (identifiant, authentifié) = authentification()
    
    print("Bienvenue " + identifiant + "\n")


def authentification():
    identifiant = str(input("Identifiant : "))
    mdp = str(input("Mot de passe : "))

    # print('Identifiant = ' + identifiant + '\n')
    # print('mdp = ' + mdp + '\n')
    mdphash = (hashlib.sha256(mdp.encode('utf-8'))).hexdigest()
    # print('mdp hashé = ' + mdphash)
    # print(mdphash)
    id = {identifiant : mdphash}
    # print(id)
    # print(mdpauth.auth)
    # verifier que l'id est dans les les clés de mdpauth
    if identifiant in mdpauth.auth.keys() :
        if mdpauth.auth[identifiant] == mdphash :
            authentifié = 1
        else : 
            authentifié = 0
    else : 
        authentifié = 0
    
    identifiant = "null"
    mdp = "null"
    mdphash = "null"
    return (identifiant, authentifié)

main()
