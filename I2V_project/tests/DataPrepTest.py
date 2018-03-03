#!/usr/bin/env python
'''
'''

import unittest
import pandas as pd
import logging
from logging import config
from I2V_project.conf.I2VConfig import I2VConfig
from I2V_project.src.DataPrep import DataPrep

config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()

class DataPrepTestCase(unittest.TestCase):
    '''
    Data preparation uniittest
    '''
    def test_data_prep(self):
        '''
        test to fetch ratings, items and to split train/test data
        '''
        result = False

        dp = DataPrep()

        split_ratio = 0.7

        try:
            logger.info("Trying to get ratings")
            ratings = dp.get_ratings()

            logger.info("Trying to get items")
            items = dp.get_items()

            logger.info("Trying to visulaize the distribution of train/test split ratios")
            ratios = dp.show_ratio_dist(split_ratio)

            logger.info("Trying to split train, test data")
            train_df, test_df = dp.train_test_split(split_ratio)

            logger.info("Trying to split train, test data")
            dp.num_user_id, dp.num_movie_id = dp.get_matrix_size()

            result = True
        except:
            logger.error("Failed test - DataPrep")
            raise

        self.assertEqual(True,result)

if __name__=="__main__":
    unittest.main()
