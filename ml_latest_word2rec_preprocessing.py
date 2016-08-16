import numpy as np
import pandas as pd
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models
import split
from itertools import chain

def get_ratings_data2(highest_user_id, highest_movie_id, ratings_contents): # train_df
    '''
    Returns a tuple containing:
        - maximum user id
        - maximum user id
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    ratings_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    num_iters = ratings_contents.shape[0]
    i = 0
    for _, row in ratings_contents.iterrows():
        # subtract 1 from id's due to match 0 indexing
        ratings_as_mat[row.userId - 1, row.movieId - 1] = row.rating
        if i % 10000 == 0:
            print '<making ratings matrics> ',i , ' Out of ' , num_iters
        i+=1

    #saving
    with open('data/ratings_as_mat_train.pkl','w') as f:
        pickle.dump(ratings_as_mat,f)
    # loading
    # ratings_as_mat = pickle.load(open('data/ratings_as_mat_train.pkl', 'rb'))

    return ratings_as_mat

def make_movies_data(highest_user_id, \
                    highest_movie_id, \
                    ratings_contents, \
                    up, down):
                    # train_df
    '''
    Returns a tuple containing:
        - liked items = positive number
        - disliked items = negative number
        - not rated = 0
    '''
    movies_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    num_iters = ratings_contents.shape[0]
    i = 0
    for _, row in ratings_contents.iterrows():
        if row.rating >= up:
            movies_as_mat[row.userId - 1, row.movieId - 1] = row.movieId
        elif row.rating < down:
            movies_as_mat[row.userId - 1, row.movieId - 1] = -1 * row.movieId
        if i % 10000 == 0:
            print '<making binary matrics> ',i , ' Out of ' , num_iters
        i+=1

    # saving
    with open('data/movies_as_mat_train_{}.pkl'.format((up,down)),'w') as f:
        pickle.dump(movies_as_mat,f)
    # loading
    # movies_as_mat = pickle.load(open('data/movies_as_mat.pkl', 'rb'))
    return movies_as_mat

def makeitems2(movies_as_mat, up, down):
    '''
    Returns a tuple containing:
        - items for all users
        - list of number of ratings per user
        - disliked_list for all users
    In training set.
    '''
    items = []
    item_numbers = []
    disliked_list = []
    tmp = sparse.csr_matrix(movies_as_mat)
    num_iters = tmp.shape[0]
    for i in xrange(num_iters):
        non_zero_list = [str(int(x)) for x in list(chain.from_iterable(tmp[i].toarray().tolist())) if x > 0]
        negative_list = [str(int(x)) for x in list(chain.from_iterable(tmp[i].toarray().tolist())) if x < 0]
        items.append(non_zero_list)
        item_numbers.append(len(non_zero_list))
        disliked_list.append(negative_list)
        if i % 10000 == 0:
            print '<making items,disliked_list> ',i , ' Out of ' , num_iters
    # saving
    with open('data/items_train_{}.pkl'.format((up,down)),'w') as f:
        pickle.dump(items, f)
    with open('data/item_numbers_train_{}.pkl'.format((up,down)),'w') as f:
        pickle.dump(item_numbers, f)
    with open('data/disliked_list_train_{}.pkl'.format((up,down)),'w') as f:
        pickle.dump(disliked_list, f)
    #
    # # loading
    # items = pickle.load(open('data/items_{}.pkl'.format((up,down)), 'rb'))
    # item_numbers = pickle.load(open('data/item_numbers_{}.pkl'.format((up,down)), 'rb'))
    # disliked_list = pickle.load(open('data/disliked_list_{}.pkl'.format((up,down)), 'rb'))

    return items, item_numbers, disliked_list


if __name__=="__main__":
    '''
    Not user-specific processes.
    '''
    # get rating matrix
    ratings_contents = pd.read_table("data/u.data",
                                     names=["userId", "movieId", "rating",
                                            "timestamp"])
    highest_user_id = ratings_contents.userId.max()
    highest_movie_id = ratings_contents.movieId.max()

    # movie_dataset
    movies_contents = pd.read_table("data/u.item",
                                    sep = '|',
                                    header = None,
                                    names = [
            'movieId' , 'movie_title' , 'release_date' , 'video_release_date',
            'IMDb_URL' , 'unknown' , 'Action' , 'Adventure' , 'Animation' ,
            'Children' , 'Comedy' , 'Crime' , 'Documentary' , 'Drama' , 'Fantasy',
            'Film_Noir' , 'Horror' , 'Musical' , 'Mystery' , 'Romance' , 'Sci_Fi',
            'Thriller' , 'War' , 'Western'
                                            ])
    movies_contents = movies_contents.ix[:,[0,1,2]]
    movies_contents= movies_contents.set_index('movieId')
    #train_df, test_df = split.train_test_split(ratings_contents)
    train_df = pickle.load(open('data/train_df.pkl', 'rb'))
    test_df = pickle.load(open('data/test_df.pkl', 'rb'))

    ratings_as_mat = get_ratings_data2(highest_user_id, highest_movie_id, train_df)
    #ratings_as_mat = pickle.load(open('data/ratings_as_mat_train.pkl', 'rb'))
    # In [14]: ratings_as_mat.shape
    # Out[14]: (247753, 151695)
    # In [24]: highest_user_id
    # Out[24]: 247753
    # In [25]: highest_movie_id
    # Out[25]: 151711


    movies_as_mat = make_movies_data(highest_user_id,
                                    highest_movie_id, train_df,
                                    up = 5, down = 2)
    #movies_as_mat = pickle.load(open('data/movies_as_mat_train_{}.pkl'.format((up,down)), 'rb')) # up=5, down=2


    up=5; down=2
    items, item_numbers, disliked_list = makeitems2(movies_as_mat,up,down)
    # loading
    # items = pickle.load(open('data/items_train_{}.pkl'.format((up,down)), 'rb'))
    # item_numbers = pickle.load(open('data/item_numbers_train_{}.pkl'.format((up,down)), 'rb'))
    # disliked_list = pickle.load(open('data/disliked_list_train_{}.pkl'.format((up,down)), 'rb'))

    print 'preprocessing done'



'''
    ##===================================================================
    ## save the ratings_as_mat (sparse matrix)
    ##===================================================================
    io.mmwrite('data/ratings_as_mat.mtx',ratings_as_mat)
    # to save memory
    del ratings_as_mat
    # will arise error
    ratings_as_mat
    # to load ratings_as_mat.mtx
    ratings_as_mat = io.mmread('data/ratings_as_mat.mtx') => Memory issue !!!
'''
'''
    ##===================================================================
    ## save the movies_as_mat (sparse matrix)
    ##===================================================================
    io.mmwrite('data/movies_as_mat.mtx',movies_as_mat)
    # to save memory
    del movies_as_mat
    # will arise error
    movies_as_mat
    # to load movies_as_mat.mtx
    movies_as_mat = io.mmread('data/movies_as_mat.mtx') => Memory issue !!!!!
'''
