import numpy as np
import pandas as pd
import cPickle as pickle
import sys
sys.path.append('code')
import models
from itertools import chain
import fnmatch
from collections import Counter

## google image search
from bs4 import BeautifulSoup
import re
import urllib2

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'lxml')

def find_imgs(titles):
    images_url = []
    for query in titles:
        query= query.split()
        query='+'.join(query)+'+poster'
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        header = {'User-Agent': 'Google Chrome'}
        soup = get_soup(url,header)
        img_soup = soup.find_all("img", {"src": re.compile("gstatic.com")})
        images = [a['src'] for a in img_soup]
        img = images[0]
        images_url.append(img)
    return images_url
# end google image search

def make_input_items(df, total_lst, str_input_list, sign):
    input_items=[]
    for str_input in str_input_list:
        # df.loc[df['title'].isin(['Legend (2015)','Toy Story (1995)'])]
        filtered = fnmatch.filter(total_lst,str_input)
        df.loc[df['title'].isin(filtered)]
        lst = df.loc[df['title'].isin(filtered)].index.tolist()
        #[1, 3114, 78499]
        if sign == 1:
            input_items.append([str(x) for x in lst])
        else:
            input_items.append([str(-1 * x) for x in lst])
    return input_items

# str_input_list = ['Toy Story*' , 'Terminator*'] # user_items
# user_items = make_input_items(df,total_lst,str_input_list,1)
# list(itertools.chain.from_iterable(user_items))
# #=> ['1', '3114', '78499', '589', '1240', '6537', '68791', '120799']
#
# # str_input_list == ['Lord of Illusions*','Castle Freak'] # negative_items
# negative_items = make_input_items(df,total_lst,str_input_list,-1)
# list(itertools.chain.from_iterable(negative_items))

def main(model,movies_contents,str_input_list_liked, str_input_list_disliked):
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
    #
    ## ========================================================
    ## input_items
    ## ========================================================
    # str_input_list_liked = ['Toy Story*' , 'Terminator*'] # user_items
    # str_input_list_disliked = ['Lord of Illusions*','Castle Freak'] # negative_items

    df = movies_contents
    total_lst = df['title'].tolist()
    user_items = make_input_items(df,total_lst,str_input_list_liked,1)
    user_items = list(chain.from_iterable(user_items))
    negative_items = make_input_items(df,total_lst,str_input_list_disliked,-1)
    negative_items = list(chain.from_iterable(negative_items))
    # user_items = ['8','146', '609', '711', '754', '808', '828']
    # negative_items = ['-132','-190','-200', '-226', '-240', '-373', '-422']

    ## ========================================================
    ## output
    ## ========================================================
    show_user_items = [int(x) for x in user_items]
    show_negative_items = [int(x)*-1 for x in negative_items]
    negative_items = [str(x) for x in show_negative_items]
    liked_list = movies_contents.ix[show_user_items,:]
    disliked_list = movies_contents.ix[show_negative_items,:]
    print 'liked_list:\n', liked_list
    print ' '
    print 'disliked_list:\n', disliked_list

    recommendations = model.recommend(user_items, negative_items, num_items=200)
    recommendations = [x for x in recommendations if x[1] > 0.5]
    print "cosine_similarities:\n",recommendations
    print "Recommended movies"
    if recommendations != []:
        recommended_list = list(zip(*recommendations)[0])
        # adjusting index by subtracting 1
        recommended_list = [int(x)-1 for x in recommended_list]
        recommended_list = [x for x in recommended_list if x in movies_contents.index.tolist()]
        extracted = movies_contents.ix[recommended_list,:]

        # genres filter
        total_lst = extracted['genres']
        if not disliked_list.empty:
            c = Counter(chain.from_iterable( [x.split('|') for x in disliked_list['genres']] ))
            if c > 1:
                input_list = zip(*c.most_common()[:len(c)-1])[0]
            else:
                input_list = c.keys()
            str_input_list = ['*'+str(x)+'*' for x in input_list]#["*Thriller*",'*Horror*']
            for str_input in str_input_list:
                filtered = fnmatch.filter(total_lst, str_input)
                mask = np.logical_not(extracted['genres'].isin(filtered))
                extracted = extracted[mask][:10]

            images_url = find_imgs(extracted['title'])

        else:
            extracted = pd.DataFrame(columns=['title','genres'])
            images_url = []

    else:
        # TODO: No recommendations case
        extracted =[]
        images_url = ['https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/No_sign.svg/2000px-No_sign.svg.png']
        recommendations=pd.DataFrame()
    return extracted, recommendations, images_url



if __name__=="__main__":
    # str_input_list_liked = ['NeverEnding Story*' , 'Home Alone*'] # user_items
    # str_input_list_disliked = ['Exorcist*', 'Texas Chainsaw Massacre*'] # negative_items
    # str_input_list_liked = ['Usual Suspects*','Psycho*'] # user_items
    # str_input_list_disliked = ['Iron Man*', 'Pirates of the Caribbean*'] # negative_items
    extracted = pd.DataFrame()
    extracted, recommendations, images_url = main(model,movies_contents,str_input_list_liked,str_input_list_disliked)
