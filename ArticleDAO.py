# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:21:20 2020

@author: cerya
"""
from model import Article
from utilities import DAOUtilities

def getAllArticles():
    articles = list()
    
    connection, cursor = DAOUtilities.getConnection()
    try:
        cursor.execute("SELECT * FROM articles ORDER BY articleid;")
        for res in cursor:
            article = Article.Article(*res)
            articles.append(article)
        print('All articles retrieved.')
    except:
        print('Problem encountered while retrieving articles.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return articles

def getArticlesByAuthor(authorID):
    articles = list()
    
    connection, cursor = DAOUtilities.getConnection()
    try:
        cursor.execute("""SELECT articles.articleid, title, journal, volume, journalnumber,
                       publicationyear, pages, articlecontent, filepath, isbookmarked FROM articles
                       INNER JOIN article_authors ON article_authors.authorid = %s
                       AND articles.articleid = article_authors.articleid;""", (authorID,))
        for res in cursor:
            article = Article.Article(*res)
            articles.append(article)
        print('Articles by author retrieved.')
    except:
        print('There was a problem encountered while retrieving articles by author.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return articles
    
def getArticleByFilepath(filepath):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("SELECT * FROM articles WHERE filepath = %s;",
                   (filepath,))
        res = cursor.fetchone()
        article = Article.Article(*res)
        print('Article retrieved.')
    except:
        print('Error while retreiving article ID.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return article

def getArticleByID(articleID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("SELECT * FROM articles WHERE articleid = %s;", 
                       (articleID,))
        res = cursor.fetchone()
        article = Article.Article(*res)
        print('Article retrieved.')
    except:
        print('There was  a problem retrieving the article.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return article

def getArticleCount():
    connection, cursor = DAOUtilities.getConnection()
    try:    
        cursor.execute("SELECT COUNT(articleid) FROM articles;")
        count = cursor.fetchone()[0]
        print('Article count obtained.')
    except:
        print('Problem obtaining article count.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return count

def getArticleIDByFilepath(filepath):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("SELECT articleid FROM articles WHERE filepath = %s;",
                   (filepath,))
        articleID = cursor.fetchone()[0]
        print('Article ID retrieved.')
    except:
        print('Error while retreiving article ID.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return articleID

def getBookmarkedArticles():
    articles = list()
    
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("SELECT * FROM articles WHERE isbookmarked = %s;",
                       (True,))
        for res in cursor:
            article = Article.Article(*res)
            articles.append(article)
        print('Bookmarks retrieved.')
    except:
        print('Error while retrieving bookmarked articles.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        return articles
    
def addArticle(article):
    connection, cursor = DAOUtilities.getConnection()
    
    data = (article.title, article.journal, article.volume, 
            article.journalNumber, article.publicationYear,
            article.pages, article.articleContent, article.filepath,)
    try:
        cursor.execute("""INSERT INTO articles (title, journal, volume, 
                       journalnumber, publicationyear, pages, 
                       articlecontent, filepath) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", data)
        
        connection.commit()
        print('Added article to database.')
    except:
        print ('Error adding article to PostgreSQL')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
        
def addBookmarkByArticleID(articleID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("""UPDATE articles SET isbookmarked = %s 
                       WHERE articleid = %s;""", (True, articleID,))
        
        connection.commit()
        print('Article bookmarked.')
    except:
        print ('Error bookmarking article.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)    
    
    
def removeArticle(articleID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("DELETE articles WHERE articleid = %s;", 
                       (articleID,))
        
        connection.commit()
        print('Article removed from database.')
    except:
        print('There was a problem removing the article from the database.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)
    
def removeBookmarkByArticleID(articleID):
    connection, cursor = DAOUtilities.getConnection()
    
    try:
        cursor.execute("""UPDATE articles SET isbookmarked = %s 
                       WHERE articleid = %s;""", (False, articleID,))
        
        connection.commit()
        print('Bookmark removed.')
    except:
        print ('Error removing bookmark.')
    finally:
        DAOUtilities.closeConnection(connection, cursor)    
    
def editArticle(articleID, newArticle):
    connection, cursor = DAOUtilities.getConnection()

    data = (newArticle.title, newArticle.journal, newArticle.volume, 
    newArticle.journalNumber, newArticle.publicationYear,
    newArticle.pages, articleID,)
    try:
        cursor.execute("""UPDATE articles SET title = %s, journal = %s, 
                       volume = %s, journalnumber = %s, 
                       publicationyear = %s, pages = %s WHERE 
                       articleid = %s;""", data)
        
        connection.commit()                   
        print('Successfully edited article.')
    except:
        print('There was a problem editing the article')
    finally:
        DAOUtilities.closeConnection(connection, cursor)