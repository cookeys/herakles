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
import mysql.connector
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from mysql.connector import Error
from mysql.connector import errorcode


## DEFINITION DES FONCTIONS

def databaseResult():
    try:
       connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='midas',
                                 password='databasecerberos2019')

       cursor = connection.cursor()
       sql_search_query = """ SELECT id_user FROM registered WHERE position="%s" """
       cursor.execute(sql_search_query, (positionNumber,))
       record = cursor.fetchall()

       for row in record:
            id_user = row[0]
            print("Utilisateur N°"+ str(id_user))
       id_user = int(id_user)
       sql_insert_query = """ INSERT INTO `results`
                              (`id_sensor`, `id_user`, `score`) VALUES (0, "%s", "%s")"""

       cursor.execute(sql_insert_query, (id_user, accuracyScore))
       connection.commit()

       print("Entrée sauvegardée dans la table 'results' avec succès")
       print("Position de l'empreinte dans le capteur : " + str(positionNumber))

    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table results {}".format(error))

    finally:
        ## Fermeture de la base de données
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Connexion à MySQL fermée")
            a = raw_input("\nProgramme terminé, passez au module suivant")

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
print("Bienvenue sur le module d'identification d'empreinte digitale")
print("Emplacements utilisés dans le capteur : " + str(f.getTemplateCount()) +"/"+ str(f.getStorageCapacity()))

## Cherche l'empreinte dans les emplacements du capteur
try:
    print("Présentez le doigt... \n")

    ## Attendre que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass

    ## Convertis l'image lue en caractéristiques et la stocke en charbuffer 1
    f.convertImage(0x01)

    ## Recherche les caractéristiques de l'image dans le capteur
    result = f.searchTemplate()
    global positionNumber
    positionNumber = result[0]
    positionNumber = int(positionNumber)
    accuracyScore = result[1]
    accuracyScore = int(accuracyScore)

    if ( positionNumber == -1 ):
        print('Aucun match trouvé !')
        accuracyScore = 0
        
    else:
        print("Correspondance trouvée à l'emplacement N°" + str(positionNumber))
        print("Score : " + str(accuracyScore) + " /108")
        databaseResult()


except Exception as e:
    print("Echec de l'opération")
    print("Message d'erreur : " + str(e))
    exit(1)
