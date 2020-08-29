# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 16:51:28 2020

@author: cerya
"""
from dao import ArticleDAO
from dao import AuthorDAO

from tkinter import DoubleVar
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import ttk

from utilities import Index
from utilities import ProcessPDFs

#%%
class importPDF():
    
    def __init__(self, master):
        self.master = master
        
        self.filepath = filedialog.askopenfilename(filetypes=[('PDF files','*.pdf')])
        if not self.filepath:
            return
        
        self.window = Toplevel(master)
        self.window.attributes('-topmost', 'true')
        self.window.title('Import new file - ' + self.filepath)
        
        self.getDetails()
        self.getAuthorDetails()
        
        buttonFrame = ttk.Frame(self.window, borderwidth=0.5, padding=10, relief='solid')
        ttk.Button(buttonFrame, text='Import', command=self.submitArticle).grid(row=0, column=0)
        ttk.Button(buttonFrame, text='Cancel', command=self.window.destroy).grid(row=0, column=1)
        buttonFrame.grid(row=1, column=1)
          
    def addAuthor(self):        
        self.lastNames.append(StringVar())
        self.firstNames.append(StringVar())
        self.middleNames.append(StringVar())

        rowNumber = len(self.lastNames)
        
        ttk.Entry(self.authorFrame, textvariable=self.lastNames[-1]).grid(row=rowNumber, column=0)
        ttk.Entry(self.authorFrame, textvariable=self.firstNames[-1]).grid(row=rowNumber, column=1)
        ttk.Entry(self.authorFrame, textvariable=self.middleNames[-1]).grid(row=rowNumber, column=2)  
    
    def getAuthorDetails(self):
        self.authorMainFrame = ttk.Labelframe(self.window, borderwidth=0.5, text='Author(s):', padding=10,
                                              relief='solid')
        self.authorFrame = ttk.Frame(self.authorMainFrame, padding=10)
        
        ttk.Label(self.authorFrame, text='Last name:').grid(row=0, column=0)
        ttk.Label(self.authorFrame, text='First name:').grid(row=0, column=1)
        ttk.Label(self.authorFrame, text='Middle name:').grid(row=0, column=2)
        
        self.lastNames = list()
        self.firstNames = list()
        self.middleNames = list()

        self.addAuthor()
        
        ttk.Button(self.authorMainFrame, text='Add additional author', command=self.addAuthor).grid(row=1, column=0)
        
        self.authorFrame.grid(row=0, column=0)
        self.authorMainFrame.grid(row=0, column=1)
    
    def getDetails(self):
        self.contentFrame = ttk.Frame(self.window, borderwidth=0.5, padding = 10, relief='solid')
        
        ttk.Label(self.contentFrame, text='Title:').grid(row=0, column=0)
        ttk.Label(self.contentFrame, text='Journal:').grid(row=1, column=0)
        ttk.Label(self.contentFrame, text='Volume:').grid(row=2, column=0)
        ttk.Label(self.contentFrame, text='Journal number:').grid(row=3, column=0)
        ttk.Label(self.contentFrame, text='Publication year:').grid(row=4, column=0)
        ttk.Label(self.contentFrame, text='Pages:').grid(row=5, column=0)
        
        self.title = StringVar()
        self.journal = StringVar()
        self.volume = StringVar()
        self.journalNumber = StringVar()
        self.publicationYear = StringVar()
        self.pages = StringVar()
        
        ttk.Entry(self.contentFrame, textvariable=self.title).grid(row=0, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journal).grid(row=1, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.volume).grid(row=2, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.journalNumber).grid(row=3, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.publicationYear).grid(row=4, column=1)
        ttk.Entry(self.contentFrame, textvariable=self.pages).grid(row=5, column=1)
        
        self.contentFrame.grid(row=0, column=0)
                
    def submitArticle(self):
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
        
        lastNames = list()
        firstNames = list()
        middleNames = list()
        for i in range(len(self.lastNames)):
            lastNames.append(self.lastNames[i].get())
            firstNames.append(self.firstNames[i].get())
            middleNames.append(self.middleNames[i].get())
        
        self.window.destroy()
        ProcessPDFs.processPDF(self.filepath, title, journal, volume, 
                               journalNumber, publicationYear, pages)
        
        article = ArticleDAO.getArticleByFilepath(self.filepath)
        for i in range(len(lastNames)):
            AuthorDAO.addAuthor(lastNames[i], firstNames[i], middleNames[i])
            authorID = AuthorDAO.getAuthorIDByName(lastNames[i], 
                                                   firstNames[i], 
                                                   middleNames[i])
            AuthorDAO.addAuthorToArticle(article.articleID, authorID)
        authors = AuthorDAO.getAuthorsByArticleID(article.articleID)
        Index.indexDocument(article, authors)
            

#%%    
class importPDFsFromFolder():
    
    def __init__(self, master):
        self.master = master
        
        dirName = filedialog.askdirectory()        
        if not dirName:
            return
        
        self.buildWindow()
        
        filepaths = list()
        filepaths = ProcessPDFs.populateList(dirName, res=list())

        count = ArticleDAO.getArticleCount()
        self.processFiles(filepaths)
        newCount = ArticleDAO.getArticleCount()
        diff = newCount - count
        
        self.window.destroy()
        messagebox.showinfo(message='%d files imported.' % diff)
        
    def buildWindow(self):
        self.window = Toplevel(self.master)
        self.window.title('Importing files')
        self.window.attributes('-topmost', 'true')
        self.contentFrame = ttk.Frame(self.window, padding=10)
        
        self.index = StringVar()
        self.numberOfFiles = StringVar()
        
        ttk.Label(self.contentFrame, text='Processing file').grid(row=0, column=0)
        ttk.Label(self.contentFrame, textvariable=self.index).grid(row=0, column=1)
        ttk.Label(self.contentFrame, text='of').grid(row=0, column=2)
        ttk.Label(self.contentFrame, textvariable=self.numberOfFiles).grid(row=0, column=3)
        ttk.Label(self.contentFrame, text='... (this may take a while)').grid(row=0, column=4)
        
        
        self.progress = DoubleVar()
        
        self.progressBar = ttk.Progressbar(self.contentFrame, length=225, 
                                           variable = self.progress, maximum=100, mode='determinate')
        self.progressBar.grid(row=1, column=0, columnspan=5)
        
        self.contentFrame.grid(row=0, column=0)
        self.master.update()
        
    def processFiles(self, filepaths):
        numberOfFiles = len(filepaths)
        self.numberOfFiles.set(numberOfFiles)
        for i in range(numberOfFiles):
            self.index.set(i+1)
            self.progress.set(i*100/numberOfFiles)
            self.master.update()
            ProcessPDFs.processPDF(filepaths[i])
            
            article = ArticleDAO.getArticleByFilepath(filepaths[i])
            authors = list()
            
            Index.indexDocument(article, authors)

#%%   
if __name__ == '__main__':
    from tkinter import Tk    
    
    root = Tk()
    
    ttk.Button(root, text='Import folder', command=lambda: importPDFsFromFolder(root)).grid(row=0,column=0)
    root.mainloop()
    
