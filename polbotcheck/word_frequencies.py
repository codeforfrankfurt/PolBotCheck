import nltk
from nltk.corpus import stopwords
from stop_words import get_stop_words


def get_word_frequencies(text, words_n=10, lang='german'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in default_stopwords]

    fdist = nltk.FreqDist(words)
    return fdist.most_common(words_n)

if __name__ == "__main__":
    # lang = 'german'
    # stop_words = set(nltk.corpus.stopwords.words(lang))

    # stop_words = get_stop_words('de')
    # print(stop_words)

    with open('output.txt', 'r') as f:
        text = f.read()
        wf = get_word_frequencies(text,words_n=100)
        for word, frequency in wf:
            print(u'{}:{}'.format(word, frequency))
