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

from pyfingerprint.pyfingerprint import PyFingerprint

## Initialisation du capteur
try:
    ## Windows
    #f = PyFingerprint('COM10', 57600, 0xFFFFFFFF, 0x00000000)
    ## Debian
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError("Mot de passe du capteur d'empreinte digitale incorrect")

except Exception as e:
    print("Impossible d'initialiser le capteur d'empreinte digitale")
    print("Message d'erreur : " + str(e))
    exit(1)

## Affiche les données sur le capteur
print("Bienvenue sur le module d'index d'emplacement du capteur d'empreinte digitale")
print("Emplacements utilisés dans le capteur: " + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Affiche l'index d'emplacement du capteur d'empreinte digitale
try:
    page = raw_input("Entre la page de l'index (0, 1, 2, 3) que vous souhaitez voir : ")
    page = int(page)

    tableIndex = f.getTemplateIndex(page)
    entries = raw_input("Quelles entrées voulez voir (De 0 à x) (xMax=255) : ")

    for i in range(0, int(entries)):
        print("L'entrée N°" + str(i) + " est utilisée : " + str(tableIndex[i]))
    print("\nFalse : L'entrée n'est pas utilisée")
    print("True : L'entrée est utilisée")


except Exception as e:
    print("Echec de l'opération")
    print("Message d'erreur : " + str(e))
    exit(1)
