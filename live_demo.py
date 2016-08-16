import numpy as np
import pandas as pd
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models
import split
from itertools import chain

def test_simple_instance(items, item_numbers, negative_items, user):
    model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
    model.fit(items)
    user_items = items[user-1]
    #negative_items = [str(-1 * int(x)) for x in unliked_list[user-1]]
    negative_items = [str(-1 * int(x)) for x in negative_items[user-1]]
    #negative_items=[]
    recommendations = model.recommend(user_items, negative_items, num_items=50)
    return recommendations

def test_simple_instance_test1(test_user, items, item_numbers, negative_items, user):
    '''
    Returns list of tuples representing item recommendations.
        - based on user's liked_list and disliked_list
        - contains cosine similarities of the recommendations
    '''
    model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
    model.fit(items)
    user_items = items[user-1]
    negative_items = [str(-1 * int(x)) for x in negative_items[user-1]]
    final = model.recommend2(test_user, user_items, negative_items, num_items=100)
    return final # movieId

def extract_names(recommendations, movies_contents):
    '''
    Returns and print the name of the itmes.
    It contains the name and the genre.
    '''
    recommended_list = list(zip(*recommendations)[0]) # movieId
    # adjusting index by subtracting 1
    recommended_list = [int(x) for x in recommended_list]
    extracted = movies_contents.ix[recommended_list,:]
    print extracted
    print '\n'
    return extracted

def examine_the_results2(final_extracted, rtmp, user):
    '''
    Returns the actual ratings of the recommend items from the user.
    Used for evaluating the performance of the recommender.
    '''
    idx = final_extracted.index
    examine_list = []
    rt = list(chain.from_iterable(rtmp[user-1].toarray().tolist()))
    for i in idx:
        r = rt[i-1]
        examine_list.append(r)
    print examine_list
    return examine_list

def examine_the_results3(final_extracted, test_user, user):
    '''
    Returns the actual ratings of the recommend items from the user.
    Used for evaluating the performance of the recommender.
    '''
    idx = final_extracted.index
    examine_list = []
    for i in idx:
        r = int( test_user[test_user['movieId'] == i].rating )
        examine_list.append(r)
    print examine_list
    return examine_list

def rec_eval(items, item_numbers, disliked_list, movies_contents, rtmp, user):
    '''
    User-specific processes.
    '''
    recommendations = test_simple_instance_test1(test_user, items, item_numbers, disliked_list, user)
    print recommendations
    # what are the names of the recommended movies
    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)

    print "User {}'s ratings on Recommended movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)
    return examine_list


def testing(train_user, test_user, items, item_numbers, disliked_list, rtmp, user):
    # new
    final = test_simple_instance_test1(test_user, items, item_numbers, disliked_list, user)
    print final
    print "final"
    #recommended_list = list(zip(*recommendations)[0])
    #recommended_list = [int(x)-1 for x in recommended_list]
    # final_extracted = movies_contents.ix[final,:]
    # print "User {}'s ratings on Recommended movis".format(user)
    # examine_list = examine_the_results2(final_extracted, rtmp, user)

    print 'train_user.shape',train_user.shape
    print 'test_user.shape',test_user.shape
    print 'train_user.movieId.unique()',train_user.movieId.unique().size
    print 'test_user.movieId.unique()',test_user.movieId.unique().size

    # final=[]
    # for movie in recommended_list:
    #     if movie in train_user.movieId.unique():
    #         print "movie ",movie,' is in train_user'
    #     if movie in test_user.movieId.unique():
    #         final.append(movie)
    #         print "movie ",movie,' is in test_user'
    print "Final movies"
    final_extracted = movies_contents.ix[final,:]
    print "User {}'s ratings on Final movies".format(user)
    final_examine_list = examine_the_results3(final_extracted, test_user, user)
    print final_examine_list


