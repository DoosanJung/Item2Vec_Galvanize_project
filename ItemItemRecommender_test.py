import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from time import time
from scipy import sparse, io
import cPickle as pickle
import sys
sys.path.append('code')
import models
import split
from itertools import chain

class ItemItemRecommender(object):
    def __init__(self,neighborhood_size):
        '''
        Initialize the parameters of the model.
        '''
        self.neighborhood_size = neighborhood_size

    def fit(self,ratings_as_mat):
        '''
        Implement the model and fit it to the data passed as an argument.

        Store objects for describing model fit as class attributes.
        '''
        self.ratings_as_mat = ratings_as_mat
        self.n_users = ratings_as_mat.shape[0]
        self.n_items = ratings_as_mat.shape[1]
        self.item_sim_mat = cosine_similarity(self.ratings_as_mat.T)
        self._set_neighborhoods()

    def _set_neighborhoods(self):
        '''
        Get the items most similar to each other item.

        Should set a class attribute with a matrix that is has
        number of rows equal to number of items and number of
        columns equal to neighborhood size. Entries of this matrix
        will be indexes of other items.

        You will call this in your fit method.
        '''
        least_to_most_sim_indexes = np.argsort(self.item_sim_mat, 1)
        self.neighborhood = least_to_most_sim_indexes[:, -self.neighborhood_size:]

    def pred_one_user(self, user_id, report_run_time = False):
        '''
        Accept user id as arg. Return the predictions for a single user.

        Optional argument to specify whether or not timing should be provided
        on this operation.
        '''
        start_time = time()
        items_rated_by_this_user = self.ratings_as_mat[user_id].nonzero()[1]
        # Just initializing so we have somewhere to put rating preds
        out = np.zeros(self.n_items)
        for item_to_rate in range(self.n_items):
            relevant_items = np.intersect1d(self.neighborhood[item_to_rate],
                                            items_rated_by_this_user,
                                            assume_unique=True)
                                        # assume_unique speeds up intersection op
            out[item_to_rate] = self.ratings_as_mat[user_id, relevant_items] * \
                self.item_sim_mat[item_to_rate, relevant_items] / \
                self.item_sim_mat[item_to_rate, relevant_items].sum()
        return np.nan_to_num(out)

    def pred_all_users(self, report_run_time = False):
        '''
        Repeated calls of pred_one_user, are combined into a single matrix.
        Return value is matrix of users (rows) items (columns) and predicted
        ratings (values).

        Optional argument to specify whether or not timing should be provided
        on this operation.
        '''
        start_time = time()
        all_ratings = [self.pred_one_user(user_id) for user_id in range(self.n_users)]
        if report_run_time:
            print("Execution time: %f seconds" % (time()-start_time))
        return np.array(all_ratings)

    def top_n_recs(self, user_id, n):
        '''
        Take user_id argument and number argument.

        Return that number of items with the highest predicted ratings, after
        removing items that user has already rated.
        '''
        pred_ratings = self.pred_one_user(user_id)
        item_index_sorted_by_pred_rating = list(np.argsort(pred_ratings))
        items_rated_by_this_user = self.ratings_as_mat[user_id].nonzero()[1]
        unrated_items_by_pred_rating = [item for item in item_index_sorted_by_pred_rating
                                        if item not in items_rated_by_this_user]
        return unrated_items_by_pred_rating[-n:]

def get_ratings_data():
    highest_user_id = ratings_contents.user.max()
    highest_movie_id = ratings_contents.movie.max()
    ratings_as_mat = sparse.lil_matrix((highest_user_id, highest_movie_id))
    for _, row in ratings_contents.iterrows():
            # subtract 1 from id's due to match 0 indexing
        ratings_as_mat[row.user-1, row.movie-1] = row.rating
    return ratings_contents, ratings_as_mat

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


if __name__ == "__main__":
    ratings_contents = pd.read_table("data/u.data",
                                     names=["userId", "movieId", "rating",
                                            "timestamp"])
    highest_user_id = ratings_contents.userId.max()
    highest_movie_id = ratings_contents.movieId.max()

    # load train_df, test_df
    # train_df = pickle.load(open('data/train_df.pkl', 'rb'))
    # test_df = pickle.load(open('data/test_df.pkl', 'rb'))
    train_df, test_df = split.train_test_split(ratings_contents)

    #ratings_as_mat = get_ratings_data(ratings_contents)
    # ratings_as_mat = get_ratings_data2(highest_user_id, highest_movie_id, train_df)
    ratings_as_mat = pickle.load(open('data/ratings_as_mat_train.pkl','rb'))
    my_rec_engine = ItemItemRecommender(neighborhood_size=75)
    my_rec_engine.fit(ratings_as_mat)
    user_1_preds = my_rec_engine.pred_one_user(user_id=1, report_run_time=True)
    # Show predicted ratings for user #1 on first 100 items
    print user_1_preds[:100]
    print my_rec_engine.top_n_recs(1, 20)
