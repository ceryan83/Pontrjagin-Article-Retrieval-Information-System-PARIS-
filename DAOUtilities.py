# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 10:04:25 2020

@author: cerya
"""
import psycopg2
   
def getConnection():        
    try:
        connection = psycopg2.connect(user = 'postgres',
                                      password = '4rt1n14n',
                                      host = '127.0.0.1',
                                      port = '5432',
                                      dbname = 'Pontrjagin',
                                      gssencmode = 'disable')
    
        cursor = connection.cursor()
    
        # Print PostgreSQL version
        cursor.execute('SELECT version();')
        record = cursor.fetchone()
        print('You are connected to - ', record,'\n')
        
        return connection, cursor
    except (Exception, psycopg2.Error) as error :
        print ('Error while connecting to PostgreSQL', error)
        
def closeConnection(connection, cursor):
    cursor.close()
    connection.close()
    print('PostgreSQL connection is closed')
        
    