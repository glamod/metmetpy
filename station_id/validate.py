#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:00:19 2019

Validates ID field in a pandas dataframe against a list of regex patterns.
Output is a boolean series.

Does not account for input dataframes/series stored in TextParsers: as opposed
to correction modules, the output is only a boolean series which is external
to the input data ....

Validations are dataset and deck specific following patterns stored in
 ./lib/dataset.json.: multiple decks in input data are not supported.

If the dataset is not available in the lib, the module
will return with no output (will break full processing downstream of its
invocation) logging an error.

ID corrections assume that the id field read from the source has
been white space stripped. Care must be taken that the way a data model
is read before input to this module, is coherent to the way patterns are
defined for that data model.

NaN: wil validate to true if blank pattern ('^$') in list, otherwise to False.

If patterns:{} for dck (empty but defined in data model file),
will warn and validate all to True, with NaN to False

@author: iregon
"""

import json
import pandas as pd
import os
from metmetpy.common import logging_hdlr
import re
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


def validate(data,dataset,data_model,dck,sid = None,blank = False, log_level = 'INFO'):
    logger = logging_hdlr.init_logger(__name__,level = log_level)

    if not isinstance(data,pd.DataFrame) and not isinstance(data,pd.Series):
        logger.error('Input data must be a pd.DataFrame or pd.Series.\
                     Input data type is {}'.format(type(data)))
        return


    id_col = properties.metadata_datamodels['id'].get(data_model)
    if not id_col:
        logger.error('Data model {} ID column not defined in\
                     properties file'.format(data_model))
        return

    idSeries = data[id_col]

    data_model_file = os.path.join(module_path,'lib',dataset+ '.json')
    if not os.path.isfile(data_model_file):
        logger.error('Input dataset "{}" has no ID deck library'
                       .format(dataset))
        return

    with open(data_model_file) as fileObj:
        id_models = json.load(fileObj)

    dck_id_model = id_models.get(dck)
    if not dck_id_model:
        logger.error('Input dck "{0}" not defined in file {1}'
                     .format(dck,data_model_file))
        return

    pattern_dict = dck_id_model.get('valid_patterns')

    if pattern_dict == {}:
        logger.warning('Input dck "{0}" validation patterns are empty in file {1}'
                     .format(dck,data_model_file))
        logger.warning('Adding match-all regex to validation patterns')
        patterns = ['.*?']
    else:
        patterns = list(pattern_dict.values())

    if blank:
        patterns.append('^$')
        logger.warning('Setting valid blank pattern option to true')
        logger.warning('NaN values will validate to True')

    na_values = True if '^$' in patterns else False
    combined_compiled = re.compile('|'.join(patterns))

    return idSeries.str.match(combined_compiled,na = na_values)
