# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:37:55 2020

@author: cerya
"""
from dao import ArticleDAO
from dao import AuthorDAO

from tkinter import Toplevel
from tkinter import ttk

import os

class viewBookmarks():
    
    def __init__(self, master):
        
        self.window = Toplevel(master)
        self.window.title('Bookmarks')
        
        self.bookmarkedArticles = ArticleDAO.getBookmarkedArticles()
                
        self.buildWindow()
            
    def buildWindow(self):
        contentFrame = ttk.Frame(self.window, padding=10)
        
        for i in range(len(self.bookmarkedArticles)):
            articleFrame = ttk.Frame(contentFrame, padding=10)
            buttonFrame = ttk.Frame(contentFrame, padding=10)
            
            ttk.Label(articleFrame, text='%d.' % (i+1)).grid(row=0, column=0)
                        
            authors = AuthorDAO.getAuthorsByArticleID(self.bookmarkedArticles[i].articleID)            
            numberOfAuthors = len(authors)
            for j in range(numberOfAuthors):
                if j < numberOfAuthors - 1:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + ';').grid(row=0, column=j+1)
                else:
                    ttk.Label(articleFrame, text=authors[j].lastName + ', ' +
                              authors[j].firstName + '.').grid(row=0, column=j+1)
            link = ttk.Label(articleFrame, text=self.bookmarkedArticles[i].title + 
                      '.', foreground='blue', cursor='hand2')
            link.grid(row=0, column=numberOfAuthors+1)
            link.bind('<Button-1>', lambda e: os.startfile(self.bookmarkedArticles[i].filepath))
            ttk.Label(articleFrame, text=self.bookmarkedArticles[i].journal).grid(row=0, column=numberOfAuthors+2)
            if self.bookmarkedArticles[i].volume:
                ttk.Label(articleFrame, text=self.bookmarkedArticles[i].volume).grid(
                    row=0, column=numberOfAuthors+3)
            if self.bookmarkedArticles[i].publicationYear:
                ttk.Label(articleFrame, text='(%d),' %(self.bookmarkedArticles[i].publicationYear)).grid(
                    row=0, column=numberOfAuthors+4)
            if self.bookmarkedArticles[i].journalNumber:
                ttk.Label(articleFrame, text='no. %d, ' %(self.bookmarkedArticles[i].journalNumber)).grid(
                    row=0, column=numberOfAuthors+5)
            ttk.Label(articleFrame, text=self.bookmarkedArticles[i].pages + '.').grid(
                row=0, column=numberOfAuthors+6)
            
            ttk.Button(buttonFrame, text='Remove Bookmark', 
                       command=lambda: ArticleDAO.removeBookmarkByArticleID(
                           self.bookmarkedArticles[i].articleID)).grid(
                           row=0, column=0)
            
            articleFrame.grid(row=i, column=0, sticky='W')
            buttonFrame.grid(row=i, column=1)
        
        contentFrame.grid(row=0, column=0)
        
if __name__ == '__main__':
    from tkinter import Tk
    
    root = Tk()
    viewBookmarks(root)
    root.mainloop()
        