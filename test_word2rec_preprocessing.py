import numpy as np
import pandas as pd
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models

def get_ratings_data(ratings_contents):
    '''
    Returns a tuple containing:
        - a dataframe of ratings
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    highest_user_id = ratings_contents.user.max()
    highest_movie_id = ratings_contents.movie.max()
    ratings_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
        # subtract 1 from id's due to match 0 indexing
        ratings_as_mat[row.user - 1, row.movie - 1] = row.rating
    return highest_user_id, highest_movie_id, ratings_contents, ratings_as_mat

def get_movies_data( movies_contents, \
                    highest_user_id, \
                    highest_movie_id, \
                    ratings_contents, \
                    up = 3, down = 3):
    '''
    Returns a tuple containing:
        - a dataframe of ratings
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    movies_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
        if row.rating >= up:
            movies_as_mat[row.user - 1, row.movie - 1] = row.movie
        elif row.rating < down:
            movies_as_mat[row.user - 1, row.movie - 1] = -1 * row.movie
    movies_array = movies_as_mat.toarray()
    movies_DataFrame = pd.DataFrame(movies_array, columns = movies_contents.ix[:,1])
    return movies_array, movies_DataFrame

def get_movies_data2( movies_contents, \
                    highest_user_id, \
                    highest_movie_id, \
                    ratings_contents, \
                    up = 3, down = 3):
    '''
    Returns a tuple containing:
        - a dataframe of ratings
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    movies_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
        if row.rating >= up:
            movies_as_mat[row.user - 1, row.movie - 1] = row.movie
        elif row.rating < down:
            movies_as_mat[row.user - 1, row.movie - 1] = -1 * row.movie
    return movies_as_mat
ato

def makeitems(movies_array):
    liked_list = []
    item_numbers = []
    unliked_list = []
    for i in xrange(movies_array.shape[0]):
        non_zero_list = [str(int(x)) for x in list(movies_array[i]) if x > 0]
        negative_list = [str(int(x)) for x in list(movies_array[i]) if x < 0]
        liked_list.append(non_zero_list)
        item_numbers.append(len(non_zero_list))
        unliked_list.append(negative_list)
    return liked_list, item_numbers, unliked_list


def makeitems2(movies_as_mat):
    liked_list = []
    item_numbers = []
    unliked_list = []
    for i in xrange(movies_as_mat.shape[0]):
        non_zero_list = [str(int(x)) for x in list(movies_as_mat[i].toarray()) if x > 0]
        negative_list = [str(int(x)) for x in list(movies_as_mat[i].toarray()) if x < 0]
        liked_list.append(non_zero_list)
        item_numbers.append(len(non_zero_list))
        unliked_list.append(negative_list)
    return liked_list, item_numbers, unliked_list






def preprocessing():
    print 'Initialize preprocessing...'
    ratings_contents = pd.read_table("data/u.data",
                                     names=["user", "movie", "rating",
                                            "timestamp"])

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







    # get rating matrix
    highest_user_id, highest_movie_id, ratings_contents, ratings_as_mat \
                                        = get_ratings_data(ratings_contents)


    # # cPickle ratings_as_mat
    # with open('ratings_as_mat', 'w') as f:
    #     pickle.dump(ratings_as_mat, f)
    # # delete
    # del ratings_as_mat
    # # loading
    # ratings_as_mat = pickle.load(open('ratings_as_mat', 'rb'))



    movies_array, movies_DataFrame = get_movies_data(
                                    movies_contents, highest_user_id,
                                    highest_movie_id, ratings_contents,
                                    up = 5, down = 2 )
    # saving movies_array.npy
    # np.save('movies_array',movies_array)
    # To load movies_array.numpy


    # make liked lists(str), unliked lists(str)
    items, item_numbers, unliked_list = makeitems(movies_array)

    # # cPickle items, item_numbers, unliked_list
    # with open('items', 'w') as f:
    #     pickle.dump(items, f)
    # with open('item_numbers', 'w') as f:
    #     pickle.dump(item_numbers, f)
    # with open('unliked_list', 'w') as f:
    #     pickle.dump(unliked_list, f)
    # # delete
    # del items
    # del item_numbers
    # del unliked_list
    # # loading
    # items = pickle.load(open('items', 'rb'))
    # item_numbers = pickle.load(open('item_numbers', 'rb'))
    # unliked_list = pickle.load(open('unliked_list', 'rb'))


    # save it to csv file
    # movies_DataFrame.to_csv('movies_DataFrame1.csv')
    ratings_DataFrame = pd.DataFrame(ratings_as_mat.toarray(), columns = movies_contents.ix[:,1])

    print 'preprocessing done'
    return items, item_numbers, unliked_list, movies_contents, ratings_as_mat, ratings_DataFrame




if __name__=="__main__":
    # preprocessing the data
    items, item_numbers, unliked_list, movies_contents, ratings_as_mat, ratings_DataFrame = preprocessing()
