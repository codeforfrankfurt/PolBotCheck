import json
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def calc_frequencies(words, words_n=50, lang='german'):
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    # words = [word for word in words if word not in all_stopwords]
    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer(lang)
    # words = [stemmer.stem(word) for word in words]

    fdist = nltk.FreqDist(words)
    return fdist.most_common(words_n)

def get_topic_frequencies(tweets, words_n=50, lang='english'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    stopwords_file = '../data/stopwords.txt'
    custom_stopwords = set(open(stopwords_file, 'r').read().splitlines())
    all_stopwords = default_stopwords | custom_stopwords
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=list(all_stopwords))
    X = vectorizer.fit_transform(tweets)
    terms = vectorizer.get_feature_names()

    important_terms = []
    for doc in range(len(tweets)):
        feature_index = X[doc, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
        doc_terms = []
        for w, s in [(terms[i], s) for (i, s) in tfidf_scores]:
            doc_terms.append((w, s))
        important_terms.append([w for w, _ in sorted(doc_terms, key=lambda x: x[1])][:5])
    important_terms = [item for sublist in important_terms for item in sublist]
    topic_frequencies = calc_frequencies(important_terms, words_n=words_n)
    return topic_frequencies

def get_topic_frequencies_two(tweets, words_n=50, lang='english'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    stopwords_file = '../data/stopwords.txt'
    custom_stopwords = set(open(stopwords_file, 'r').read().splitlines())
    all_stopwords = default_stopwords | custom_stopwords

    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=list(all_stopwords))
    X = vectorizer.fit_transform(tweets)
    terms = vectorizer.get_feature_names()

    important_terms = []
    for doc in range(len(tweets)):
        feature_index = X[doc, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
        doc_terms = []
        for word, score in [(terms[i], score) for (i, score) in tfidf_scores]:
            doc_terms.append((word, score))
        important_terms.append([(word, score) for word, score in sorted(doc_terms, key=lambda x: x[1])][:100])
    #important_terms = [item for sublist in important_terms for item in sublist]
    #topic_frequencies = calc_frequencies(important_terms, words_n=words_n)
    return important_terms

def save_wordcloud(frequencies, filename):
    wordcloud = WordCloud(width=1024, height=786).fit_words(frequencies)
    fig = plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(16)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(filename, facecolor='k', bbox_inches='tight')
    print('imaged created')

def load_example_data():
    tweets = []
    with open('../../../tweets.20150430-223406.json') as f:
        for line in f:
            tweets.append(json.loads(line)['text'])
    return tweets

def get_corpus_of_most_active_users(n_users=5):
    tweets = []
    texts = []
    with open('../../../tweets.20150430-223406.json') as f:
        for line in f:
            tweets.append(json.loads(line)['user']['screen_name'])
            texts.append((json.loads(line)['user']['screen_name'], json.loads(line)['text']))

    five_users = nltk.FreqDist(tweets).most_common(n_users)

    dict = {}
    for user, tweet in texts:
        if user in dict:
            dict[user] = " ".join([dict[user],tweet])
        else:
            dict[user] = tweet

    corpus = [dict[name] for name, _ in five_users]
    return  corpus

if __name__ == "__main__":
    #tweets = load_example_data()
    corpus = get_corpus_of_most_active_users()
    topic_frequencies = get_topic_frequencies_two(corpus, words_n=100, lang='english')
    for topic in topic_frequencies:
        print(topic)
    #save_wordcloud(topic_frequencies, 'wordcloud_uk_election.png')
