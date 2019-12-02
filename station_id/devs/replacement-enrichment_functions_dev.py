#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:07:05 2019

@author: iregon
"""

import os
import json
import pandas as pd
from metmetpy.common import functions
import re
from .. import properties
from metmetpy.common import functions

module_path = os.path.dirname(os.path.abspath(__file__))
rep_strings_path = os.path.join(module_path,'replacement_maps')


def get_replacement_map(rep_map_name):
    rep_map_file = os.path.join(rep_strings_path,rep_map_name + '.json')
    with open(rep_map_file,'r') as fileObj:
        rep_map = json.load(fileObj)
    return rep_map

def deck_116_imma1(data):
    # from Liz's correct_ids.R and reformat_ids.R
    yr_col = properties.metadata_datamodels.get('year').get('imma1')
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    pt_col = properties.metadata_datamodels.get('platform').get('imma1')

    data[id_col] = data[id_col].str.strip()
    
    loc = (data[yr_col] == 1953) & (data[id_col] == '404')
    data[id_col].loc[loc] = '4045'
    
    regexes = re.compile(re.compile('|'.join(['^\d{4,5}$','^-\d{3,4}$'])))
    loc = (data[id_col].str.match(regexes))
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-US'
      
    regexes = re.compile('^\d{3}$')
    loc = (data[id_col].str.match(regexes)) & (data[pt_col] == '3')
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-US'
    
    return data

def deck_117_imma1(data):
    # from Liz's reformat_ids.R
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    
    data[id_col] = data[id_col].str.strip()
    
    regexes = re.compile(re.compile('|'.join(['^\d{4,5}$','^-\d{3,4}$'])))
    loc = (data[id_col].str.match(regexes))
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-US'
      
    regexes = re.compile('^\d{2}$')
    loc = (data[id_col].str.match(regexes))
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-US'
    
    return data

def deck_118_9_imma1(data):
    # from Liz's reformat_ids.R
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    dck_col = properties.metadata_datamodels.get('deck').get('imma1')
    yr_col = properties.metadata_datamodels.get('year').get('imma1')
    
    data[id_col] = data[id_col].str.strip()
    
    regexes = re.compile('^\d{6}$')
    loc = data[id_col].str.match(regexes)
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-d' + data[dck_col].loc[loc]
    
    loc = data[id_col].str.len() == 3 & (data[id_col].str[-2:] == data[yr_col].astype(str).str[-2:])
    data[id_col].loc[loc] = '-' + data[yr_col].astype(str).str[-2:].loc[loc] + data[id_col].str[-2:]
    
    loc = data[id_col].str.len() == 5
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-d' + data[dck_col].loc[loc]
    
    return data


def deck_128_imma1(data):
    # from Liz's reformat_ids.R
    yr_col = properties.metadata_datamodels.get('year').get('imma1')
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    
    data[id_col] = data[id_col].str.strip()
    
    regexes = re.compile(re.compile('|'.join(['^\d{4,5}$','^-\d{3,4}$'])))
    loc = (data[id_col].str.match(regexes)) & (data[yr_col] <= 1965 )
    data[id_col].loc[loc] = data[id_col].loc[loc] + '-US'

    return data

def deck_184_imma1(data):
    # from Liz's reformat_ids.R
    yr_col = properties.metadata_datamodels.get('year').get('imma1')
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    pt_col = properties.metadata_datamodels.get('platform').get('imma1')
    
    s1 = data[id_col].str[0:3].str.strip()
    s1.loc[ data[pt_col] == '0' ] = '09 '
    s1.loc[s1.str[-1] == '4']  = '14 '
    s1.loc[s1.str[-1] == '0']  = '10 '
    s1.loc[s1.str[-2:] == '01']  = '14 '
    s1.loc[(s1.str[-2:] == '31') & (data[yr_col] < 1956)]  = '10 '
    s1.loc[(s1.str[-2:] == '31') & (data[yr_col] >= 1956)]  = '14 '
    
    s2 = '000000' + data[id_col].str[3:].str.strip()[-4:]
    s2.loc[s2 == '0000']  = '0'
    s2.loc[s2 == '00NA']  = '0'
    
    data[id_col] = s1 + s2

    return data




def deck_197_imma1(data):
    # Danish Polar, variety of ids
    rep_map_name = 'ids_to_join_720'
    rep_map = get_replacement_map(rep_map_name)
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    sid_col = properties.metadata_datamodels.get('source').get('imma1')

    loc = data[sid_col].isin(['134','136'])

    data[id_col].loc[loc] = data[id_col].loc[loc].map(functions.smart_dict(rep_map))
    
    return data



def deck_701_imma1(data):
#    WE NEED TO MAKE THIS DATE DEPENDENT AS FILLNA TO FOLLOW DEPENDS ON IT
    # REcover long names from ancilliary info
    # US Maury, names from list on ICOADS website: http://icoads.noaa.gov/software/transpec/maury/mauri_out
    rep_map_name = 'usmaury_names_c0_imma1'
    rep_map = get_replacement_map(rep_map_name)
    data[id_col] = data[id_col].map(functions.smart_dict(rep_map))
    # Now fill in empty info use common.fill_value()
    yr_col = properties.metadata_datamodels.get('year').get('imma1')
    mm_col = properties.metadata_datamodels.get('month').get('imma1')
    data[id_col].loc[(data[yr_col] == 1850) & (data[id_col].isna())] = 'Unknown_701_1'
    data[id_col].loc[(data[yr_col] == 1851) & (data[mm_col] <= 2 ) & (data[id_col].isna())] = 'Unknown_701_1'
    data[id_col].loc[(data[yr_col] == 1851) & (data[mm_col] == 4 ) & (data[id_col].isna())] = 'Unknown_701_2'
    data[id_col].loc[(data[yr_col] == 1851) & (data[mm_col] == 12 ) & (data[id_col].isna())] = 'Unknown_701_3'
    return data


def deck_721_imma1(data):
    # German Maury, make corrections based on extended length ids from US Maury, assign missing
    rep_map_name = '721_imma1'
    rep_map = get_replacement_map(rep_map_name)
    data[id_col] = data[id_col].map(functions.smart_dict(rep_map))
    # Now fill in empty info use common.fill_value()
#    yr < 1986 "Unknown_701_1"
#    yr == 1851  mo <= 2, "Unknown_701_1"
#    yr == 1851  mo == 4, "Unknown_701_2"
#    yr == 1851  mo == 12, "Unknown_701_3"
    return data


def sequential_logbook_720_imma1(data):
    rep_map_name = 'ids_to_join_720'
    rep_map = get_replacement_map(rep_map_name)
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    sid_col = properties.metadata_datamodels.get('source').get('imma1')

    loc = data[sid_col].isin(['134','136'])

    data[id_col].loc[loc] = data[id_col].loc[loc].map(functions.smart_dict(rep_map))
    
    return data