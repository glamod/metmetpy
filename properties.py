#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:18:41 2019


@author: iregon
"""

metadata_datamodels = {}

metadata_datamodels['deck'] = {}
metadata_datamodels['deck']['imma1'] = ('c1','DCK')

metadata_datamodels['source'] = {}
metadata_datamodels['source']['imma1'] = ('c1','SID')

metadata_datamodels['platform'] = {}
metadata_datamodels['platform']['imma1'] = ('c1','PT')
metadata_datamodels['platform']['cdm'] = ('header','platform_type')

metadata_datamodels['id'] = {}
metadata_datamodels['id']['imma1'] = ('core','ID')
metadata_datamodels['id']['cdm'] = ('header','primary_station_id')

metadata_datamodels['year'] = {}
metadata_datamodels['year']['imma1'] = ('core','YR')

metadata_datamodels['month'] = {}
metadata_datamodels['month']['imma1'] = ('core','MO')

metadata_datamodels['day'] = {}
metadata_datamodels['day']['imma1'] = ('core','DY')

metadata_datamodels['hour'] = {}
metadata_datamodels['hour']['imma1'] = ('core','HR')

metadata_datamodels['datetime'] = {}
metadata_datamodels['datetime']['cdm'] = ('header','report_timestamp')
