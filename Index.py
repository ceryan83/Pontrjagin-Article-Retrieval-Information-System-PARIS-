# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:54:34 2020

@author: cerya
"""
from whoosh import index
from whoosh.fields import NUMERIC, Schema, TEXT
from whoosh.qparser import MultifieldParser

import os

def deleteDocument(articleID):
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        ix = index.create_in("indexdir", getSchema())
        
    ix = index.open_dir("indexdir")
    writer = ix.writer()
    writer.delete_by_term('articleID', articleID)
    writer.commit()
    print('Document removed from index.')

def getSchema():
    return Schema(articleID=NUMERIC(stored=True, unique=True),
                authors=TEXT,
                title=TEXT(field_boost=2.0),
                journal=TEXT,
                publicationYear=NUMERIC,                
                articleContent=TEXT)

def indexDocument(article, authors):
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        ix = index.create_in("indexdir", getSchema())
        print('Index created.')
        
    ix = index.open_dir("indexdir")
    
    authorString = ''
    for i in range(len(authors)):
        if authors[i].middleName != '':
            authorString += authors[i].lastName + ', '
            authorString += authors[i].firstName + ' '
            authorString += authors[i].middleName 
        else:
            authorString += authors[i].lastName + ', '
            authorString += authors[i].firstName
        if i < len(authors) - 1:
            authorString += '; '
    
    writer = ix.writer()
    writer.update_document(articleID = article.articleID, authors = authorString,
                           title = article.title, journal = article.journal,
                           publicationYear = article.publicationYear,
                           articleContent = article.articleContent)
    writer.commit()
    print('Document indexed.')
    
def searchIndex(query):
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        ix = index.create_in("indexdir", getSchema())
        
    ix = index.open_dir("indexdir")
    
    qp = MultifieldParser(['authors', 'title', 'articleContent'], schema=ix.schema)
    q = qp.parse(query)
    
    with ix.searcher() as searcher:
        results = searcher.search(q)
        articleIDs = list()
        for i in range(min(10, len(results))):
            articleIDs.append(results[i]['articleID'])
        print('Obtained %d hits. Returning results.' % (len(articleIDs)))
    return articleIDs
    

    