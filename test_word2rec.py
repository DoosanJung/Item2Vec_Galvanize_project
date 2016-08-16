import numpy as np
import pandas as pd
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models
import split
from itertools import chain

def get_ratings_data(ratings_contents):
    '''
    Returns a tuple containing:
        - a dataframe of ratings
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    highest_user_id = ratings_contents.userId.max()
    highest_movie_id = ratings_contents.movieId.max()
    ratings_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
        # subtract 1 from id's due to match 0 indexing
        ratings_as_mat[row.userId - 1, row.movieId - 1] = row.rating
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
            movies_as_mat[row.userId - 1, row.movieId - 1] = row.movieId
        elif row.rating < down:
            movies_as_mat[row.userId - 1, row.movieId - 1] = -1 * row.movieId
    movies_array = movies_as_mat.toarray()
    #movies_DataFrame = pd.DataFrame(movies_array, columns = movies_contents.ix[:,1])
    return movies_array#, movies_DataFrame

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

def test_simple_instance(items, item_numbers, negative_items, user):
    model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
    model.fit(items)
    user_items = items[user-1]
    #negative_items = [str(-1 * int(x)) for x in unliked_list[user-1]]
    negative_items = [str(-1 * int(x)) for x in negative_items[user-1]]
    #negative_items=[]
    recommendations = model.recommend(user_items, negative_items, num_items=10)
    return recommendations

def extract_names(recommendations, movies_contents):
    recommended_list = list(zip(*recommendations)[0])
    # adjusting index by subtracting 1
    #recommended_list = [int(x)-1 for x in recommended_list]
    recommended_list = [int(x) for x in recommended_list]
    extracted = movies_contents.ix[recommended_list,:]
    print extracted
    print '\n'
    return extracted

def examine_the_results(extracted, ratings_DataFrame, user):
    idx = extracted.index-1
    examine_list = []
    for i in idx:
        r = ratings_DataFrame.ix[user-1,:][i]
        examine_list.append(r)
    print examine_list
    return examine_list

def examine_the_results2(extracted, rtmp, user):
    idx = extracted.index-1
    examine_list = []
    rt = list(chain.from_iterable(rtmp[user-1].toarray().tolist()))
    for i in idx:
        r = rt[i]
        examine_list.append(r)
    print examine_list
    return examine_list

def preprocessing():
    print 'Initialize preprocessing...'
    ##===================================================================
    ## getting data
    ##===================================================================
    # raw data
    ratings_contents = pd.read_table("data/u.data",
                                     names=["userId", "movieId", "rating",
                                            "timestamp"])
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


    # get rating matrix
    highest_user_id, highest_movie_id, ratings_contents, ratings_as_mat \
                                        = get_ratings_data(ratings_contents)


    # cPickle ratings_as_mat
    # with open('ratings_as_mat', 'w') as f:
    #     pickle.dump(ratings_as_mat, f)
    # # delete
    # del ratings_as_mat
    # loading
    #ratings_as_mat = pickle.load(open('ratings_as_mat', 'rb'))



    # movies_array, movies_DataFrame = get_movies_data(
    #                                 movies_contents, highest_user_id,
    #                                 highest_movie_id, ratings_contents,
    #                                 up = 5, down = 2 )
    movies_array = get_movies_data(movies_contents, highest_user_id,
                                    highest_movie_id, ratings_contents,
                                    up = 5, down = 2 )

    # saving movies_array.npy
    #np.save('movies_array',movies_array)
    # To load movies_array.numpy


    # make liked lists(str), unliked lists(str)
    items, item_numbers, unliked_list = makeitems(movies_array)

    # cPickle items, item_numbers, unliked_list
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

def preprocessing2(train_df):
    print "Using train_df"
    # get rating matrix
    highest_user_id, highest_movie_id, train_df, ratings_as_mat \
                                        = get_ratings_data(train_df)


    # cPickle ratings_as_mat
    # with open('ratings_as_mat', 'w') as f:
    #     pickle.dump(ratings_as_mat, f)
    # # delete
    # del ratings_as_mat
    # loading
    #ratings_as_mat = pickle.load(open('ratings_as_mat', 'rb'))



    # movies_array, movies_DataFrame = get_movies_data(
    #                                 movies_contents, highest_user_id,
    #                                 highest_movie_id, train_df,
    #                                 up = 5, down = 2 )
    movies_array = get_movies_data(movies_contents, highest_user_id,
                                    highest_movie_id, train_df,
                                    up = 5, down = 2 )

    # saving movies_array.npy
    #np.save('movies_array',movies_array)
    # To load movies_array.numpy


    # make liked lists(str), unliked lists(str)
    items, item_numbers, unliked_list = makeitems(movies_array)

    # cPickle items, item_numbers, unliked_list
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
    #ratings_DataFrame = pd.DataFrame(ratings_as_mat.toarray(), columns = movies_contents.ix[:,1])


    print 'preprocessing done'
    return items, item_numbers, unliked_list, movies_contents, ratings_as_mat#, ratings_DataFrame


def rec_eval(items, item_numbers, unliked_list, movies_contents,ratings_as_mat, ratings_DataFrame, user):
    ##===================================================================
    ## making recommendations
    ##===================================================================
    # make recommendations
    recommendations = test_simple_instance(items, item_numbers, unliked_list, user)
    print 'training done'
    print ' '

    # what are the names of the recommended movies
    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)

    ##===================================================================
    ## examine the results
    ##===================================================================
    # user's rating list
    print "User {}'s ratings on Recommended movis".format(user)
        # user1,  all of the ratings
        #ratings_DataFrame.ix[0,:]

        # user1,  movie 1 (Toy Story) rating
        #ratings_DataFrame.ix[0,:][0] == 5

        # user1, unliked_list (rating < 2)
        # ['-8', ratings_DataFrame.ix[0,:][7] == 1
        # '-21', ratings_DataFrame.ix[0,:][20] == 1
        # '-29', ratings_DataFrame.ix[0,:][28] == 1
        # '-35',ratings_DataFrame.ix[0,:][34] == 1
        #...

    examine_list = examine_the_results(extracted, ratings_DataFrame, user)
        # examine recommended_list (window = 10000)
        #          movie_id                          movie_title release_date
        # 55         56                  Pulp Fiction (1994)  01-Jan-1994
        # 152       153          Fish Called Wanda, A (1988)  01-Jan-1988
        # 432       433                      Heathers (1989)  01-Jan-1989
        # 188       189              Grand Day Out, A (1992)  01-Jan-1992
        # 184       185                        Psycho (1960)  01-Jan-1960
        # 212       213           Room with a View, A (1986)  01-Jan-1986
        # 505       506         Rebel Without a Cause (1955)  01-Jan-1955
        # 734       735                  Philadelphia (1993)  01-Jan-1993
        # 135       136  Mr. Smith Goes to Washington (1939)  01-Jan-1939
        # 46         47                       Ed Wood (1994)  01-Jan-1994
        # print ratings_DataFrame.ix[0,:][55]
        # print ratings_DataFrame.ix[0,:][152]
        # print ratings_DataFrame.ix[0,:][432]
        # print ratings_DataFrame.ix[0,:][188]
        # print ratings_DataFrame.ix[0,:][184]
        # print ratings_DataFrame.ix[0,:][212]
        # print ratings_DataFrame.ix[0,:][505]
        # print ratings_DataFrame.ix[0,:][734]
        # print ratings_DataFrame.ix[0,:][136]
        # print ratings_DataFrame.ix[0,:][46]
        # 4.0
        # 3.0
        # 0.0
        # 3.0
        # 4.0
        # 2.0
        # 0.0
        # 0.0
        # 5.0
        # 4.0
    return examine_list

def rec_eval2(items, item_numbers, unliked_list, movies_contents,ratings_as_mat, rtmp, user):
    recommendations = test_simple_instance(items, item_numbers, unliked_list, user)

    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)

    print "User {}'s ratings on Recommended movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)

    return examine_list

def iter_exam(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user):
    num_iter = 10
    examine_list_iter = []
    for i in xrange(num_iter):
        element = rec_eval(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user)
        examine_list_iter.append(element)
    print examine_list_iter
    return examine_list_iter

def iter_exam2(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,rtmp, user):
    num_iter = 10
    examine_list_iter = []
    for i in xrange(num_iter):
        element = rec_eval(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,rtmp, user)
        examine_list_iter.append(element)
    print examine_list_iter
    return examine_list_iter

if __name__=="__main__":
    # preprocessing the data
    #items, item_numbers, unliked_list, movies_contents, ratings_as_mat, ratings_DataFrame = preprocessing()
    items, item_numbers, unliked_list, movies_contents, ratings_as_mat = preprocessing2(train_df)

    rtmp = sparse.csr_matrix(ratings_as_mat)

    # recommendations and evaluations
    #examine_list = rec_eval(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user=1)
    examine_list = rec_eval2(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,rtmp, user=1)

    #
    examine_list_iter = iter_exam(items, item_numbers, unliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user=1)
    print np.mean([x for row in examine_list_iter for x in row if x > 0])
