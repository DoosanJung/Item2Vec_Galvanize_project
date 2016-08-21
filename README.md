# Item2Vec Project
A recommender system based on word2vec

### Neural network based Recommender system
#### Description
In this project, I want to build a new recommender model using newly developed technique(this year), [Item2Vec](https://arxiv.org/pdf/1603.04259.pdf).


>Many Collaborative Filtering (CF) algorithms are item-based in the sense that they analyze item-item relations in order to produce item similarities. Recently, several works in the field of Natural Language Processing suggested to learn a latent representation of words using neural embedding algorithms. Among them, the Skip-gram with Negative Sampling (SGNS), also known as Word2Vec, was shown to provide state-of-the-art results on various linguistics tasks. In this paper, we show that item-based CF can be cast in the same framework of neural word embedding. Inspired by SGNS, we describe a method we name Item2Vec for item-based CF that produces embedding for items in a latent space. The method is capable of inferring item-to-item relations even when user information is not available. We present experimental results on large scale datasets that demonstrate the effectiveness of the Item2Vec method and show it is competitive with SVD.

Item2Vec is introduced for scalable item-item collaborative filtering. Item2Vec Âproduces low dimensional representation for items, where the affinity between items can be measured by cosine similarity. The method is based on the Word2Vec method that was successfully applied to natural language processing applications.

#### Data
MovieLens latest datasets - [Full dataset](http://grouplens.org/datasets/movielens/latest/)</br>(22,000,000 ratings and 580,000 tag applications applied to 33,000 movies by 240,000 users. Last updated 1/2016.)

#### References and Packages used
[Item2Vec](https://arxiv.org/pdf/1603.04259.pdf)
</br>[Gensim](https://radimrehurek.com/gensim/)
</br>[Sparsesvd](https://pypi.python.org/pypi/sparsesvd/)
</br>[Flask](http://flask.pocoo.org/)
</br>[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
</br>[Bootstrap](http://getbootstrap.com/)
</br>[From word embeddings to item recommendation](https://arxiv.org/pdf/1601.01356.pdf)

#### Video demo and Slides
[Video demo](https://youtu.be/L_ktRIDjqRg)
</br>[Slides](https://docs.google.com/presentation/d/1kPe0RocrqYM0FRX-Isi4PdoTYeWYwZbyZddEoECOMvY/edit?usp=sharing)
