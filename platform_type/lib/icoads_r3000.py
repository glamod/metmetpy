#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:07:05 2019

@author: iregon
"""

import os
import numpy as np
import pandas as pd
from metmetpy.common import functions
import re
from .. import properties


def deck_700_imma1(data):
    #idt=="NNNNN" & dck==700 & sid == 147 & pt == 5
    drifters = '7'
    sid = '147'
    pt = '5'
    buoys = '6'
    regex = re.compile('^\d{5,5}$')
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    sid_col = properties.metadata_datamodels.get('source').get('imma1')
    pt_col = properties.metadata_datamodels.get('platform').get('imma1')

    data[pt_col].iloc[np.where(data[pt_col].isna())] = drifters
    loc = (data[id_col].str.match(regex)) & (data[sid_col] == sid )\
        & (data[pt_col] == pt )

    data[pt_col].loc[loc] = buoys

    return data

def deck_892_imma1(data):
    #idt=="NNNNN" & dck==892 & sid == 29 & pt == 5
    sid = '29'
    pt = '5'
    buoys = '6'
    regex = re.compile('^\d{5,5}$')
    id_col = properties.metadata_datamodels.get('id').get('imma1')
    sid_col = properties.metadata_datamodels.get('source').get('imma1')
    pt_col = properties.metadata_datamodels.get('platform').get('imma1')

    loc = (data[id_col].str.match(regex)) & (data[sid_col] == sid )\
        & (data[pt_col] == pt )

    data[pt_col].loc[loc] = buoys

    return data
