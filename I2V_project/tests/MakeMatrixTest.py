#!/usr/bin/env python
'''
'''

import unittest
import pandas as pd
import logging
from logging import config
from I2V_project.conf.I2VConfig import I2VConfig
from I2V_project.src.DataPrep import DataPrep
from I2V_project.src.MakeMatrix import MakeMatrix

config.fileConfig("I2V_project/conf/I2V.cfg")
logger = logging.getLogger()

class MakeMatrixTestCase(unittest.TestCase):
    '''
    make ratings matrix, item matrix uniittest
    '''
    def test_make_matrix(self):
        '''
        test to fetch ratings, items and to split train/test data
        '''
        result = False

        dp = DataPrep()
        split_ratio = 0.7
        train_df, test_df = dp.train_test_split(split_ratio)
        dp.num_user_id, dp.num_movie_id = dp.get_matrix_size()

        up = 6
        down = 1
        mm = MakeMatrix(n_rows=dp.num_user_id, \
                        n_cols=dp.num_movie_id, \
                        df=train_df)

        try:
            logger.info("Trying to get ratings matrix")
            rating_matrix = mm.get_rating_matrix()

            logger.info("Trying to get item matrix")
            item_matrix = mm.get_item_matrix(up=up, down=down)

            logger.info("Trying to liked item, disliked item")
            liked_items, liked_item_numbers, disliked_list = mm.get_liked_disliked_items(up=up, down=down)

            result = True
        except:
            logger.error("Failed test - MakeMatrix")
            raise

        self.assertEqual(True,result)

if __name__=="__main__":
    unittest.main()
