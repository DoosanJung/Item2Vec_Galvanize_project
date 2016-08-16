##===============================================================
## To create the "per user" training, validation dataset
## ==============================================================

import pandas as pd
from scipy import sparse

import sys
sys.path.append('code')

import models

if __name__=="__main__":
    # raw data
    ratings_contents = pd.read_table("data/u.data",
                                     names=["user", "movie", "rating",
                                            "timestamp"])
    # movie_dataset
    movies_contents = pd.read_table("data/u.item",
                                    sep = '|',
                                    header = None,
                                    names = [
            'movie_id' , 'movie_title' , 'release_date' , 'video_release_date',
            'IMDb_URL' , 'unknown' , 'Action' , 'Adventure' , 'Animation' ,
            'Children' , 'Comedy' , 'Crime' , 'Documentary' , 'Drama' , 'Fantasy',
            'Film_Noir' , 'Horror' , 'Musical' , 'Mystery' , 'Romance' , 'Sci_Fi',
            'Thriller' , 'War' , 'Western'
                                            ])
