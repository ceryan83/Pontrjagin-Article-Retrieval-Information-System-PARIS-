# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:52:52 2020

@author: cerya
"""
from dao import ArticleDAO

from utilities import GetContent
import os
    
def populateList(parent, res = list()):
    for name in os.listdir(parent):
        path = os.path.join(parent, name).replace('\\', '/')
        if os.path.isfile(path):
            if '.pdf' in path:
                res.append(path)
        else:
            populateList(path, res)
    return res

def processPDF(filepath, title = '', journal = '', volume = None, 
               journalNumber = None, publicationYear = None, pages = ''):
    article = ArticleDAO.Article.Article()
    article.articleContent = GetContent.getContentFromPDF(filepath)
    article.filepath = filepath
    article.title = title
    article.journal = journal
    article.volume = volume
    article.journalNumber = journalNumber
    article.publicationYear = publicationYear
    article.pages = pages
    
    ArticleDAO.addArticle(article)
    
if __name__ == '__main__':
    parent = 'C:\\Users\\cerya\\Dropbox\\Mathematics\\Research\\ReferencePapers'
    filepaths = populateList(parent)
    print(len(filepaths))
    
        