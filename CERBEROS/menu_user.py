#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyFingerprint <identifier>
Copyright (C) 2019 Julien Charlent <julien.charlent@gmail.com>
All rights reserved.

"""

## Statut :
## Code : OK
## Langue : OK

import os

print("## Bienvenue sur le selecteur de programme d'empreinte digitale ##")
print("Choisissez l'une des options suivantes :")
print("0 - Lancer le programme d'analyse CERBEROS")
print("1 - Enregistrer un nouveau profil dans la base de données")
print("2 - Modifier la date d'expiration d'un profil")

userChoice = 'y'
userChoice = str(userChoice)
while userChoice == 'y':
    f = input("Indiquez votre choix (0-2) : ")
    try:
        f = int(f)

        if f == 0:
            import cerberos_main_soft
            pass

        if f == 1:
            import new_user
            pass

        if f == 2:
            import exp_user
            pass

        userChoice = input("Voulez vous executer un autre script ? (y/n)\n")

    except ValueError:
        print("Choisissez une valeur comprise entre 0 et 2")

    
