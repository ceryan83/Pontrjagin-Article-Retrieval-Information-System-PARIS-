# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:26:45 2020

@author: cerya
"""
from dao import ArticleDAO
from dao import AuthorDAO

from functools import partial

from model import Article

from tkinter import filedialog
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import ttk

from utilities import Index

#%%
class editArticle():
    
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.attributes('-topmost', 'true')
        self.window.title('Edit article')
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        ttk.Label(self.contentFrame, text='Choose filepath of article to edit:').grid(row=0, column=0)
        ttk.Button(self.contentFrame, text='Browse', command=self.getDetails).grid(row=0, column=1)
        
        self.contentFrame.grid(row=0, column=0)
        
    def addAuthor(self):        
        self.lastNames.append(StringVar())
        self.firstNames.append(StringVar())
        self.middleNames.append(StringVar())

        rowNumber = len(self.lastNames)
        
        ttk.Entry(self.authorFrame, textvariable=self.lastNames[-1]).grid(row=rowNumber, column=0)
        ttk.Entry(self.authorFrame, textvariable=self.firstNames[-1]).grid(row=rowNumber, column=1)
        ttk.Entry(self.authorFrame, textvariable=self.middleNames[-1]).grid(row=rowNumber, column=2)       
    
    def getAuthorDetails(self):        
        self.authorMainFrame = ttk.LabelFrame(self.window, text = 'Author(s)', padding=10)
        self.authors = AuthorDAO.getAuthorsByArticleID(self.articleID)
        
        self.authorFrame = ttk.Frame(self.authorMainFrame, padding=10)
        
        ttk.Label(self.authorFrame, text='Last name:').grid(row=0, column=0)
        ttk.Label(self.authorFrame, text='First name:').grid(row=0, column=1)
        ttk.Label(self.authorFrame, text='Middle name:').grid(row=0, column=2)
        
        self.lastNames = list()
        self.firstNames = list()
        self.middleNames = list()
        
        if not self.authors:
            self.addAuthor()
        else:
            self.lastNameEntries = list()
            self.firstNameEntries = list()
            self.middleNameEntries = list()
            
            self.removeButtons = list()
            for i in range(len(self.authors)):
                self.lastNames.append(StringVar())
                self.firstNames.append(StringVar())
                self.middleNames.append(StringVar())
                                
                self.lastNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.lastNames[i]))                                            
                self.firstNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.firstNames[i]))
                self.middleNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.middleNames[i]))
                
                self.lastNames[i].set(self.authors[i].lastName)
                self.firstNames[i].set(self.authors[i].firstName)
                self.middleNames[i].set(self.authors[i].middleName)
                
                self.lastNameEntries[i].grid(row=i+1, column=0)                
                self.firstNameEntries[i].grid(row=i+1, column=1)
                self.middleNameEntries[i].grid(row=i+1, column=2)
        
                ttk.Button(self.authorFrame, text='Remove', command=partial(self.removeAuthor, i)).grid(row=i+1, column=3)
                
        ttk.Button(self.authorMainFrame, text='Add additional author', command=self.addAuthor).grid(row=1, column=0)
                            
        self.authorFrame.grid(row=0, column=0)
        self.authorMainFrame.grid(row=0, column=1)
    
    def getDetails(self):
        self.filepath = filedialog.askopenfilename(filetypes=[('PDF files','*.pdf')])
        if not self.filepath:
            return
        
        self.articleID = ArticleDAO.getArticleIDByFilepath(self.filepath)
        article = ArticleDAO.getArticleByID(self.articleID)
        
        ttk.Label(self.contentFrame, text='Title:').grid(row=1, column=0)
        ttk.Label(self.contentFrame, text='Journal:').grid(row=2, column=0)
        ttk.Label(self.contentFrame, text='Volume:').grid(row=3, column=0)
        ttk.Label(self.contentFrame, text='Journal number:').grid(row=4, column=0)
        ttk.Label(self.contentFrame, text='Publication year:').grid(row=5, column=0)
        ttk.Label(self.contentFrame, text='Pages:').grid(row=6, column=0)
        
        self.title = StringVar()
        self.journal = StringVar()
        self.volume = StringVar()
        self.journalNumber = StringVar()
        self.publicationYear = StringVar()
        self.pages = StringVar()
        
        self.title.set(article.title)
        self.journal.set(article.journal)
        if article.volume != None:
            self.volume.set(article.volume)
        if article.journalNumber != None:
            self.journalNumber.set(article.journalNumber)
        if article.publicationYear != None:
            self.publicationYear.set(article.publicationYear)
        self.pages.set(article.pages)
        
        ttk.Entry(self.contentFrame, textvariable=self.title).grid(row=1, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journal).grid(row=2, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.volume).grid(row=3, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journalNumber).grid(row=4, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.publicationYear).grid(row=5, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.pages).grid(row=6, column=1)
        
        ttk.Button(self.contentFrame, text='Update', command=self.update).grid(row=7, column=0)
        
        #Get Authors 
        self.getAuthorDetails()
        
    def removeAuthor(self, i):
        authorID = self.authors[i].authorID
        
        AuthorDAO.removeAuthorFromArticle(self.articleID, authorID)
        
        articleCount = AuthorDAO.getArticleCountByAuthor(authorID)
        if articleCount == 0:
            AuthorDAO.removeAuthor(authorID)
        
        self.authorMainFrame.destroy()
        self.getAuthorDetails()
        
    def update(self):
        title = self.title.get()
        journal = self.journal.get()
        volume = self.volume.get()
        if volume == '':
            volume = None
        journalNumber = self.journalNumber.get()
        if journalNumber == '':
            journalNumber = None
        publicationYear = self.publicationYear.get()
        if publicationYear == '':
            publicationYear = None
        pages = self.pages.get()
        
        newArticle = Article.Article(self.articleID, title, journal, volume, 
                                     journalNumber, publicationYear, pages)
        ArticleDAO.editArticle(self.articleID, newArticle)
        
        for i in range(len(self.lastNames)):
            lastName = self.lastNames[i].get()
            firstName = self.firstNames[i].get()
            middleName = self.middleNames[i].get()
            
            if lastName != '':
                AuthorDAO.addAuthor(lastName, firstName, middleName)
                authorID = AuthorDAO.getAuthorIDByName(lastName, firstName, middleName)
                AuthorDAO.addAuthorToArticle(self.articleID, authorID)
                
        article = ArticleDAO.getArticleByID(self.articleID)
        authors = AuthorDAO.getAuthorsByArticleID(self.articleID)
        Index.indexDocument(article, authors)
            
        self.window.destroy()

#%%
class removeArticle():
    
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.attributes('-topmost', 'true')
        self.window.title('Remove article')
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        ttk.Label(self.contentFrame, text='Choose filepath of article to remove:').grid(row=0, column=0)
        ttk.Button(self.contentFrame, text='Browse', command=self.getDetails).grid(row=0, column=1)
        
        self.contentFrame.grid(row=0, column=0)
        
    def addAuthor(self):        
        self.lastNames.append(StringVar())
        self.firstNames.append(StringVar())
        self.middleNames.append(StringVar())

        rowNumber = len(self.lastNames)
        
        ttk.Entry(self.authorFrame, textvariable=self.lastNames[-1]).grid(row=rowNumber, column=0)
        ttk.Entry(self.authorFrame, textvariable=self.firstNames[-1]).grid(row=rowNumber, column=1)
        ttk.Entry(self.authorFrame, textvariable=self.middleNames[-1]).grid(row=rowNumber, column=2)       
    
    def getAuthorDetails(self):        
        self.authorMainFrame = ttk.LabelFrame(self.window, text = 'Author(s)', padding=10)
        self.authors = AuthorDAO.getAuthorsByArticleID(self.articleID)
        
        self.authorFrame = ttk.Frame(self.authorMainFrame, padding=10)
        
        ttk.Label(self.authorFrame, text='Last name:').grid(row=0, column=0)
        ttk.Label(self.authorFrame, text='First name:').grid(row=0, column=1)
        ttk.Label(self.authorFrame, text='Middle name:').grid(row=0, column=2)
        
        self.lastNames = list()
        self.firstNames = list()
        self.middleNames = list()
        
        if not self.authors:
            self.addAuthor()
        else:
            self.lastNameEntries = list()
            self.firstNameEntries = list()
            self.middleNameEntries = list()
            
            self.removeButtons = list()
            for i in range(len(self.authors)):
                self.lastNames.append(StringVar())
                self.firstNames.append(StringVar())
                self.middleNames.append(StringVar())
                                
                self.lastNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.lastNames[i]))                                            
                self.firstNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.firstNames[i]))
                self.middleNameEntries.append(ttk.Entry(self.authorFrame, textvariable=self.middleNames[i]))
                
                self.lastNames[i].set(self.authors[i].lastName)
                self.firstNames[i].set(self.authors[i].firstName)
                self.middleNames[i].set(self.authors[i].middleName)
                
                self.lastNameEntries[i].grid(row=i+1, column=0)                
                self.firstNameEntries[i].grid(row=i+1, column=1)
                self.middleNameEntries[i].grid(row=i+1, column=2)
                           
        self.authorFrame.grid(row=0, column=0)
        self.authorMainFrame.grid(row=0, column=1)
    
    def getDetails(self):
        self.filepath = filedialog.askopenfilename(filetypes=[('PDF files','*.pdf')])
        if not self.filepath:
            return
        
        self.articleID = ArticleDAO.getArticleIDByFilepath(self.filepath)
        article = ArticleDAO.getArticleByID(self.articleID)
        
        ttk.Label(self.contentFrame, text='Title:').grid(row=1, column=0)
        ttk.Label(self.contentFrame, text='Journal:').grid(row=2, column=0)
        ttk.Label(self.contentFrame, text='Volume:').grid(row=3, column=0)
        ttk.Label(self.contentFrame, text='Journal number:').grid(row=4, column=0)
        ttk.Label(self.contentFrame, text='Publication year:').grid(row=5, column=0)
        ttk.Label(self.contentFrame, text='Pages:').grid(row=6, column=0)
        
        self.title = StringVar()
        self.journal = StringVar()
        self.volume = StringVar()
        self.journalNumber = StringVar()
        self.publicationYear = StringVar()
        self.pages = StringVar()
        
        self.title.set(article.title)
        self.journal.set(article.journal)
        if article.volume != None:
            self.volume.set(article.volume)
        if article.journalNumber != None:
            self.journalNumber.set(article.journalNumber)
        if article.publicationYear != None:
            self.publicationYear.set(article.publicationYear)
        self.pages.set(article.pages)
        
        ttk.Entry(self.contentFrame, textvariable=self.title).grid(row=1, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journal).grid(row=2, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.volume).grid(row=3, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journalNumber).grid(row=4, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.publicationYear).grid(row=5, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.pages).grid(row=6, column=1)
        
        ttk.Button(self.contentFrame, text='Remove', command=self.remove).grid(row=7, column=0)
        
        #Get Authors 
        self.getAuthorDetails()
        
    def removeAuthor(self, i):
        authorID = self.authors[i].authorID
        
        AuthorDAO.removeAuthorFromArticle(self.articleID, authorID)
        
        articleCount = AuthorDAO.getArticleCountByAuthor(authorID)
        if articleCount == 0:
            AuthorDAO.removeAuthor(authorID)
        
        self.authorMainFrame.destroy()
        self.getAuthorDetails()
        
    def remove(self):
        Index.deleteDocument(self.articleID)
        
        for i in range(len(self.authors)):
            self.removeAuthor(i)
            
        ArticleDAO.removeArticle(self.articleID)
        self.window.destroy()