import numpy as np
import pandas as pd
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models
import split
from itertools import chain

def get_ratings_data2(highest_user_id, highest_movie_id, ratings_contents):
    '''
    Returns a tuple containing:
        - maximum user id
        - maximum item id
        - a sparse matrix where rows correspond to users and columns correspond
        to movies. Each element is the user's rating for that movie.
    '''
    ratings_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
        # subtract 1 from id's due to match 0 indexing
        ratings_as_mat[row.userId - 1, row.movieId - 1] = row.rating
    return ratings_as_mat

def make_movies_data(highest_user_id, \
                    highest_movie_id, \
                    ratings_contents, \
                    up = 3, down = 3):
    '''
    Returns a sparse matrix.(like / dislike / not_rated as 0 )
        - liked items = positive number
        - dislied items = negative number
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
            print '<making binary matrices>',i, ' out of ', num_iters
        i += 1
    return movies_as_mat

def makeitems(movies_as_mat,up,down):
    '''
    Returns a tuple containing:
        - liked_list for all users
        - list of number of ratings per user
        - disliked_list for all users
    '''
    liked_list = []
    item_numbers = []
    disliked_list = []
    tmp = sparse.csr_matrix(movies_as_mat)
    num_iters = tmp.shape[0]
    for i in xrange(num_iters):
        non_zero_list = [str(int(x)) for x in list(chain.from_iterable(tmp[i].toarray().tolist())) if x > 0]
        negative_list = [str(int(x)) for x in list(chain.from_iterable(tmp[i].toarray().tolist())) if x < 0]
        liked_list.append(non_zero_list)
        item_numbers.append(len(non_zero_list))
        disliked_list.append(negative_list)
        if i % 10000 == 0:
            print '<making items, disliked_list>', i , ' out of ', num_iters
    return liked_list, item_numbers, disliked_list

# def test_simple_instance(items, item_numbers, negative_items, user):
#     '''
#     Returns list of tuples representing item recommendations.
#         - based on user's liked_list and disliked_list.
#         - contains cosine similarities of the recommendations.
#     '''
#     model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
#     model.fit(items)
#     user_items = items[user-1]
#     negative_items = [str(-1 * int(x)) for x in negative_items[user-1]]
#     #negative_items=[]
#     recommendations = model.recommend(user_items, negative_items, num_items=10)
#     return recommendations

def test_simple_instance_test1(test_user, items, item_numbers, negative_items, user):
    model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
    model.fit(items)
    user_items = items[user-1]
    negative_items = [str(-1 * int(x)) for x in negative_items[user-1]]
    #negative_items=[]
    final = model.recommend(test_user, user_items, negative_items, num_items=50)
    return final

def extract_names(recommendations, movies_contents):
    '''
    Returns and print the name of the itmes.
    It contains the name and the genre.
    '''
    recommended_list = list(zip(*recommendations)[0])
    # adjusting index by subtracting 1
    recommended_list = [int(x)-1 for x in recommended_list]
    extracted = movies_contents.ix[recommended_list,:]
    print extracted
    print '\n'
    return extracted

def examine_the_results2(extracted, rtmp, user):
    '''
    Returns the actual ratings of the recommend items from the user.
    Used for evaluating the performance of the recommender.
    '''
    idx = extracted.index-1
    examine_list = []
    rt = list(chain.from_iterable(rtmp[user-1].toarray().tolist()))
    for i in idx:
        r = rt[i]
        examine_list.append(r)
    print examine_list
    return examine_list

def preprocessing2(train_df):
    '''
    Not user-specific processes.
    '''
    print "Using train_df"
    ratings_as_mat = get_ratings_data2(highest_user_id, highest_movie_id, train_df)



    movies_as_mat = make_movies_data(highest_user_id,
                                    highest_movie_id, train_df,
                                    up = 5, down = 2 )

    up = 5; down = 2
    # make liked lists(str), unliked lists(str)
    items, item_numbers, disliked_list = makeitems(movies_as_mat, up, down)

    print 'preprocessing done'
    return items, item_numbers, disliked_list, movies_contents, ratings_as_mat#, ratings_DataFrame


