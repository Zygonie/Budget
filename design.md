# Design de l'application

## Schéma de données

class Année
    jours
    année
    montant début
    montant fin

class Jour
    date
    opérations
    jour_in (jour précédent)
    valeur_out (fin de journée)


class Operation
    date
    montant
    mode de paiement (comptant, crédit)
    récurrence (fréquence, début, fin)

Comment faire pour calculer chaque jour ?
  Pour une année en particulier, on connait le montant du début (au 1er janvier minuit). On définit une liste de `Jour` en commençant par le 1er janvier. On ajoute à partir de la BD `Operation` toutes les opérations d'une même journée. On met à jour la valeur de fin de journée et on passe au jour suivant.