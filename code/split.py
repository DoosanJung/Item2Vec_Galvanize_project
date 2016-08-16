from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def split_ratio(ratings_contents):
    num_user = len(ratings_contents.userId.unique())
    res = np.zeros(num_user)
    num_iter = 0
    for i in xrange(num_user):
        tmp_user = ratings_contents[ratings_contents['userId']==i+1]
        #split = pd.Series.quantile(user1.timestamp,0.75)
        #split = np.percentile(tmp_user.timestamp,70)
        st = tmp_user.timestamp.sort_values()
        stu = tmp_user.timestamp.sort_values().unique()
        split = np.percentile(stu,70)
        above_u = len(stu[stu >= split])
        below_u = len(stu[stu < split])
        if below_u > 0:
            res[i] = above_u / below_u
        num_iter += 1
        if num_iter % 100 == 0:
            print 'split_ratio iteration: ', num_iter, 'out of', num_user
    #plt.hist(res, bins = 50)
    #plt.show()
    #print res
    print 'min',res.min()
    print 'max',res.max()
    print 'argmin',res.argmin()
    print 'argmax',res.argmax()
    i = res.argmin()
    tmp_user = ratings_contents[ratings_contents['userId']==i+1]
    #split = pd.Series.quantile(user1.timestamp,0.75)
    #split = np.percentile(tmp_user.timestamp,70)
    st = tmp_user.timestamp.sort_values()
    stu = tmp_user.timestamp.sort_values().unique()
    split = np.percentile(stu,70)
    above_u = len(stu[stu >= split])
    below_u = len(stu[stu < split])
    print 'above_u, below_u: ',above_u, below_u

    i = res.argmax()
    tmp_user = ratings_contents[ratings_contents['userId']==i+1]
    #split = pd.Series.quantile(user1.timestamp,0.75)
    #split = np.percentile(tmp_user.timestamp,70)
    st = tmp_user.timestamp.sort_values()
    stu = tmp_user.timestamp.sort_values().unique()
    split = np.percentile(stu,70)
    above_u = len(stu[stu >= split])
    below_u = len(stu[stu < split])
    print 'above_u, below_u: ',above_u, below_u


def train_test_split(ratings_contents):
    num_user = len(ratings_contents.userId.unique())
    num_iter = 0
    for i in xrange(num_user):
        tmp_user = ratings_contents[ratings_contents['userId']==i+1]
        st = tmp_user.timestamp.sort_values()
        stu = tmp_user.timestamp.sort_values().unique()
        split = np.percentile(stu,70)
        # above_u = stu[stu >= split]
        # below_u = stu[stu < split]
        above = st[st >= split]
        below = st[st < split]
        above_df = tmp_user[tmp_user['timestamp'] >= split ]
        below_df = tmp_user[tmp_user['timestamp'] < split ]

        #print 'train',below_df.shape[0] , len(below)
        #print 'test',above_df.shape[0] , len(above)

        if above_df.shape[0] != len(above):
            print 'shit!! ', i+1 ,' above'
        if below_df.shape[0] != len(below):
            print 'shit!! ', i+1 ,' below'

        if i==0:
            train_df = below_df
            test_df = above_df
        else:
            train_df = train_df.append(below_df)
            test_df = test_df.append(above_df)

        num_iter += 1
        if num_iter % 100 == 0:
            print 'split_ratio iteration: ', num_iter, 'out of', num_user

        #print 'appending ',i+1,'user df'
        #print 'train_df',train_df.shape
        #print 'test_df',test_df.shape
        #print '==========================='

    return train_df, test_df


if __name__=="__main__":
    train_df , test_df = train_test_split(ratings_contents)

    with open('data/train_df.pkl','w') as f:
        pickle.dump(train_df, f)
    with open('data/test_df.pkl','w') as f:
        pickle.dump(test_df, f)




    # ratings_contents
    # to human readable type
    #readable = [datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d') for x in ratings_contents.timestamp]
