#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:43:53 2019

@author: iregon
"""
import sys
sys.path.append('/Users/iregon/dessaps')
import os
import mdf_reader
from metmetpy.station_id import validate as validate_id
from metmetpy.datetime import validate as validate_datetime
from metmetpy.datetime import correct as correct_datetime
from metmetpy.platform_type import platform_type
import numpy as np

test_data_path = '/Users/iregon/dessaps/metmetpy/tests/data'


def test_id_fix(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core','c1'])
    imma_data_orig = imma_data.copy()
#    imma_data['data'][('core','ID')].iloc[0] = np.nan
    non_ascii_out = os.path.join(test_data_path,sid_dck,date_stamp + '_non_ascii_id.json')
    try:
        os.remove(non_ascii_out)
    except OSError:
        pass
   
    imma_data = station_id.make_conform(imma_data['data'],data_model)
    return imma_data,imma_data_orig['data']





def test_pt_fix(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core','c1'],chunksize = 1000)
    #imma_data['data'][('c1','PT')].iloc[0] = np.nan
    imma_data['data'] = platform_type.fix(imma_data['data'],data_model)
    return imma_data

def test_datetime_validation(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core'])  
    imma_data['valid_mask'][('core','datetime')] = validate_datetime.validate(imma_data['data'],data_model)
    return imma_data

def test_datetime_correction(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core'])  
    return correct_datetime.correct(imma_data['data'],data_model,sid_dck.split("-")[1])

def test_id_validation(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core'])  
    imma_data['valid_mask'][('core','ID')] = validate.validate(imma_data['data'][('core','ID')],data_model,sid_dck.split("-")[1])
    return imma_data

def test_id_validation_chunks(sid_dck,date_stamp,data_model):
    imma_path = os.path.join(test_data_path,sid_dck,date_stamp + '.imma')
    imma_data = mdf_reader.read(imma_path,data_model = data_model,sections = ['core'],chunksize = 30000) 
    for data,mask in zip(imma_data['data'],imma_data['valid_mask']):
        mask[('core','ID')] = validate.validate(data[('core','ID')],data_model,sid_dck.split("-")[1])
    return data[('core','ID')],mask[('core','ID')]

#sid_dck = '096-702'
#date_stamp = '1889-07'
#data_model = 'imma1'
#imma_fixed = test_id_fix(sid_dck,date_stamp,data_model)

#sid_dck = '125-704'
#date_stamp = '1894-02'
#data_model = 'imma1'
#imma_fixed = test_id_fix(sid_dck,date_stamp,data_model)

#sid_dck = '133-730'
#date_stamp = '1854-10'
#data_model = 'imma1'
#imma_fixed = test_id_fix(sid_dck,date_stamp,data_model)

#sid_dck = '069-701'
#date_stamp = '1863-05'
#data_model = 'imma1'
#imma_fixed = test_pt_fix(sid_dck,date_stamp,data_model)

#sid_dck = '152-721'
#date_stamp = '1866-10'
#data_model = 'imma1'
#imma_fixed = test_pt_fix(sid_dck,date_stamp,data_model)
    
sid_dck = '001-116'
date_stamp = '1960-12'
data_model = 'imma1'
validated = test_datetime_correction(sid_dck,date_stamp,data_model)