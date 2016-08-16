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
    # old
    negative_items = disliked_list
    recommendations = test_simple_instance(items, item_numbers, negative_items, user)
    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)
    print "User {}'s ratings on Recommended movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)

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


# user 654(userId 654) All recommendations
# [('186', 0.999988317489624),
#  ('208', 0.9999874234199524),
#  ('527', 0.9999861121177673),
#  ('153', 0.9999856948852539),
#  ('125', 0.9999853372573853),
#  ('588', 0.9999845027923584),
#  ('204', 0.9999845027923584),
#  ('485', 0.9999840259552002),
#  ('216', 0.9999839067459106),
#  ('172', 0.9999837875366211),
#  ('419', 0.9999837875366211),
#  ('132', 0.9999836683273315),
#  ('451', 0.9999836683273315),
#  ('202', 0.9999836087226868),
#  ('11', 0.9999832510948181),
#  ('182', 0.9999831914901733),
#  ('71', 0.9999830722808838),
#  ('234', 0.9999829530715942),
#  ('83', 0.9999829530715942),
#  ('237', 0.9999825954437256),
#  ('228', 0.999982476234436),
#  ('82', 0.9999821782112122),
#  ('223', 0.9999821186065674),
#  ('385', 0.9999821186065674),
#  ('96', 0.9999818801879883),
#  ('501', 0.9999818801879883),
#  ('95', 0.999981701374054),
#  ('1', 0.9999816417694092),
#  ('196', 0.9999814629554749),
#  ('684', 0.9999814033508301),
#  ('288', 0.9999814033508301),
#  ('200', 0.9999813437461853),
#  ('199', 0.9999813437461853),
#  ('28', 0.9999812841415405),
#  ('144', 0.9999812841415405),
#  ('121', 0.999981164932251),
#  ('423', 0.9999811053276062),
#  ('484', 0.9999809265136719),
#  ('655', 0.9999808073043823),
#  ('663', 0.9999805688858032),
#  ('174', 0.9999805688858032),
#  ('568', 0.9999803304672241),
#  ('432', 0.9999803304672241),
#  ('69', 0.9999802112579346),
#  ('257', 0.9999802112579346),
#  ('183', 0.9999801516532898),
#  ('179', 0.9999799728393555),
#  ('735', 0.9999799728393555),
#  ('168', 0.9999799728393555),
#  ('181', 0.9999799728393555)]

# user 654(userId 654) Final recommendations
#[588, 71, 196, 144, 98, 83, 82, 69, 204, 568, 215, 174, 317, 66, 269, 735]
# User 654's ratings on Final movies
# [4, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 5, 4, 4, 4, 4]


# later...
# def iter_exam(items, item_numbers, disliked_list, movies_contents, rtmp, user):
#     num_iter = 10
#     examine_list_iter = []
#     for i in xrange(num_iter):
#         print 'iteration number: ', i+1
#         element = rec_eval(items, item_numbers, disliked_list, movies_contents, rtmp, user)
#         examine_list_iter.append(element)
#     print examine_list_iter
#     return examine_list_iter

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
    user = 181

    # how many movies do users rated?
    # count_ratings_per_users = count_num_ratings_per_users(ratings_as_mat)
    # count_ratings_per_users = pd.DataFrame(count_ratings_per_users.items(), columns = ['userId','num_ratings'])
    # count_ratings_per_users = count_ratings_per_users.sort_values(by = 'num_ratings', axis =0, ascending = False)

    # In [145]: count_ratings_per_users
    # Out[145]:
    #      userId  num_ratings
    # 12       13          526
    # 404     405          520
    # 654     655          443
    # 449     450          423
    # 275     276          400
    # 302     303          385
    # 233     234          369
    # 536     537          349
    # 6         7          328
    # 845     846          321
    # 392     393          318
    # 307     308          314
    # 278     279          308
    # 180     181          308
    # 93       94          306
    # 91       92          296
    # 428     429          295
    # 416     417          292
    # 879     880          288
    # 757     758          287
    # 221     222          286
    # 434     435          285
    # 292     293          280
    # 200     201          279
    # 377     378          276
    # 560     561          275
    # 129     130          273
    # 681     682          273
    # 591     592          271
    # 58       59          270

    '''
    User 13's ratings on Final movies
    [5, 4, 4, 4, 4, 5, 2, 4, 2, 3, 3, 4, 4, 5]

    User 405's ratings on Final movies
    [3, 5, 4, 5, 3, 4, 3, 4, 5, 3, 4, 5, 5, 3, 5, 5, 5, 3]
    User 450's ratings on Final movies
    [4, 5, 3, 5, 3, 4, 5, 5, 3, 3, 5, 3, 5, 4, 3, 5, 4, 4, 5, 3, 4, 4]

    User 276's ratings on Final movies
    [5, 4, 5, 5, 4, 4, 4, 5, 4, 4, 4, 5]
    User 276's ratings on Final movies
    [5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5, 4]

    User 303's ratings on Final movies
    [4]
    User 303's ratings on Final movies
    [4]

    User 234's ratings on Final movies
    [3, 3, 4]
    User 234's ratings on Final movies
    [3, 4, 2, 3]

    User 537's ratings on Final movies
    [3, 3, 1, 3, 3, 3, 3, 2, 2]
    User 537's ratings on Final movies
    [2, 1, 3, 3, 2, 3]

    User 7's ratings on Final movies
    [5, 4, 5, 5, 1, 3, 5, 5, 5, 5, 5, 5, 4]
    User 7's ratings on Final movies
    [5, 5, 5, 5, 3, 5, 1, 5, 4, 5, 4, 5, 4, 5]

    User 846's ratings on Final movies
    []

    User 393's ratings on Final movies
    [3, 3, 3, 4]

    User 308's ratings on Final movies
    [4, 3, 4, 3, 3, 4, 4]

    User 279's ratings on Final movies
    [3, 3, 3, 1, 4, 5, 4, 3, 3, 4, 1, 5, 4, 3]

    User 181's ratings on Final movies
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2]

    User 94's ratings on Final movies
    [5, 5, 4, 5, 4, 3, 5]

    User 92's ratings on Final movies
    [4, 3, 3, 4]

    User 429's ratings on Final movies
    [5, 4, 5, 5, 5, 5, 4, 4]

    User 417's ratings on Final movies
    [4, 3]
    '''
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
