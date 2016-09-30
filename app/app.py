import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from flask import request
import sys
sys.path.append('../code')
import models # under the code directory
import live_demo_small # under the code directory
import cPickle as pickle
from itertools import chain
import fnmatch
from collections import Counter


app = Flask(__name__)

## load the data
ratings_contents = pd.read_csv('../data/ratings_small.csv')

movies_contents = pd.read_csv("../data/movies_small.csv")
movies_contents = movies_contents.set_index('movieId')

items = pickle.load(open('../data/items_small.pkl','rb'))
item_numbers = pickle.load(open('../data/item_numbers_small.pkl','rb'))
disliked_list = pickle.load(open('../data/disliked_list_small.pkl','rb'))

negative_items = disliked_list
model = models.Word2VecRecommender(size=200, window=max(item_numbers), min_count=1)
model.fit(items)

@app.route('/index')
def index():
    return render_template('index.html')

# Form page to submit text
@app.route('/submission_page')
def submission_page():
    return render_template('submission_page.html')

@app.route('/submission_page_copy')
def submission_page_copy():
    return render_template('submission_page_copy.html')

@app.route('/futures')
def futures():
    return render_template('futures.html')

@app.route('/word_counter', methods=['POST'] )
def word_counter():
    '''
    live_demo_small
    '''
    # ## ========================================================
    # ## load the data
    # ## ========================================================
    # ratings_contents = pd.read_csv('../data/ratings_small.csv')
    #
    # movies_contents = pd.read_csv("../data/movies_small.csv")
    # movies_contents = movies_contents.set_index('movieId')
    #
    # items = pickle.load(open('../data/items_small.pkl','rb'))
    # item_numbers = pickle.load(open('../data/item_numbers_small.pkl','rb'))
    # disliked_list = pickle.load(open('../data/disliked_list_small.pkl','rb'))
    #
    # negative_items = disliked_list
    # model = models.Word2VecRecommender(size=1000, window=max(item_numbers), min_count=1)
    # model.fit(items)

    #up=5;down=2
    # get data from request form, the key is the name you set in your form

    # str_input_list_liked = ['Toy Story*' , 'Terminator*'] # user_items
    # str_input_list_disliked = ['Lord of Illusions*','Castle Freak'] # negative_items
    # str(data) = 'Toy Story*,Terminator*.Lord of Illusions*,Castle Freak*'

    data = request.form['user_input']
    ## data = u'Toy Story*, Jumanji*|Exorcist*,Texas Chainsaw Massacre*'^'Usual Suspects*, Psycho* | Iron Man*, Pirates of the Caribbean*'
    responses = []
    data = str(data).split('^')
    for testset in data:
        response = {}
        # convert data from unicode to string
        testset = str(testset)
        testset = testset.split('|')
        l = testset[0]
        d = testset[1]
        str_input_list_liked = l.split(',')
        str_input_list_disliked = d.split(',')
        extracted, recommendations, images_url = live_demo_small.main(model,movies_contents,str_input_list_liked, str_input_list_disliked)
        response['Liked'] = str_input_list_liked
        response['Disliked'] = str_input_list_disliked
        response['Recommended'] = [x for x in extracted['title']]
        response['Genres'] = [x for x in extracted['genres']]
        response['url'] = images_url
        response['title_url'] = zip(response['url'],response['Recommended'])
        responses.append(response)
    return render_template('word_counter.html', items = responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)
