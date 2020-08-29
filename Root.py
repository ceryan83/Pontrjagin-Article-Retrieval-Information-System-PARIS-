# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:58:20 2020

@author: cerya
"""
from tkinter import Menu
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Tk
from tkinter import ttk
from tkinter import *

from utilities import PontrjaginNLP

import Bookmarks
import Browse
import EditArticle
import ImportPDF
import Search

def aboutInfo():
    messagebox.showinfo(message='''Pontrjagin Article Retrieval Information System (PARIS)
                        version 0.1\n\n
                        Created by Christopher Ryan\n\n
                        PARIS uses PyTesseract OCR to scan .pdf files for text, and
                        the Whoosh search engine to search through those files. Its recommendation
                        engine uses Latent Dirichlet Allocation (LDA), a machine learning
                        algorithm, to make suggestions for similar articles. 
                        ''')
    #TODO include date of creation, version numbers for Whoosh and PyTesseract
    return False

def browseAll(category = 'all'):
    Browse.BrowseAll(root, category)

def browseByAuthor():
    Browse.BrowseByAuthor(root)
    
def calibrate():
    PontrjaginNLP.Calibrate()

def editArticle():
    EditArticle.editArticle(root)

def getFAQ():
    #TODO define function
    return False

def getInstructions():
    #TODO define function
    return False
    
def importPDF():
    ImportPDF.importPDF(root)
    
def importPDFsFromFolder():
    ImportPDF.importPDFsFromFolder(root)
    
def removeArticle():
    EditArticle.removeArticle(root)

def search():
    queryString = query.get()
    Search.Results(root, searchFrame, queryString)

def viewBookmarks():
    Bookmarks.viewBookmarks(root)

root = Tk()
root.title('Pontrjagin Article Retrieval Information System (PARIS)')

root.option_add('*tearOff', False)
menubar = Menu(root)
root['menu'] = menubar
menuFile = Menu(menubar)
menuEdit = Menu(menubar)
menuBrowse = Menu(menubar)
menuHelp = Menu(menubar)
menubar.add_cascade(menu=menuFile, label='File')
menubar.add_cascade(menu=menuEdit, label='Edit')
menubar.add_command(label='Bookmarks', command=lambda: browseAll(category='bookmarked'))
menubar.add_cascade(menu=menuBrowse, label='Browse')
menubar.add_command(label='Calibrate', command=calibrate)
menubar.add_cascade(menu=menuHelp, label='Help')
menuFile.add_command(label='Import article', command=importPDF)
menuFile.add_command(label='Import articles in folder', 
                     command=importPDFsFromFolder)
menuEdit.add_command(label='Edit article details', command=editArticle)
menuEdit.add_command(label='Remove article', command=removeArticle)
menuBrowse.add_command(label='Browse all', command=browseAll)
menuBrowse.add_command(label='Browse by author', 
                       command=browseByAuthor)
menuHelp.add_command(label='About...', command=aboutInfo)
menuHelp.add_separator()
menuHelp.add_command(label='FAQ', command=getFAQ)
menuHelp.add_separator()
menuHelp.add_command(label='How to use', command=getInstructions)

searchFrame = ttk.Frame(root, padding=10)

query = StringVar()

ttk.Entry(searchFrame, width=60, textvariable=query).grid(row=0, column=0,
                                                           sticky='W', pady=5)
ttk.Button(searchFrame, text='Search', command=search).grid(row=1, column=0, 
                                                             sticky='W')

searchFrame.grid(row=0, column=0, sticky='NSEW')

root.mainloop()