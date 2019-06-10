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

import hashlib
import time
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
print("Bienvenue sur le module de recherche d'empreinte digitale")
print("Emplacements utilisés dans le capteur: " + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Lit et exporte au format .bmp l'empreinte digitale
try:
    print("Présentez le doigt... \n")

    ## Attendre que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass

    ## Convertis l'image lue en caractéristiques et la stocke en charbuffer 1
    f.convertImage(0x01)

    ## Recherche les caractéristiques de l'image dans le capteur
    result = f.searchTemplate()
    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('Aucun match trouvé !')
        accuracyScore = 0
        
    else:
        print("Correspondance trouvée à l'emplacement N°" + str(positionNumber))
        print("Score : " + str(accuracyScore) + " /108")


except Exception as e:
    print("Echec de l'opération")
    print("Message d'erreur : " + str(e))
    exit(1)
