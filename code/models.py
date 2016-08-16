from gensim.models import Word2Vec

class Word2VecRecommender(object):
    DEFAULT_WORD2VEC_PARAMETERS = dict(size=300, window=100000, min_count=5, hs=1 , workers=8)

    def __init__(self, **word2vec_parameters):
        self.word2vec_params = dict(Word2VecRecommender.DEFAULT_WORD2VEC_PARAMETERS)
        self.word2vec_params.update(word2vec_parameters)
        self.model = Word2Vec(**self.word2vec_params)

    def fit(self, items):
        """
            Fits the model to a given list of items.
            `items` is a list of lists of strings. Every list is a certain user's items (from the training set), and items are represented by str ids.
        """
        self.training_items = items
        self.unique_items = set(item for item_list in items for item in item_list)

        trim_rule = self.word2vec_params.get('trim_rule', None)
        self.model.build_vocab(self.training_items, trim_rule=trim_rule)
        self.model.train(self.training_items)
        self.model.init_sims(replace=True) # precompute the L2 normalized vectors

    # original
    def recommend(self, user_items, negative_items = None, num_items = 10):
        negative_items = negative_items or []
        # pick the items only in the item vocabulary
        user_items = [item for item in user_items if item in self.model.vocab]
        negative_items = [item for item in negative_items if item in self.model.vocab]
        if not user_items:
            return []
        #return self.model.most_similar_cosmul(positive=user_items, negative=negative_items, topn=num_items)
        return self.model.most_similar(positive=user_items, negative=negative_items, topn=num_items)

    # testing
    def recommend2(self, test_user, user_items, negative_items = None, num_items = 10):
        negative_items = negative_items or []
        # pick the items only in the item vocabulary
        user_items = [item for item in user_items if item in self.model.vocab]
        negative_items = [item for item in negative_items if item in self.model.vocab]
        #if not user_items:
        #    return []

        # 1th iteration
        #return self.model.most_similar_cosmul(positive=user_items, negative=negative_items, topn=num_items)
        recommendations =  self.model.most_similar(positive=user_items, negative=negative_items, topn=num_items)
        recommended_list = list(zip(*recommendations)[0])
        recommended_list = [int(x) for x in recommended_list]
        cos_sim = list(zip(*recommendations)[1])

        # rec_df = pd.DataFrame(recommendations, columns =['a','b'])

        final = []
        # for movie in recommended_list:
        #     if movie in test_user.movieId.unique():
        #         if movie not in final:
        #             final.append(movie)
        for movie in recommended_list:
            final.append(movie)

        return final
