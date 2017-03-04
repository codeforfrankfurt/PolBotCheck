import json
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
import nltk
from nltk.corpus import stopwords

if __name__ == "__main__":

    with open('sapmle_tweets.json') as json_data:
        tweets = json.load(json_data)
    # categories = [ 'alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space' ]
    # dataset = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

    # print("%d documents" % len(dataset.data))
    # print("%d categories" % len(dataset.target_names))
    # hasher = HashingVectorizer(n_features=opts.n_features, stop_words='english', non_negative=True, norm=None, binary=False)
    default_stopwords = nltk.corpus.stopwords.words('german')
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=default_stopwords)
    X = vectorizer.fit_transform(tweets)
    print(X)
    terms = vectorizer.get_feature_names()

    for doc in range(len(tweets)):
        feature_index = X[doc,:].nonzero()[1]
        tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
        for w, s in [(terms[i], s) for (i, s) in tfidf_scores]:
            if w == 'ja':
                print(w, s)
    # print(terms[878])
