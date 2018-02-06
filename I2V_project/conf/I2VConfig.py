#!/usr/bin/env python
'''

'''

class I2VConfig(object):
    '''
        I2V configuration class
    '''

    COLUMNS = {
        # rating Matrix
        'ratings_columns' : ["userId", \
                            "movieId", \
                            "rating", \
                            "timestamp"
                            ],

        'movies_columns' : [ 'movieId', \
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
