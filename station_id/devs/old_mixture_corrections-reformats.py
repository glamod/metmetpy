#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:00:19 2019

Forces id field format comformity in 2 stages:
    1. corrects deck specific known errors in names/callsigns
    2. applies common format comformity rules
    
To account for dataframes stored in TextParsers and for eventual use of data columns other
than those to be fixed in this or other metmetpy modules,
the input and output are the full data set.

Specific corrections/replacememnts (stage 1) to apply are data model and deck
specific and are registered in ./lib/data_model.json. 

The deck is accessed from the corresponding data model column. Multiple decks
are not supported. In the event of multiple decks in the input data, the module
will return with no output (will break full processing downstream of its 
invocation) logging an error. 

Reference names of different metadata fields used in the metmetpy modules
and its location column|(section,column) in a data model are
registered in ../properties.py in metadata_datamodels.

If the data model is not available in ./lib it is assumed to no corrections are
needed (no stage 1). It will just log a warning.
If the data model is not available in metadata_models, the module
will return with no output (will break full processing downstream of its 
invocation) logging an error. 

After stage 1, id is supposed to be ascii.....

Some of the ID corrections assume that the id field read from the source has
not been white space stripped. Care must be taken that the way a data model 
is read before input to this module, is coherent to the way corrections are
performed for that data model.
                          
