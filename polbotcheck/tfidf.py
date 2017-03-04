import json
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
import nltk
from nltk.corpus import stopwords
from pprint import pprint
from stop_words import get_stop_words

def get_word_frequencies(words, words_n=10, lang='german'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in default_stopwords]

    fdist = nltk.FreqDist(words)
    return fdist.most_common(words_n)

if __name__ == "__main__":
    lang = 'english'
    # lang = 'german'
    tweets = []
    with open('../../../data/tweets.20150430-223406.json') as f:
        for line in f:
            tweets.append(json.loads(line)['text'])

    default_stopwords = nltk.corpus.stopwords.words(lang)
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=default_stopwords)
    X = vectorizer.fit_transform(tweets)
    # print(X)
    terms = vectorizer.get_feature_names()

    important_terms = []
    for doc in range(len(tweets)):
        feature_index = X[doc,:].nonzero()[1]
        tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
        doc_terms =  []
        for w, s in [(terms[i], s) for (i, s) in tfidf_scores]:
            doc_terms.append((w, s))
        important_terms.append([w for w, _ in sorted(doc_terms, key=lambda x: x[1])][:5])
    important_terms = [item for sublist in important_terms for item in sublist]

    # print(important_terms)
    most_common_terms = get_word_frequencies(important_terms)
    print(most_common_terms)
