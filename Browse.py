# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:02:31 2020

@author: cerya
"""
from dao import ArticleDAO
from dao import AuthorDAO

from functools import partial

from tkinter import Toplevel
from tkinter import ttk

from utilities import PontrjaginNLP

import os

class BrowseAll():
    
    def __init__(self, master, category='all'):
        
        self.window = Toplevel(master)
        self.window.title('Articles')
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        if category == 'all':
            articles = ArticleDAO.getAllArticles()
        if category == 'bookmarked':
            articles = ArticleDAO.getBookmarkedArticles()
        
        self.buildArticleWindow(articles)
        
    def articleDetails(self, article):
        print(article.title)
        articleID = article.articleID
        print(articleID)
        os.startfile(article.filepath)
        
        relatedArticleIDs, distances = PontrjaginNLP.get_k_nearest_docs(articleID, k=2,
                                                                        get_dist=True)

        articles = list()
        for i in range(len(relatedArticleIDs)):
            recommendedArticle = ArticleDAO.getArticleByID(relatedArticleIDs[i])
            articles.append(recommendedArticle)
            
        self.buildArticleWindow(articles, distances)
            
    def buildArticleWindow(self, articles, distances=list()):
        self.contentFrame.destroy()
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        for i in range(len(articles)):
            articleFrame = ttk.Frame(self.contentFrame, padding=10)
            
            ttk.Label(articleFrame, text='%d.' % (i+1)).grid(row=0, column=0)
                        
            authors = AuthorDAO.getAuthorsByArticleID(articles[i].articleID)            
            numberOfAuthors = len(authors)
            for j in range(numberOfAuthors):
                if j < numberOfAuthors - 1:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + ';').grid(row=0, column=j+1)
                else:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + '.').grid(row=0, column=j+1)
            ttk.Label(articleFrame, text=articles[i].title + '.').grid(row=0, column=numberOfAuthors+1)
            ttk.Label(articleFrame, text=articles[i].journal).grid(row=0, column=numberOfAuthors+2)
            if articles[i].volume:
                ttk.Label(articleFrame, text=articles[i].volume).grid(
                    row=0, column=numberOfAuthors+3)
            if articles[i].publicationYear:
                ttk.Label(articleFrame, text='(%d),' %(articles[i].publicationYear)).grid(
                    row=0, column=numberOfAuthors+4)
            if articles[i].journalNumber:
                ttk.Label(articleFrame, text='no. %d, ' %(articles[i].journalNumber)).grid(
                    row=0, column=numberOfAuthors+5)
            ttk.Label(articleFrame, text=articles[i].pages + '.').grid(
                row=0, column=numberOfAuthors+6)
            if distances != []:
                ttk.Label(articleFrame, text='(%d%% similar)' %(distances[i])).grid(row=1,
                                                                                  column=1)            
            ttk.Button(self.contentFrame, text='Open', 
                       command=partial(self.articleDetails, articles[i])).grid(row=i, column=1)
            if articles[i].isBookmarked != True:
                ttk.Button(self.contentFrame, text='Add Bookmark', 
                           command=partial(ArticleDAO.addBookmarkByArticleID,
                                           articles[i].articleID)).grid(row=i, column=2)
            else:
                ttk.Button(self.contentFrame, text='Remove Bookmark', 
                           command=partial(ArticleDAO.removeBookmarkByArticleID,
                                           articles[i].articleID)).grid(row=i, column=2)
            articleFrame.grid(row=i, column=0, sticky='W')
        
        self.contentFrame.grid(row=0, column=0)
        
class BrowseByAuthor():
    
    def __init__(self, master):
        
        self.window = Toplevel(master)
        self.window.title('List of authors')
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        authors = AuthorDAO.getAllAuthors()
        self.buildAuthorWindow(authors)
        
    def articleDetails(self, article):
        
        os.startfile(article.filepath)
        
        relatedArticleIDs, distances = PontrjaginNLP.get_k_nearest_docs(article.articleID,
                                                                        get_dist=True)
        articles = list()
        for i in range(len(relatedArticleIDs)):
            articles.append(ArticleDAO.getArticleByID(relatedArticleIDs[i]))
            
        self.buildArticleWindow(articles, distances)
        
        
    def buildAuthorWindow(self, authors):
        
        for i in range(len(authors)):
            authorFrame = ttk.Frame(self.contentFrame, padding=10)
            
            ttk.Label(authorFrame, text='%d.' % (i+1)).grid(row=0, column=0)
                        
            if authors[i].middleName != '':
                ttk.Label(authorFrame, text=authors[i].lastName + ', ' +
                                 authors[i].firstName + ' ' +
                                 authors[i].middleName).grid(row=0, column=1)
            else:
                ttk.Label(authorFrame, text=authors[i].lastName + ', ' +
                                 authors[i].firstName).grid(row=0, column=1)
                
            authorFrame.grid(row=i, column=0, sticky='W')
            ttk.Button(self.contentFrame, text='View articles', 
                       command=partial(self.getArticles, authors[i].authorID)).grid(row=i, column=1)
        
        self.contentFrame.grid(row=0, column=0)
        
    def buildArticleWindow(self, articles, distances = list()):
        self.contentFrame.destroy()
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        for i in range(len(articles)):
            articleFrame = ttk.Frame(self.contentFrame, padding=10)
            
            ttk.Label(articleFrame, text='%d.' % (i+1)).grid(row=0, column=0)
                        
            authors = AuthorDAO.getAuthorsByArticleID(articles[i].articleID)            
            numberOfAuthors = len(authors)
            for j in range(numberOfAuthors):
                if j < numberOfAuthors - 1:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + ';').grid(row=0, column=j+1)
                else:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + '.').grid(row=0, column=j+1)
            ttk.Label(articleFrame, text=articles[i].title + '.').grid(row=0, column=numberOfAuthors+1)
            ttk.Label(articleFrame, text=articles[i].journal).grid(row=0, column=numberOfAuthors+2)
            if articles[i].volume:
                ttk.Label(articleFrame, text=articles[i].volume).grid(
                    row=0, column=numberOfAuthors+3)
            if articles[i].publicationYear:
                ttk.Label(articleFrame, text='(%d),' %(articles[i].publicationYear)).grid(
                    row=0, column=numberOfAuthors+4)
            if articles[i].journalNumber:
                ttk.Label(articleFrame, text='no. %d, ' %(articles[i].journalNumber)).grid(
                    row=0, column=numberOfAuthors+5)
            ttk.Label(articleFrame, text=articles[i].pages + '.').grid(
                row=0, column=numberOfAuthors+6)
            if distances != []:
                ttk.Label(articleFrame, text='(%d%% similar)' %(distances[i])).grid(row=1,
                                                                                  column=1)
            
            articleFrame.grid(row=i, column=0, sticky='W')
            ttk.Button(self.contentFrame, text='Open', 
                       command=partial(self.articleDetails, articles[i])).grid(row=i, column=1)
            if articles[i].isBookmarked != True:
                ttk.Button(self.contentFrame, text='Add Bookmark', 
                           command=partial(ArticleDAO.addBookmarkByArticleID,
                                           articles[i].articleID)).grid(row=i, column=2)
            else:
                ttk.Button(self.contentFrame, text='Remove Bookmark', 
                           command=partial(ArticleDAO.removeBookmarkByArticleID,
                                           articles[i].articleID)).grid(row=i, column=2)
            
                    
        
        self.contentFrame.grid(row=0, column=0)
        
    def getArticles(self, authorID):
        articles = ArticleDAO.getArticlesByAuthor(authorID)
        self.buildArticleWindow(articles)
        
if __name__ == '__main__':
    from tkinter import Tk
    
    root = Tk()
    BrowseAll(root)
    root.mainloop()
        
        