@author: iregon
"""

import json
import importlib
import pandas as pd
import numpy as np
import os
from io import StringIO
from unidecode import unidecode
from string import punctuation
from metmetpy.common import logging_hdlr
from .. import properties

class smart_dict(dict):
    def __init__(self, *args):
        dict.__init__(self,*args)
 
    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val
 
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
 
    def __missing__(self, key):
        key = key
        return key

tool_name = 'metmetpy'
module_path = os.path.dirname(os.path.abspath(__file__))

functions_module_path = os.path.join(module_path,'correction_functions')
functions_module_tree = functions_module_path[functions_module_path.find('/' + tool_name + '/')+1:].split('/')
id_functions_mdl = importlib.import_module('.'.join(functions_module_tree), package=None)

correction_method_path = os.path.join(module_path,'lib')
cor_maps_path = os.path.join(module_path,'correction_maps')

#   
#def correct_id(data,data_model,id_correction_,log_level = 'INFO'):
#    logger = logging_hdlr.init_logger(__name__,level = log_level) 
#    id_col = properties.metadata_datamodels['id'].get(data_model)
##    in:
##        - pd.Series with ID: when fixing is independent of other parameters or
##       and we just have this info
##        - pd.DataFrame with all (need to give idColumn name): applicable also to
##        case above, but specially to enable dependencies on other fields.
##    out: pdSeries with ID fixed
#     
##    Find replacement method and apply
#    id_correction = id_correction_.get('corrections')
#    if id_correction.get('method') == 'map':
#        cor_map_name = id_correction.get('map')
#        rep_map_file = os.path.join(cor_maps_path,cor_map_name + '.json')
#        with open(rep_map_file,'r') as fileObj:
#            rep_map = json.load(fileObj)
#        if id_correction.get('fill_value'):
#            data[id_col].iloc[np.where(data[id_col].isna())] = id_correction.get('fill_value')
#        data[id_col] = data[id_col].map(smart_dict(rep_map))    
#        return data
#    elif id_correction.get('method') == 'function':
#        transform = id_correction.get('function')
#        trans = eval('id_functions_mdl.' + transform)
#        data = trans(data)
#        return data
#    elif id_correction.get('method') == 'TBD':
#        logger.warning('Replacement method to confirm/define: {}'.format(id_correction.get('what')))
#        return data
#    elif id_correction.get('method') == 'fillna':
#        data[id_col].iloc[np.where(data[id_col].isna())] = id_correction.get('fill_value')
#        return data
#    else:
#        logger.error('Replacement method not available: {}'.format(id_correction.get('method')))
#        return
    
#def reformat_id(id_data, log_level = 'INFO'):
#    logger = logging_hdlr.init_logger(__name__,level = log_level)
##   This formating derived from Liz's reformatting of cliwoc names before
##   replacement in dck 730 and from the general reformatting performed to all
##   decks:
##   cliwoc_names<-trimws(cliwoc_names)
##   cliwoc_names<-gsub(" ","XXXX",cliwoc_names)
##   cliwoc_names<-gsub("[[:punct:]]","-",cliwoc_names)
##   cliwoc_name<-iconv(cliwoc_names, to = "ASCII//TRANSLIT")
##   cliwoc_names<-gsub("XXXX","_",cliwoc_names) 
#    
##   We basically:
##   ensure is ascii
##   ensure trimmed
##   spaces to _
##   punctuations to -
#    logger.info('Forcing ascii...')
#    id_data.loc[id_data.notna()] = id_data[id_data.notna()].apply(unidecode)
#    logger.info('Removing leading/trailing blanks...')
#    id_data = id_data.str.strip()
#    logger.info('Punctutation characters to "-"')
#    pattern = r"[{}]".format(punctuation)
#    id_data = id_data.str.replace(pattern, "-")
#    logger.info('Blanks to unsderscore')
#    id_data = id_data.str.replace(" ", "_")
#    return id_data   
                    

def correct_it(data,data_model,deck,non_ascii_out = 'print',
                    log_level= 'INFO'):
    logger = logging_hdlr.init_logger(__name__,level = log_level)            
    
    id_col = properties.metadata_datamodels['id'].get(data_model)

    # Optional deck specific corrections
    correction_method_file = os.path.join(correction_method_path,data_model+ '.json')
    with open(correction_method_file,'r') as fileObj:
        correction_method = json.load(fileObj) 
    id_correction = correction_method.get(deck)
    if not id_correction.get(deck) or not id_correction.get(deck,{}).get('corrections'):
        logger.info('No replacements to apply to deck {0} data from data\
                    model {1}'.format(deck,data_model))
        from_non_ascii = []
    else:
        logger.info('Applying "{0}" replacement method'.format(id_correction.get('corrections').get('method')))
        try:
            data = correct_id(data,data_model,id_correction)
        except Exception:
            logger.error('Applying replacement', exc_info=True)
            return
        from_non_ascii = []
#       keep track of remaining non ascii IDs after replacement: these need to stand out!
#        id_ascii = id_data.copy()
#        id_ascii[id_ascii.notna()] = id_ascii[id_ascii.notna()].apply(unidecode)
#        from_non_ascii = id_data[id_data != id_ascii].dropna()
  
#    # 2. Common ID building rules
#    try:
#        logger.info('Applying common ID formatting rules')
#        data[id_col] = reformat_id(data[id_col])
#    except Exception:
#        logger.error('Applying common ID formatting rules', exc_info=True)
#        return    
#        
#    if len(from_non_ascii)>0:
#        from_non_ascii = pd.concat([from_non_ascii.rename('id from original or replacement'),id_data.iloc[from_non_ascii.index].rename('current id')],axis = 1)
#        if len(from_non_ascii)>0:
#            dict_out = from_non_ascii.drop_duplicates(keep='last').set_index('current id').to_dict(orient='index')
#            list_out = [ ":".join(k,v) for k,v in dict_out.items() ]
#            if non_ascii_out == 'print':
#                logger.info('List of ID that remained non ascii after ID replacement, prior to final ID reformatting:'.format(",".join(list_out)))
#            else:
#                if os.path.isdir(os.path.dirname(non_ascii_out)):
#                    with open(non_ascii_out,'w') as fileObj:
#                        json.dump(dict_out,fileObj,indent=4,ensure_ascii=False)
#                else:
#                    logger.error('Saving non ascii IDs to file {}'.format(non_ascii_out))
#                    logger.info('List of ID that remained non ascii after ID replacement, prior to final ID reformatting:'.format(",".join(list_out)))
    return data


def correct(data,data_model,deck,non_ascii_out = 'print',log_level= 'INFO'):
    logger = logging_hdlr.init_logger(__name__,level = log_level)
           
    correction_methods_file = os.path.join(correction_method_path,data_model+ '.json')
    if not os.path.isfile(correction_methods_file):
        logger.error('Data model {} has no corrections in library'
                       .format(data_model))
        return

    
    id_col = properties.metadata_datamodels['id'].get(data_model)
    
    if not id_col:
        logger.error('Data model {} ID column not defined in\
                     properties file'.format(data_model)) 
        return
    
    if isinstance(data,pd.DataFrame):
        data = correct_it(data,data_model,deck,non_ascii_out = 'print',
                               log_level= 'INFO') 
        return data  
    elif isinstance(data,pd.io.parsers.TextFileReader):
        read_params = ['chunksize','names','dtype','parse_dates','date_parser',
                       'infer_datetime_format']
        read_dict = {x:data.orig_options.get(x) for x in read_params}
        buffer = StringIO() 
        for df in data:
            df = correct_it(df,data_model,deck,non_ascii_out = 'print',
                                 log_level= 'INFO')
            df.to_csv(buffer,header = False, index = False, mode = 'a')
      
        buffer.seek(0)
        return pd.read_csv(buffer,**read_dict)
