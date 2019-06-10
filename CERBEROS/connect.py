#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyFingerprint <connect>
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


try:
       connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='cerberos',
                                 password='databasecerberos2019')

       cursor = connection.cursor()
       if(connection.is_connected()):
            db_Info = connection.get_server_info()  
            print("Connected to MySQL database")  
            a = input("Appuyez sur entrée pour fermer la connexion")
            
except mysql.connector.Error as error:
    connection.rollback() ## Rollback en cas d'erreur
    print("Impossible d'enregistrer l'entrée dans la table {}".format(error))

finally:
 ## Fermeture de la base de données
    if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Connexion à MySQL fermée")
