#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyFingerprint <enroll_new_fg>
Copyright (C) 2019 Julien Charlent <julien.charlent@gmail.com>
All rights reserved.

"""

## Statut :
## Code : OK
## Langue : OK

import mysql.connector
import time
import os
import tempfile
import datetime
from pyfingerprint.pyfingerprint import PyFingerprint
from mysql.connector import Error
from mysql.connector import errorcode

## DEFINITION FONCTION DATABASE

def databaseEnroll():
    try:
       connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='midas',
                                 password='databasecerberos2019')

       cursor = connection.cursor()

       sql_insert_query = """ INSERT INTO `registered`
                              (`id_sensor`, `id_user`, `attribute` , `position`) VALUES ("%s", "%s", "%s", "%s")"""
       cursor.execute(sql_insert_query, (id_sensor, id_user, fingerName, positionNumber))
       connection.commit()

       print ("Entrée sauvegardée dans la table 'registered' avec succès")
       print('Entrée sauvegardée dans le capteur avec succès')
       print("Position de l'empreinte dans le capteur: " + str(positionNumber))

    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table {}".format(error))

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

## Affiche les données sur le capteur
print("Bienvenue sur le module d'enregistrement d'empreinte digitale")
print("Emplacements utilisés dans le capteur : " + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Enregistrement de l'empreinte dans la BDD et le capteur
try:
    print("Présentez le doigt...")

    ## Attendre que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass

    ## Convertis l'image lue en caractéristiques et la stocke en charbuffer 1
    f.convertImage(0x01)

    ## Recherche les caractéristiques de l'image dans le capteur
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print("Empreinte déjà enregistrée !")
        print("Correspondance trouvée à l'emplacement N°" + str(positionNumber))
        exit(0)

    print("Retirez le doigt")
    time.sleep(1)

    print("Re-présentez le doigt...")

    ## Attendre que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass
    
    ## Convertis l'image lue en caractéristiques et la stocke en charbuffer 2
    f.convertImage(0x02)
    
    ## Compare les caractéristiques des deux images
    if ( f.compareCharacteristics() == 0 ):
        raise Exception("Les doigts ne correspondent pas !")

    ## Attente que le lecteur lise le doigt
    while ( f.readImage() == False ):
        pass

    ## Edition du nom de fichier
    global id_user
    id_user = raw_input("ID utilisateur : ")
    id_sensor = 0
    fingerName = raw_input("Doigt enregistré : ")
    dateNow = datetime.datetime.today().strftime('%Y_%m_%d')

    imageDestination =  tempfile.gettempdir() + '/FG/' + id_user + fingerName +'_' + dateNow + '_FG' + '.bmp'

    print("Stockage de l'image (temps estimé : 20 secondes)")

    f.downloadImage(imageDestination)

    print("L'image a été sauvegardée à : " + imageDestination + ".")
    id_user = int(id_user)
    ## Crée un template de l'empreinte
    f.createTemplate()
    
    ## Sauvegarde l'empreinte dans un emplacement vide du capteur
    positionNumber = f.storeTemplate()

    ## Sauvegarde l'entrée dans la base de données
    databaseEnroll()
        

except Exception as e:
    print("Echec de l'opération")
    print("Message d'erreur : " + str(e))
    exit(1)
