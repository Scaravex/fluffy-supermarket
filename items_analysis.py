# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 10:02:42 2017

@author: scaravex
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getDummies(dfz, col, minCtn=10):
    '''
    function which create dummy variables 
    for the different categories
    '''    
    df2 = dfz.copy()
    df2['_id'] = 1
    df_aux = df2.groupby(col).aggregate({'_id':'count'}).reset_index() 
    df_aux = df_aux[df_aux._id>=minCtn]
    topColTypes = list(set(df_aux[col].values))
    dfz[col] = dfz.apply(lambda r: r[col] if r[col] in topColTypes else 'OTHER' , axis=1)
    dummies = pd.get_dummies(dfz[col], prefix=col) # +'_')

    return dummies, topColTypes


def cleaning_items (items):
    '''
    function which reduces the categories for unfrquent factors,
    output is a reduced family types
    '''
    ## if it is a small category, put OTHER (ideally: OTHER_Perishable and OTHER_nonPerishable)
    items['family']=items['family'].astype('category')
    frequency_count = items['family'].value_counts()/items['family'].count()
    #categories which appears less than 1%
    threshold = 0.01 
    # cond whether the ratios is higher than the threshold
    mask =  items['family'].isin(frequency_count[frequency_count>=threshold].index)
    # replace the ones which ratio is lower than the threshold with "Others"
    items['reduced_family'] = np.where(mask == True,items['family'], "Others")
    items.drop('family', axis=1, inplace=True)

    return items

items = pd.read_csv('items.csv', encoding="UTF-8")
items.describe()
items['family'] = items['family'].astype('category')
plt.hist(items['family'].value_counts())
items['family'].value_counts()/items['family'].count()

items.groupby('family').mean()

items = cleaning_items (items)
plt.hist(items['reduced_family'].value_counts())

''' 
--> da capire se nel big dataset queste colonne sono simile e studiarne la stagionalità
GROCERY I                     1334
BEVERAGES                      613
CLEANING                       446
PRODUCE                        306
DAIRY                          242
PERSONAL CARE                  153
BREAD/BAKERY                   134
HOME CARE                      108
DELI                            91
MEATS                           84
HOME AND KITCHEN I              77
LIQUOR,WINE,BEER                73
FROZEN FOODS                    55
POULTRY                         54
'''

'''  Perishable:
BREAD/BAKERY
DAIRY
DELI
EGGS
MEATS
POLTRY
PREPARED FOODS
PRODUCE
SEAFOOD
'''

test = pd.read_csv('test.csv', encoding="UTF-8")
test.head()

new_test = pd.merge(test,items, on='item_nbr')
