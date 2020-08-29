# -*- coding: utf-8 -*-

class Article:
    """Represents an article object in the database."""
    
    
    def __init__(self, articleID = None, title = '', journal = '', 
                 volume = None, journalNumber = None, 
                 publicationYear = None, pages = '', articleContent = '',
                 filepath = '', isBookmarked = False):
        self.articleID = articleID
        self.title = title
        self.journal = journal
        self.volume = volume
        self.journalNumber = journalNumber
        self.publicationYear = publicationYear
        self.pages = pages
        self.articleContent = articleContent
        self.filepath = filepath
        self.isBookmarked = isBookmarked
        
    def __str__(self):
        return self.articleContent
        