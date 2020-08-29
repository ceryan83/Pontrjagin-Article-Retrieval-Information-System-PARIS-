# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:58:55 2020

@author: cerya
"""
from model import Author
from utilities import DAOUtilities

def getAllAuthors():
    authors = list()
    
    connection, cursor = DAOUtilities.getConnection()
    try:
        cursor.execute("SELECT * FROM authors ORDER BY lastname, firstname, middlename;")
        for res in cursor:
            author = Author.Author(*res)
            authors.append(author)
        print('Authors retrieved.')
    except:
        print('Encountered a problem while retrieving authors.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return authors
    
def getArticleCountByAuthor(authorID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("""SELECT COUNT(articleid) FROM article_authors WHERE
                       authorid = %s;""", (authorID,))
        count = cursor.fetchone()[0]
        print('Retrieved article count.')
    except:
        print('Encountered a problem getting article count for author.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)               
        return count

def getAuthorsByArticleID(articleID):
    authors = list()
    
    connection, cursor = DAOUtilities.getConnection()
    try:
        cursor.execute("""SELECT authors.authorid, lastname, firstname, middlename 
                       FROM authors INNER JOIN article_authors
                       ON article_authors.articleid = %s 
                       AND authors.authorid = article_authors.authorid 
                       ORDER BY authors.lastname, firstname, middlename;;""", (articleID,))
        for res in cursor:
            author = Author.Author(*res)
            authors.append(author)
        print('Author information pulled from database.')
    except:
        print('There was a problem pulling the author info for the article.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return authors

def getAuthorByID(authorID):
    connection, cursor = DAOUtilities.getConnection()
    
    cursor.execute("SELECT * FROM authors WHERE authorid = %s;", 
                   (authorID,))
    res = cursor.fetchone()
    author = Author.Author(*res)
    
    DAOUtilities.closeConnection(connection, cursor)
    return author

def getAuthorIDByName(lastName, firstName, middleName):
    connection, cursor = DAOUtilities.getConnection()
    
    data = (lastName, firstName, middleName,)
    try:
        cursor.execute("""SELECT authorid FROM authors WHERE 
                       lastname = %s AND firstname = %s AND
                       middlename = %s;""", data)
        res = cursor.fetchone()
        if res != None:
            authorID = res[0]            
            print('Author ID retrieved.')
        else:
            authorID = 0
            print('Author not in database, returning authorID of 0.')
    except:
        print('Encountered a problem while retrieving author ID.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return authorID

def addAuthor(lastName, firstName, middleName):
    connection, cursor = DAOUtilities.getConnection()
    
    data = (lastName, firstName, middleName,)
    try:
        if getAuthorIDByName(lastName, firstName, middleName) == 0:
            cursor.execute("""INSERT INTO authors (lastname, firstname, middlename) 
                           VALUES (%s, %s, %s);""", data)
    
            connection.commit()
            print('Author added to database.')
    except:
        print('There was a problem entering the author into the database.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
    
def addAuthorToArticle(articleID, authorID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("INSERT INTO article_authors VALUES (%s, %s);", 
                   (articleID, authorID,))
    
        connection.commit()
        print('Author added to article.')
    except:
        print('Encountered a problem while adding author to article.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
    
def removeAuthor(authorID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("""SELECT articleid FROM article_authors WHERE 
                       authorid = %s;""", (authorID,))
        for res in cursor:
            removeAuthorFromArticle(res[0], authorID)
        cursor.execute("DELETE FROM authors WHERE authorid = %s;", (authorID,))
    
        connection.commit()
        print('Author removed from database.')
    except:
        print('There was a problem removing the author from the database.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
    
def removeAuthorFromArticle(articleID, authorID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("""DELETE FROM article_authors WHERE articleid = %s AND 
                       authorid = %s""", (articleID, authorID,))
                       
        connection.commit()               
        print('Author removed from article.')
    except:
        print('There was a problem removing the author from the article.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)