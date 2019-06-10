#!/usr/bin/env python2
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
print("0 - Tester la connexion à la base de données")
print("1 - Enregistrer une nouvelle empreinte")
print("2 - Rechercher si une empreinte est enregistrée dans le capteur et la base de données")
print("3 - Permet uniquement d'exporter une empreinte au format .bmp")
print("4 - Supprimer une empreinte du capteur et de la base de données")
print("5 - Montrer l'index des emplacements du capteur")


userChoice = 'y'
userChoice = str(userChoice)
while userChoice == 'y':
    f = raw_input("Indiquez votre choix (0-5) : ")
    try:
        f = int(f)

        if f == 0:
            import connect
            pass

        if f == 1:
            import enroll_new_fg
            pass

        if f == 2:
            import identifier
            pass

        if f == 3:
            import export_fg
            pass

        if f == 4:
            import delete
            pass  

        if f == 5:
            import index
            pass
            
        userChoice = raw_input("Voulez vous executer un autre script ? (y/n)\n")
    except ValueError:
        print("Choisissez une valeur comprise entre 1 et 5")

    