def rec_eval2(items, item_numbers, disliked_list, movies_contents,ratings_as_mat, rtmp, user):
    '''
    User-specific processes.
    '''
    recommendations = test_simple_instance(items, item_numbers, disliked_list, user)

    print "Recommended movies"
    extracted = extract_names(recommendations, movies_contents)

    print "User {}'s ratings on Recommended movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)

    return examine_list

def iter_exam2(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,rtmp, user):
    '''
    Recommend and evaluate iteratively.
    '''
    num_iters = 10
    examine_list_iter = []
    for i in xrange(num_iters):
        element = rec_eval(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,rtmp, user)
        examine_list_iter.append(element)
    print examine_list_iter
    return examine_list_iter

if __name__=="__main__":
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
    train_df, test_df = split.train_test_split(ratings_contents)
    # preprocessing the data
    #items, item_numbers, disliked_list, movies_contents, ratings_as_mat, ratings_DataFrame = preprocessing()
    items, item_numbers, disliked_list, movies_contents, ratings_as_mat = preprocessing2(train_df)

    rtmp = sparse.csr_matrix(ratings_as_mat)

    # recommendations and evaluations
    #examine_list = rec_eval(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user=1)
    #examine_list = rec_eval2(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,rtmp, user=1)

    #==>> to test1

    # user = 1
    # recommendations = test_simple_instance(items, item_numbers, disliked_list, user)
    # print "Recommended movies"
    # extracted = movies_contents.ix[recommended_list,:]
    # print "User {}'s ratings on Recommended movis".format(user)
    # examine_list = examine_the_results2(extracted, rtmp, user)

    #
    # examine_list_iter = iter_exam(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user=1)
    # print np.mean([x for row in examine_list_iter for x in row if x > 0])
    #
    # # how many movies do users rated?
    # num_ratings_per_users = ratings_DataFrame.sum(axis=1).sort_values(axis=0, ascending=False)




## =============================================================
## original
## =============================================================
    # user 1 recommendations
    # Recommended movies
    #                                     movie_title release_date
    # movieId
    # 207                   Cyrano de Bergerac (1990)  01-Jan-1990
    # 168      Monty Python and the Holy Grail (1974)  01-Jan-1974
    # 432                             Fantasia (1940)  01-Jan-1940
    # 132                    Wizard of Oz, The (1939)  01-Jan-1939
    # 82                         Jurassic Park (1993)  01-Jan-1993
    # 131               Breakfast at Tiffany's (1961)  01-Jan-1961
    # 184                     Army of Darkness (1993)  01-Jan-1993
    # 1038                          Switchback (1997)  01-Jan-1997
    # 202                        Groundhog Day (1993)  01-Jan-1993
    # 192                          Raging Bull (1980)  01-Jan-1980

    recommended_list = list(zip(*recommendations)[0])
    # In [95]: recommendations
    # Out[95]:
    # [('208', 0.9999507665634155),
    #  ('651', 0.9999498128890991),
    #  ('433', 0.9999495148658752),
    #  ('136', 0.9999482035636902),
    #  ('185', 0.9999475479125977),
    #  ('169', 0.9999474883079529),
    #  ('238', 0.9999473094940186),
    #  ('83', 0.9999469518661499),
    #  ('132', 0.9999469518661499),
    #  ('28', 0.9999468326568604)]
    recommended_list = [int(x)-1 for x in recommended_list]
    # [207, 650, 432, 135, 184, 168, 237, 82, 131, 27]
    # print 'train_df.shape',train_df.shape
    # print 'test_df.shape',test_df.shape
    # print 'train_df.movieId.unique()',train_df.movieId.unique().size
    # print 'test_df.movieId.unique()',test_df.movieId.unique().size
    user=1
    train_user = train_df[train_df['userId'] == user] # user already rated. used for training
    test_user = test_df[test_df['userId'] == user] # user already rated. used for validation
    print 'train_user.shape',train_user.shape
    print 'test_user.shape',test_user.shape
    print 'train_user.movieId.unique()',train_user.movieId.unique().size
    print 'test_user.movieId.unique()',test_user.movieId.unique().size
    final=[]
    for movie in recommended_list:
        if movie in train_user.movieId.unique():
            print "movie ",movie,' is in train_user'
        if movie in test_user.movieId.unique():
            final.append(movie)
            print "movie ",movie,' is in test_user'
    print "Final movies"
    extracted = extract_names(final, movies_contents)
    print "User {}'s ratings on Final movis".format(user)
    examine_list = examine_the_results2(extracted, rtmp, user)

    # movie  207  is in train_user
    # movie  135  is in train_user
    # movie  184  is in train_user
    # movie  168  is in train_user
    # movie  237  is in train_user
    # movie  82  is in test_user
    # movie  131  is in test_user
    # movie  27  is in train_user

    # Don't recommend the movies user already rated
    # BAD




