import nltk
from nltk.corpus import stopwords

def get_word_frequencies(text, words_n=10, lang='german'):
    default_stopwords = set(nltk.corpus.stopwords.words(lang))
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in default_stopwords]

    fdist = nltk.FreqDist(words)
    for word, frequency in fdist.most_common(words_n):
        print(u'{}:{}'.format(word, frequency))

    return fdist.most_common(words_n)
if __name__ == "__main__":
    text = 'Die offene Gesellschaft ist ein in der Tradition des Liberalismus stehendes Gesellschaftsmodell Karl Poppers, das zum Ziel hat, „die kritischen Fähigkeiten des Menschen“ freizusetzen. Die Gewalt des Staates soll dabei so weit wie möglich geteilt werden, um Machtmissbrauch zu verhindern. Poppers Vorstellung von der offenen Gesellschaft ist eng mit der Staatsform der Demokratie verbunden, allerdings nicht verstanden als Herrschaft der Mehrheit, sondern als die Möglichkeit, die Regierung gewaltfrei abzuwählen. Der offenen Gesellschaft steht einerseits die Laissez-Faire-Gesellschaft gegenüber, andererseits die totalitäre, am holistisch-kollektivistischen Denken ausgerichtete „geschlossene Gesellschaft“, die Popper auch ironisch den „Himmel auf Erden“ nennt, weil sie als solcher propagiert wird.'

    get_word_frequencies(text)
