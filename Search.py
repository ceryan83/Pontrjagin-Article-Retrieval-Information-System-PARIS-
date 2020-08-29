# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:36:35 2020

@author: cerya
"""
from dao import ArticleDAO
from dao import AuthorDAO

from functools import partial

from tkinter import messagebox
from tkinter import ttk

from utilities import Index
from utilities import PontrjaginNLP

import os

class Results():
    
    def __init__(self, master, searchFrame, queryString):
        self.master = master
        
        self.searchFrame = searchFrame
        
        self.articleIDs = Index.searchIndex(queryString)
        
        if len(self.articleIDs) > 0:
            self.buildResults(self.articleIDs)
        else:            
            messagebox.showinfo(message='The search returned 0 hits.')
            
    def articleDetails(self, article):
        articleID = article.articleID
        os.startfile(article.filepath)
        
        relatedArticleIDs, distances = PontrjaginNLP.get_k_nearest_docs(articleID, k=2,
                                                                        get_dist=True)
        self.resultsFrame.destroy()
        self.backFrame.destroy()
        self.buildResults(relatedArticleIDs, distances)
                    
        
    def buildBackFrame(self):    
        self.searchFrame.grid_forget()
        self.backFrame = ttk.Frame(self.master, padding=10)
        
        ttk.Button(self.backFrame, text='Back', command=self.goBack).grid(row=0, column=0, sticky='W')
          
        self.backFrame.grid(row=0, column=0, sticky='W')
    
    def buildResults(self, articleIDs, distances = list()):
        self.buildBackFrame()
        self.resultsFrame = ttk.Frame(self.master, padding=10)
        
        for i in range(len(articleIDs)):
            articleFrame = ttk.Frame(self.resultsFrame, padding=10)
            buttonFrame = ttk.Frame(self.resultsFrame, padding=10)
            
            article = ArticleDAO.getArticleByID(articleIDs[i])
            
            ttk.Label(articleFrame, text='%d.' % (i+1)).grid(row=0, column=0)
                        
            authors = AuthorDAO.getAuthorsByArticleID(article.articleID)            
            numberOfAuthors = len(authors)
            for j in range(numberOfAuthors):
                if j < numberOfAuthors - 1:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + ';').grid(row=0, column=j+1)
                else:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + '.').grid(row=0, column=j+1)
            ttk.Label(articleFrame, text=article.title + '.').grid(row=0, column=numberOfAuthors+1)
            ttk.Label(articleFrame, text=article.journal).grid(row=0, column=numberOfAuthors+2)
            if article.volume:
                ttk.Label(articleFrame, text=article.volume).grid(
                    row=0, column=numberOfAuthors+3)
            if article.publicationYear:
                ttk.Label(articleFrame, text='(%d),' %(article.publicationYear)).grid(
                    row=0, column=numberOfAuthors+4)
            if article.journalNumber:
                ttk.Label(articleFrame, text='no. %d, ' %(article.journalNumber)).grid(
                    row=0, column=numberOfAuthors+5)
            ttk.Label(articleFrame, text=article.pages + '.').grid(
                row=0, column=numberOfAuthors+6)
            if distances != []:
                ttk.Label(articleFrame, text='(%d%% similar)' %(distances[i])).grid(row=1,
                                                                                  column=1)            
            
            
            ttk.Button(buttonFrame, text='Open', 
                       command=partial(self.articleDetails, 
                                       article)).grid(row=0, column=0)
            if article.isBookmarked != True:
                ttk.Button(buttonFrame, text='Add Bookmark', 
                           command=partial(ArticleDAO.addBookmarkByArticleID,
                                           article.articleID)).grid(row=0, column=1)
            else:
                ttk.Button(buttonFrame, text='Remove Bookmark', 
                           command=partial(ArticleDAO.removeBookmarkByArticleID,
                                           article.articleID)).grid(row=0, column=1)
            
            articleFrame.grid(row=i, column=0, sticky='W')
            buttonFrame.grid(row=i, column=1)
            
        self.resultsFrame.grid(row=1, column=0)
        
    def goBack(self):
        self.backFrame.destroy()
        self.resultsFrame.destroy()
        
        self.searchFrame.grid(row=0, column=0, sticky='NSEW')