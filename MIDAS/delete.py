#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyFingerprint <delete>
Copyright (C) 2019 Julien Charlent <julien.charlent@gmail.com>
All rights reserved.

"""

## Statut :
## Code : OK
## Langue : OK

import mysql.connector
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from mysql.connector import Error
from mysql.connector import errorcode

## DEFINITION DES FONCTIONS

def databaseDelete():
    try:
       connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='midas',
                                 password='databasecerberos2019')

       cursor = connection.cursor(buffered=True)

       ## Supprime l'entrée de la BDD
       sql_Delete_query = """DELETE FROM registered WHERE position = %s"""
       cursor.execute(sql_Delete_query, (positionNumber,))
       connection.commit()
       print(cursor.rowcount, "Entree.s supprimee de la BDD")

    except mysql.connector.Error as error :
        print("Impossible de supprimer l'entrée : {}".format(error))

    finally:
         ## Fermeture de la base de données
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Connexion à MySQL fermée")

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

print("Bienvenue sur le module de suppression d'empreinte digitale")

userChoice = 'y'
userChoice = str(userChoice)
while userChoice == 'y':
## Effacement de l'empreinte digitale du capteur
    try:
## Affiche les données sur le capteur       
        print("Emplacements utilisés dans le capteur: " + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        positionNumber = raw_input("Entrez l'emplacement à supprimer : ")
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print("Empreinte supprimée avec succès : ")
            databaseDelete()
            userChoice = raw_input("Voulez vous en supprimer d'autres ? (y/n)\n")

    except Exception as e:
        print("Echec de l'opération")
        print("Message d'erreur : " + str(e))
        exit(1)

