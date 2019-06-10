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
from mysql.connector import Error
from mysql.connector import errorcode

## DEFINITION FONCTION DATABASE

connection = mysql.connector.connect(host='192.168.1.10',
                        database='cerberos',
                        user='cerberos',
                        password='databasecerberos2019')
cursor = connection.cursor()
 
def databaseClose():
 ## Fermeture de la base de données
        if(connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connexion à MySQL fermée")


def databaseID():
    sql_search_query = """ SELECT id_user FROM users WHERE full_name=%s ORDER BY registration_date DESC LIMIT 1 """
    cursor.execute(sql_search_query, (full_name,))
    record = cursor.fetchall()
  
    for row in record:
        global id_user
        id_user = row[0]
  
    print ("Profil sauvegardé dans la table 'users' avec pour ID N°" + str(id_user) + " avec succès")
    databaseClose()



def databaseEnroll():
    try:
        sql_insert_query = """ INSERT INTO `users`
                              (`full_name`, `registration_date`, `expiration_date`) VALUES (%s, %s, %s)"""
        cursor.execute(sql_insert_query, (full_name, dateNowSQL, expDateSQL))
        connection.commit()
        databaseID()

    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table {}".format(error))


## Edition du nom de fichier
global full_name
full_name = input("Nom complet : ")

global dateNow
dateNow = datetime.datetime.now()
dateNowSQL= dateNow.strftime('%Y-%m-%d')


global expiration_date
expDate = dateNow + datetime.timedelta(days=365)
expDateSQL = expDate.strftime('%Y-%m-%d')

## Sauvegarde l'entrée dans la base de données
databaseEnroll()
