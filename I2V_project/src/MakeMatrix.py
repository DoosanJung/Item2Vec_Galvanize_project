#!/usr/bin/env Python
'''

'''

import logging
from logging import config
import numpy as np
import pandas as pd
from scipy import sparse, io
from itertools import chain
import matplotlib.pyplot as plt
from I2V_project.conf.I2VConfig import I2VConfig
from I2V_project.src.DataPrep import DataPrep


config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()


class MakeMatrix(object):
    '''
    make matrices from the data
    '''
    def __init__(self, n_rows, n_cols, df):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.df = df

    def get_rating_matrix(self): # train_df
        '''
        make a sparse matrix where rows correspond to users and columns correspond
        to items. Each element is the user's rating for that item
        '''
        logger.info('Trying to make a rating_matrix..')
        try:
            if not all(self.df.columns.isin([u'userId', u'movieId', u'rating', u'timestamp'])):
                logger.error("df columns do not match")
                raise
            matrix = sparse.lil_matrix((self.n_rows, self.n_cols))
            for _, row in self.df.iterrows():
                # subtract 1 from id's due to match 0 indexing
                matrix[row.userId - 1, row.movieId - 1] = row.rating
            logger.info('Succeed in making a rating_matrix')
            return matrix
        except:
            logger.error('Failed to make a rating_matrix')
            raise

    def get_item_matrix(self, up, down):
        '''
        (1 <= up, down <= 5)

        make a item matrix where
        a positive element represents liked item by the user (rating greater than or equal to 'up' value),
        a negative element represents disliked item by the user (rating smaller than 'down' value),
        and a zero element represents neutral item by the user
        '''
        logger.info('Trying to make a item_matrix..')
        try:
            if not all(self.df.columns.isin([u'userId', u'movieId', u'rating', u'timestamp'])):
                logger.error("df columns do not match")
                raise
            matrix = sparse.lil_matrix((self.n_rows, self.n_cols))
            for _, row in self.df.iterrows():
                if row.rating >= up:
                    matrix[row.userId - 1, row.movieId - 1] = row.movieId
                elif row.rating < down:
                    matrix[row.userId - 1, row.movieId - 1] = -1 * row.movieId
            logger.info('Succeed in making a item_matrix')
            return matrix
        except:
            logger.error("Failed to make a item_matrix")
            raise
