#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:43:53 2019

@author: iregon
"""
import pandas as pd
import numpy as np
from metadatafix.initial_functions import fill_value
from random import randint

df = pd.DataFrame({'A': [randint(1, 9) for x in range(10)],
                   'B': [randint(1, 9)*10 for x in range(10)],
                   'C': [randint(1, 9)*100 for x in range(10)]})



def all_is_None(df):
    dft = df.copy()
    dft.iloc[0,0] = np.nan
    return fill_value(dft['A'],fill_value = 'A')

def self_condition_set(df):
    dft = df.copy()
    dft.iloc[0,0] = 8
    return fill_value(dft['A'],fill_value = 'A',self_condition_value = 8)

def self_condition_is_None_other_is_series(df):
    dft = df.copy()
    return fill_value(dft['A'],fill_value = 'A',out_condition = dft['B'], 
                      out_condition_values = {'B':60})
    
def self_condition_is_set_other_is_series(df):
    dft = df.copy()
    return fill_value(dft['A'],fill_value = 'A',self_condition = 
                      out_condition = dft['B'], 
                      out_condition_values = {'B':60})