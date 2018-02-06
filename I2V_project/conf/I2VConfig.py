#!/usr/bin/env python
'''

'''
import os

class I2VConfig(object):
    '''
    I2V configuration class
    '''
    HOME_PATH = os.path.expanduser('~/projects/I2V_project')

    FILE_PATH = {
        'test' : {
                    "ratings_testdata" : "/I2V_project/data/u.data",
                    "items_testdata"  : "/I2V_project/data/u.item",
        },
        'dev' : {
                    "ratings"          : "/I2V_project/data/ratings.csv",
                    "items"           : "/I2V_project/data/movies.csv"
        }
    }

    COLUMNS = {
        # rating Matrix
        'ratings_columns' : ["userId", \
                            "movieId", \
                            "rating", \
                            "timestamp"
                            ],

        'items_columns' : [ 'movieId', \
                            'movie_title', \
                            'release_date', \
                            'video_release_date', \
                            'IMDb_URL', \
                            'unknown', \
                            'Action', \
                            'Adventure', \
                            'Animation', \
                            'Children', \
                            'Comedy', \
                            'Crime', \
                            'Documentary', \
                            'Drama', \
                            'Fantasy', \
                            'Film_Noir', \
                            'Horror', \
                            'Musical', \
                            'Mystery', \
                            'Romance', \
                            'Sci_Fi', \
                            'Thriller', \
                            'War', \
                            'Western'
                            ]
    }

    PLOT = True

    @staticmethod
    def get_config():
        '''
            get configuration test or dev
        '''
        return {
            'HOME_PATH' : I2VConfig.HOME_PATH,
            'FILE_PATH' : I2VConfig.FILE_PATH['test'],
            'COLUMNS'   :  I2VConfig.COLUMNS
        }
