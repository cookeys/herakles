#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyFingerprint <export_fg>
Copyright (C) 2019 Julien Charlent <julien.charlent@gmail.com>
All rights reserved.

"""

## Statut :
## Code : OK
## Langue : OK

import time
import os
import tempfile
import datetime
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
print("Bienvenue sur le module d'exportation d'empreinte digitale")
print("Emplacements utilisés dans le capteur: " + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Lit et exporte au format .bmp l'empreinte digitale
try:
    print("Présentez le doigt... \n")

    ## Attendre que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass

    ## Edition du nom de fichier
    id_user = raw_input("ID utilisateur : ")
    id_sensor = 0
    fingerName = raw_input("Doigt enregistré : ")
    dateNow = datetime.datetime.today().strftime('%Y_%m_%d')

    imageDestination =  tempfile.gettempdir() + '/FG/' + id_user + fingerName +'_' + dateNow + '_FG' + '.bmp'

    print("Stockage de l'image (temps estimé : 20 secondes)")

    f.downloadImage(imageDestination)

    print("L'image a été sauvegardée à : " + imageDestination + ".")

except Exception as e:
    print("Echec de l'opération")
    print("Message d'erreur : " + str(e))
    exit(1)
