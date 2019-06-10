#!/usr/bin/env python3
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
import hashlib
import mysql.connector
import time
import datetime
from mysql.connector import Error
from mysql.connector import errorcode

print("Verion : 1.0")
print("Bienvenue sur le programme d'identification CERBEROS")
a = input("Appuyez sur ENTREE dès que toutes les valeurs sont envoyées par les modules à la BDD")

connection = mysql.connector.connect(host='192.168.1.10',
                                 database='cerberos',
                                 user='cerberos',
                                 password='databasecerberos2019')

cursor = connection.cursor()

def userCheck():
    if int(fgUser) == int(fcUser) == int(gtUser):
        global id_user
        id_user = fgUser

        global dateNow
        dateNow = datetime.datetime.now()
        dateNowSQL= dateNow.strftime('%Y-%m-%d')

        ## PARTIE COMPARAISON EXPIRATION
        sql_search_query = """ SELECT expiration_date FROM users WHERE id_user="%s" """
        cursor.execute(sql_search_query, (id_user,))
        record = cursor.fetchall()

        for row in record:
              global expDate
              expDate = row[0]
              expDateSQL = expDate.strftime('%Y-%m-%d')

              if dateNowSQL < expDateSQL:
                print("\nExpiration du profil N°" + str(id_user) +" le " + expDate.strftime('%d-%m-%Y'))
              else:
                raise Exception("Profil expiré - ACCES REFUSE")
                 
            
        pass

    else:
        raise Exception('Les données récupérées ne proviennent pas du même utilisateur')
         

def databaseRecoverResults():
    try:
       ## PARTIE EMPREINTE (MIDAS)
       sql_search_query = """ SELECT score, id_user FROM results WHERE id_sensor=0 ORDER BY timestamp DESC LIMIT 1  """
       cursor.execute(sql_search_query)
       record = cursor.fetchall()

       for row in record:
            global fgScore
            fgScore = row[0]
            global fgUser
            fgUser = row[1]

            ## A SUPPRIMER APRES ESSAIS
            print("\nScore empreinte "+ str(fgScore))
            print("Utilisateur N°"+ str(fgUser))

       ## PARTIE VISAGE (CYCLOP)
       sql_search_query = """ SELECT score, id_user FROM results WHERE id_sensor=1 ORDER BY timestamp DESC LIMIT 1  """
       cursor.execute(sql_search_query)
       record = cursor.fetchall()

       for row in record:
            global fcScore
            fcScore = row[0]
            global fcUser
            fcUser = row[1]

            ## A SUPPRIMER APRES ESSAIS
            print("\nScore visage "+ str(fcScore))
            print("Utilisateur N°"+ str(fcUser))

       ## PARTIE DEMARCHE (ZEUS)
       sql_search_query = """ SELECT score, id_user FROM results WHERE id_sensor=2 ORDER BY timestamp DESC LIMIT 1  """
       cursor.execute(sql_search_query)
       record = cursor.fetchall()

       for row in record:
            global gtScore
            gtScore = row[0]
            global gtUser
            gtUser = row[1]

            ## A SUPPRIMER APRES ESSAIS
            print("\nScore demarche "+ str(gtScore))
            print("Utilisateur N°"+ str(gtUser))

    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table {}".format(error))
         

    finally:
        userCheck()
        pass

def databaseClose(): 
    if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("Connexion à MySQL fermée")

def databaseInsertResults():
    try:
       sql_insert_query = """ INSERT INTO `access`
                              (`id_user`, `final_score`) VALUES ("%s", "%s")"""

       cursor.execute(sql_insert_query, (id_user, final_score))
       connection.commit()

       print ("\nEntrée sauvegardée dans la table 'access' avec succès")
       
    except mysql.connector.Error as error :
        connection.rollback() ## Rollback en cas d'erreur
        print("Impossible d'enregistrer l'entrée dans la table access {}".format(error))
         

    finally:
        databaseClose()
        pass

## Recuperation des resultats
databaseRecoverResults()

## Conversion des valeurs en int
fgScore = int(fgScore)
fcScore = int(fcScore)
gtScore = int(gtScore)

## (Variable empreinte /val. max (108)) * 100 ###
fgScore = round(fgScore/108*100)
print("\nPourcentage empreinte : " + str(fgScore) + "%")

## (Variable visage /val. max) * 100 ###-->  A CHANGER QUAND SCRIPT OP
fcScore = round(fcScore/130*100)
print("\nPourcentage visage : " + str(fcScore) + "%")

## (Variable démarche / val. max) * 100 ###-->  A CHANGER QUAND SCRIPT OP
gtScore = round(gtScore/108*100)
print("\nPourcentage allure : " + str(gtScore) + "%")

## (val_dem + val_vis + val_emp) / 3 # = %rec Donc moyenne sur 100 (pourcentage)
final_score = fgScore + fcScore + gtScore
final_score = int(final_score) / 3
final_score = round(final_score)
print("\nPourcentage final : " + str(final_score) + "%")

databaseInsertResults()

#Si %rec < 60 && %rec > 40 ->> Appel opérateur vérification manuelle


### Si l'un des pourcentage est en dessous de x% on

if final_score > 60:
    print("\nACCES AUTORISE ET CONFIRME")

if final_score <= 60 and final_score >= 40:
    print("\nNECESSITE DE REPASSER LE TEST")
# -> Edition base de données pour intervention operateur et acces ou non au site (BOOLEAN : TRUE / FALSE)

#Si %rec < 40 ->> Alerte intrusion opérateur
if final_score < 40:
    print("\nACCES REFUSE !")

a = input("\nProgramme terminé")
