# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:47:03 2020

@author: cerya
"""
import numpy as np
import pandas as pd
import sqlalchemy

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import scispacy
import spacy
import en_core_sci_lg

from scipy.spatial.distance import jensenshannon

import joblib

from IPython.display import HTML, display

from ipywidgets import interact, Layout, HBox, VBox, Box
import ipywidgets as widgets
from IPython.display import clear_output

from tqdm import tqdm
from os.path import isfile

import seaborn as sb
import matplotlib.pyplot as plt

from dao import ArticleDAO

#%%
class Calibrate():
    
    def __init__(self):
        engine = sqlalchemy.create_engine("postgresql://postgres:4rt1n14n@localhost:5432/Pontrjagin", 
                                          connect_args={'gssencmode':'disable'})        
        df = pd.read_sql_table('articles', 
                               engine, index_col='articleid', 
                               columns=['articleid', 'title', 'articlecontent'])       
        all_texts = df.articlecontent
            
        self.nlp = en_core_sci_lg.load(disable=["tagger", "parser", "ner"])
        self.nlp.max_length = 3000000
    
        customize_stop_words = [
            'doi', 'preprint', 'copyright', 'org', 'https', 'et', 'al', 'author', 'figure', 'table',
            'rights', 'reserved', 'permission', 'use', 'used', 'using', 'biorxiv', 'medrxiv', 'license', 
            'fig', 'fig.', 'al.', 'Elsevier', 'PMC', 'CZI', '-PRON-', 'usually', 'theorem', 'let', 'example',
            'leave', 'lemma', 'satisfy', 'proof', 'r.', 'denote', 'g.', 'general', 'fact', 'give', 'e.', 'math', 
            'follow', 'form', 'shall', 'suppose', 'ii', 'iii', 'p.', 'j.', 'prove', 'a.', 't', 
            'imply', 'property', 'assume', 'note', 'define', 'ij', 'show', 'have', 'theory',
            'call', 'write', 'construct', 'epi-', 'https://about.jstor.org/terms',
            r'\usepackage{amsbsy', r'\usepackage{amsfonts', r'\usepackage{mathrsfs', r'\usepackage{amssymb', r'\usepackage{wasysym',
            r'\setlength{\oddsidemargin}{-69pt',  r'\usepackage{upgreek', r'\documentclass[12pt]{minimal'
        ]
    
        for w in customize_stop_words:
            self.nlp.vocab[w].is_stop = True
            
        vectorizer = CountVectorizer(tokenizer = self.spacy_tokenizer, min_df=2)
        data_vectorized = vectorizer.fit_transform(tqdm(all_texts))
    
        word_count = pd.DataFrame({'word': vectorizer.get_feature_names(), 
                                    'count': np.asarray(data_vectorized.sum(axis=0))[0]})
        
        word_count.sort_values('count', ascending=False).set_index('word')[
            :25].sort_values('count', ascending=True).plot(kind='barh')
    
        joblib.dump(vectorizer, 'vectorizer.csv')
        joblib.dump(data_vectorized, 'data_vectorized.csv')
        
        lda = LatentDirichletAllocation(n_components=min(len(all_texts)//4 + 1,50), random_state=0)
        lda.fit(data_vectorized)
        joblib.dump(lda, 'lda.csv')
            
        self.print_top_words(lda, vectorizer, 25)
        
        doc_topic_dist = pd.DataFrame(lda.transform(data_vectorized),
                                      index=df.index)
        doc_topic_dist.to_csv('doc_topic_dist.csv')   

        print('Calibration complete.')        
    
    def print_top_words(self, model, vectorizer, n_top_words):
        feature_names = vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(model.components_):
            message = "\nTopic #%d: " % topic_idx
            message += " ".join([feature_names[i]
                                  for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
        print()
    
    def spacy_tokenizer(self, sentence):
        return [word.lemma_ for word in self.nlp(sentence) if not (word.like_num or 
                                                              word.is_stop or 
                                                              word.is_punct or 
                                                              word.is_space or 
                                                              len(word)==1)]

def get_k_nearest_docs(articleID, k=5, get_dist=False):
    '''
    doc_dist: topic distribution (sums to 1) of one article
    
    Returns the index of the k nearest articles (as by Jensen–Shannon divergence in topic space). 
    '''
    doc_topic_dist = pd.read_csv('doc_topic_dist.csv', index_col='articleid')
    doc_dist = doc_topic_dist[doc_topic_dist.index == articleID].values[0]
    
    distances = doc_topic_dist.apply(lambda x: jensenshannon(x, doc_dist), axis=1)
    k_nearest = distances[distances != 0].nsmallest(n=k).index
    articleIDs = list()
    for i in range(len(k_nearest)):
        articleIDs.append(int(k_nearest.values[i]))
    if get_dist:
        k_distances = distances[distances != 0].nsmallest(n=k)
        similarities = list()
        for i in range(len(k_distances)):
            similarities.append(int(k_distances.values[i]*100))
        return articleIDs, similarities
    else:
        return articleIDs
    
if __name__ == '__main__':
    articleIDs, distances  = get_k_nearest_docs(1, get_dist=True)