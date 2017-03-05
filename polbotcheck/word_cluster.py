import json
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
import nltk
from nltk.corpus import stopwords
from pprint import pprint
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def calc_frequencies(words, words_n=50, lang='german'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    stopwords_file = '../data/stopwords.txt'
    custom_stopwords = set(open(stopwords_file, 'r').read().splitlines())
    all_stopwords = default_stopwords | custom_stopwords
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in all_stopwords]
    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer(lang)
    # words = [stemmer.stem(word) for word in words]

    fdist = nltk.FreqDist(words)
    return fdist.most_common(words_n)

def get_topic_frequencies(tweets, words_n=50, lang='english'):
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
    topic_frequencies = calc_frequencies(important_terms, words_n=words_n)
    return topic_frequencies

def save_wordcloud(frequencies, filename):
    wordcloud = WordCloud().fit_words(frequencies)
    fig = plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(16)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(filename, facecolor='k', bbox_inches='tight')
    print('imaged created')

def load_example_data():
    tweets = []
    with open('../../../data/tweets.20150430-223406.json') as f:
        for line in f:
            tweets.append(json.loads(line)['text'])
    return tweets

if __name__ == "__main__":
    tweets = load_example_data()
    topic_frequencies = get_topic_frequencies(tweets, words_n=100)
    print(topic_frequencies)

    save_wordcloud(topic_frequencies, 'wordcloud_uk_election.png')

