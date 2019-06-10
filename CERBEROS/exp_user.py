#!/usr/bin/env python3
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
from mysql.connector import Error
from mysql.connector import errorcode

print("Verion : 1.0")
print("Bienvenue sur le programme de modification de la date d'expiration du profil")

## DEFINITION FONCTION DATABASE

def databaseEnroll():
    try:
        
        connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='cerberos',
                                 password='databasecerberos2019')

        cursor = connection.cursor()
        sql_insert_query = """ UPDATE `users`
                              SET `expiration_date`=%s WHERE id_user=%s """
        cursor.execute(sql_insert_query, (expDate, id_user))
        connection.commit()

        print ("Entrée sauvegardée dans la table 'users' avec succès")

    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table {}".format(error))

    finally:
 ## Fermeture de la base de données
        if(connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connexion à MySQL fermée")


## Edition du nom de fichier
global id_user
id_user = input("ID user : ")
id_user = int(id_user)


global expDate
expAnnee = input("Entrez l'année' d'expiration : ")
expMois = input("Entrez le mois d'expiration : ")
expJour = input("Entrez le jour d'expiration : ")
expDate = expAnnee + expMois + expJour

## Sauvegarde l'entrée dans la base de données
databaseEnroll()