## =============================================================
## test1 (models.py)
## =============================================================

    # recommendations and evaluations
    #examine_list = rec_eval(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,ratings_DataFrame, user=1)
    #examine_list = rec_eval2(items, item_numbers, disliked_list, movies_contents,ratings_as_mat,rtmp, user=1)

    user = 1
    train_user = train_df[train_df['userId'] == user] # user already rated. used for training
    test_user = test_df[test_df['userId'] == user] # user already rated. used for validation
    #items, item_numbers, disliked_list, movies_contents, ratings_as_mat = preprocessing2(train_df)
    #rtmp = sparse.csr_matrix(ratings_as_mat)

    negative_items = disliked_list
    final = test_simple_instance_test1(test_user, items, item_numbers, disliked_list, user)
    print "Recommended movies"
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
    final_examine_list = examine_the_results2(final_extracted, rtmp, user)

    print len(final_examine_list)
    print len([x for x in final_examine_list if x >= 4])









# Do not user num_ratings_per_users
# num_ratings_per_users = pd.DataFrame(ratings_as_mat.todense(), columns = movies_contents.ix[:,1])
# num_ratings_per_users = num_ratings_per_users[num_ratings_per_users!=0].count(axis=1).sort_values(axis=0, ascending=False)
# 404    737
# 654    685
# 12     636
# 449    540
# 275    518

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

count_ratings_per_users = count_num_ratings_per_users(ratings_as_mat)
count_ratings_per_users = pd.DataFrame(count_ratings_per_users.items(), columns = ['userId','num_ratings'])
count_ratings_per_users = count_per_users.sort_values(by = 'num_ratings', axis =0, ascending = False)
#      userId  num_ratings
# 404     405          737
# 654     655          685
# 12       13          636
# 449     450          540
# 275     276          518


def recall_at_M(test_user, final_examine_list, num_items):
    '''
                  Number of items user i liked among the top M items (test set)
    recall @ M =  --------------------------------------------------------------
                         Total number of items user i likes (test set) = M
    '''
    # first define "likes"
    # likes = ratings over 4

    numerator = len([x for x in final_examine_list if x >= 4])
    denominator = len(final_examine_list)
    denominator =

    return numerator/denominator










'''
# To inspect
def pipeline(train_df, test_df, user):
    train_user = train_df[train_df['userId'] == user]
    test_user = test_df[test_df['userId'] == user]
    count =0
    for movie in train_user.movieId:
        if movie in test_user.movieId:
            count += 1
    return count

def pipeline2(train_df, test_df, user):
    train_user = train_df[train_df['userId'] == user]
    test_user = test_df[test_df['userId'] == user]
    count =0
    for movie in train_user.movieId.unique():
        if movie in test_user.movieId.unique():
            count += 1
    return count

result = []
num_user = len(ratings_contents.userId.unique())
for i in xrange(num_user):
    result.append(pipeline(train_df,test_df, i))
print sum(result)

result2 = []
num_user = len(ratings_contents.userId.unique())
for i in xrange(num_user):
    result2.append(pipeline2(train_df,test_df, i))
print sum(result2)
'''
