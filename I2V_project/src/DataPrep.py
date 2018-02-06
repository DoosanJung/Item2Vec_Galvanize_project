#!/usr/bin/env Python
'''

'''

import logging
from logging import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from __future__ import division
from I2V_project.conf.I2VConfig import I2VConfig


config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()


class DataPrep(object):
    '''
        import data and split train/test data
    '''


    def __init__(self):
        self.home_path = I2VConfig.HOME_PATH
        self.file_path = I2VConfig.get_config()['FILE_PATH']
        self.columns = I2VConfig.COLUMNS

    def get_ratings(self):
        '''
            get movies and their ratings
        '''
        ratings = pd.read_table(self.home_path + self.file_path['ratings_testdata'],
                                         names = self.columns['ratings_columns'])
        highest_user_id = ratings.userId.max()
        highest_movie_id = ratings.movieId.max()

    def get_items(self):
        '''
        '''
        movies_contents = pd.read_table(self.home_path + self.file_path['movies_testdata'],
                                sep = '|',
                                header = None,
                                names = self.columns['movies_columns'])
        movies_contents = movies_contents.ix[:,[0,1,2]]
        movies_contents= movies_contents.set_index('movieId')
