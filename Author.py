# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:54:05 2020

@author: cerya
"""

class Author:
    """Represents an author in the database."""
    
    def __init__(self, authorID = None, lastName = '', firstName = '', 
                 middleName = ''):
        self.authorID = authorID
        self.lastName = lastName
        self.firstName = firstName
        self.middleName = middleName
    
    def __str__(self):
        return self.lastName + ', ' + self.firstName + ' ' + self.middleName