#!/usr/bin/env Python
'''

'''

import logging
from logging import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from I2V_project.conf.I2VConfig import I2VConfig


config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()


class DataPrep(object):
    '''
    Import data and split train/test data per user
    Each user will have own train/test data
    '''
    def __init__(self):
        self.home_path = I2VConfig.HOME_PATH
        self.file_path = I2VConfig.get_config()['FILE_PATH']
        self.columns = I2VConfig.COLUMNS
        self.plot = I2VConfig.PLOT

    def get_ratings(self):
        '''
        get movies' rating
        '''
        logger.info('Trying to get ratings data')
        try:
            ratings = pd.read_table(self.home_path + self.file_path['ratings_testdata'],
                                             names = self.columns['ratings_columns'])
            # check missing userId or movieId
            if len(ratings.userId.unique()) != ratings.userId.max():
                logger.error('missing userID')
                raise

            if len(ratings.movieId.unique()) != ratings.movieId.max():
                logger.error('missing movieId')
                raise

            self.highest_user_id = ratings.userId.max()
            self.highest_movie_id = ratings.movieId.max()
            logger.info('Succeed in getting ratings data')
            return ratings
        except:
            logger.error('Failed to get ratings data')
            raise

    def get_items(self):
        '''
        get movies' description
        '''
        logger.info('Trying to get movie data')
        try:
            items = pd.read_table(self.home_path + self.file_path['items_testdata'],
                                sep = '|',
                                header = None,
                                names = self.columns['items_columns'])
            items = items.iloc[:,[0,1,2]]
            items= items.set_index('movieId')
            logger.info('Succeed in getting movie data')
            return items
        except:
            logger.error('Failed to get movie data')
            raise

    def show_ratio_dist(self, split_ratio):
        '''
        show the distribution of train/test split ratios
        '''
        ratings = self.get_ratings()
        self.split_ratio = split_ratio # e.g. 70

        logger.info('Trying to visualize the distribution of train/test split ratios..')
        try:
            num_user = len(ratings.userId.unique())
            ratios = np.zeros(num_user)
            num_iter = 0
            for i in xrange(num_user):
                user = ratings[ratings['userId']==i+1]
                srtd_tmp_unique = user.timestamp.sort_values().unique()

                # past (70%), future(30%) for the user based on timestamp
                split = np.percentile(srtd_tmp_unique, self.split_ratio)
                future_u = len(srtd_tmp_unique[srtd_tmp_unique >= split])
                past_u = len(srtd_tmp_unique[srtd_tmp_unique < split])
                if past_u > 0:
                    ratios[i] = future_u / float(past_u)
                num_iter += 1
                if num_iter % 100 == 0:
                    logger.info('split_ratio iteration: {} out of {} users'.format(num_iter, num_user))

            # to show histogram of train/test split ratios..
            if self.plot == True:
                plt.hist(ratios, bins = 50)
                plt.show()

            logger.info( pd.Series(ratios).describe() )
            logger.info('argmin: user no.{}'.format(ratios.argmin()+1))
            logger.info('argmax: user no.{}'.format(ratios.argmax()+1))

            def find_ratio(i):
                user = ratings[ratings['userId']==i+1]
                srtd_tmp = user.timestamp.sort_values()
                srtd_tmp_unique = user.timestamp.sort_values().unique()
                split = np.percentile(srtd_tmp_unique, self.split_ratio)
                future_u = len(srtd_tmp_unique[srtd_tmp_unique >= split])
                past_u = len(srtd_tmp_unique[srtd_tmp_unique < split])
                return future_u, past_u

            min_future, min_past = find_ratio(ratios.argmin())
            max_future, max_past = find_ratio(ratios.argmax())
            logger.info('future_u, past_u for minimum ratio user: {} and {} '.format(min_future, min_past))
            logger.info('future_u, past_u for maximum ratio user: {} and {} '.format(max_future, max_past))

            logger.info('Succeed in visualizing the distribution of train/test split ratios')
            return ratios
        except:
            logger.error('Failed to visualize the distribution of train/test split ratios')
            raise

    def train_test_split(self, split_ratio):
        '''
        get train/test split
        '''
        ratings = self.get_ratings()
        self.split_ratio = split_ratio # e.g. 70

        logger.info('Trying to split train/test datasets..')
        try:
            num_user = len(ratings.userId.unique())
            num_iter = 0
            for i in xrange(num_user):
                user = ratings[ratings['userId']==i+1]
                srtd_tmp = user.timestamp.sort_values()
                srtd_tmp_unique = user.timestamp.sort_values().unique()
                split = np.percentile(srtd_tmp_unique, self.split_ratio)
                future = srtd_tmp[srtd_tmp >= split]
                past = srtd_tmp[srtd_tmp < split]
                future_df = user[user['timestamp'] >= split ].sort_values('timestamp')
                past_df = user[user['timestamp'] < split ].sort_values('timestamp')

                if future_df.shape[0] != len(future):
                    logger.error('test,{},{},user no.{}'.format( future_df.shape[0] , len(future), i+1))
                    raise

                if past_df.shape[0] != len(past):
                    logger.error('train,{},{},user no.{}'.format( past_df.shape[0] , len(past), i+1))
                    raise

                if i==0:
                    train_df = past_df
                    test_df = future_df
                else:
                    train_df = train_df.append(past_df)
                    test_df = test_df.append(future_df)

                num_iter += 1
                if num_iter % 100 == 0:
                    logger.info('split_ratio iteration: {} out of {} users'.format(num_iter, num_user))

            logger.info('Succeed in split train/test datasets')
        except:
            logger.error('Failed to split train/test datasets')
            raise
        return train_df, test_df

    def get_matrix_size(self):
        '''
        get data matrix size
        '''
        ratings = self.get_ratings()
        return self.highest_user_id, self.highest_movie_id
