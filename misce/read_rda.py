#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 07:51:48 2019

@author: iregon
"""
import pyreadr
import pandas as pd

rda_path = '/Users/iregon/dessaps/metadatafix/test_data/rda/tracking/athena/1992.4.Rda'

data_dict = pyreadr.read_r(rda_path)
data_frame = data_dict[None]