def count_num_ratings_per_users(ratings_as_mat):
    '''
    To identify the number of ratings per users
    '''
    count_per_users = {}
    tmp = sparse.csr_matrix(ratings_as_mat)
    num_users = tmp.shape[0]
    for i in xrange(num_users):
        ratings_list = [int(x) for x in list(chain.from_iterable(tmp[i].toarray().tolist())) if x > 0]
        count_per_users[i+1] = len(ratings_list)
        if i % 100 == 0:
            print '<counting number of ratings for user>', i , ' out of ', num_users
    return count_per_users

def recall_at_M(test_user, final_examine_list, num_items):
    '''
                  Number of items user i liked among the top M items (test set)
    recall @ M =  --------------------------------------------------------------
                         Total number of items user i likes (test set)
    '''
    # first define "likes"
    # likes = ratings over 4
    numerator = len([x for x in final_examine_list if x >=4])
    denominator = len(final_examine_list) # M
    return float(numerator) / denominator





if __name__=="__main__":
    up=5; down=2


    # preprocessing the data
    # ratings_as_mat = pickle.load(open('data/ratings_as_mat_train.pkl', 'rb'))
    # movies_as_mat = pickle.load(open('data/movies_as_mat_train_.pkl', 'rb'))
    # movies_contents = pd.read_csv("data/movies.csv")
    # movies_contents = movies_contents.set_index('movieId')
    train_df = pickle.load(open('data/train_df.pkl', 'rb'))
    test_df = pickle.load(open('data/test_df.pkl', 'rb'))

    train_user = train_df[train_df['userId'] == user] # user already rated. used for training
    test_user = test_df[test_df['userId'] == user] # user already rated. used for validation

    # items, item_numbers, disliked_list from train_df
    items = pickle.load(open('data/items_train_{}.pkl'.format((up,down)), 'rb'))
    item_numbers = pickle.load(open('data/item_numbers_train_{}.pkl'.format((up,down)), 'rb'))
    disliked_list = pickle.load(open('data/disliked_list_train_{}.pkl'.format((up,down)), 'rb'))
    rtmp = sparse.csr_matrix(ratings_as_mat)

    # examine_list = rec_eval(items, item_numbers, disliked_list, movies_contents, rtmp, user)
    #testing(train_df, test_df, items, item_numbers, disliked_list, rtmp, user)

    # copy and paste... of the function testing
    negative_items = disliked_list
    recommendations = test_simple_instance(items, item_numbers, negative_items, user)
    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)

    print "User {}'s ratings on Recommended movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)

    final = test_simple_instance_test1(test_user, items, item_numbers, disliked_list, user)
    print final
    print "final"
    #recommended_list = list(zip(*recommendations)[0])
    #recommended_list = [int(x)-1 for x in recommended_list]
    # final_extracted = movies_contents.ix[final,:]
    # print "User {}'s ratings on Recommended movis".format(user)
    # examine_list = examine_the_results2(final_extracted, rtmp, user)

    print 'train_user.shape',train_user.shape
    print 'test_user.shape',test_user.shape
    print 'train_user.movieId.unique()',train_user.movieId.unique().size
    print 'test_user.movieId.unique()',test_user.movieId.unique().size

    # final=[]
    # for movie in recommended_list:
    #     if movie in train_user.movieId.unique():
    #         print "movie ",movie,' is in train_user'
    #     if movie in test_user.movieId.unique():
    #         final.append(movie)
    #         print "movie ",movie,' is in test_user'
    print "Final movies"
    final_extracted = movies_contents.ix[final,:]
    print "User {}'s ratings on Final movies".format(user)
    final_examine_list = examine_the_results3(final_extracted, test_user, user)





    # later...
    #examine_list_iter = iter_exam(items, item_numbers, disliked_list, movies_contents, ratings_as_mat, user=654)
    #examine_list_iter = iter_exam(items, item_numbers, disliked_list, movies_contents, rtmp, user=654)
    #or row in examine_list_iter for x in row if x > 0])
