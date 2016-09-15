from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import casual

# Construct stopwords
en_stop = set(stopwords.words("english")).union(['http', 'https', 'rt', 'co',
                                                 'like'])


# Bag of words
def word_bagger(tlist):

    # Take out twitter handles
    newdoc = []
    for doc in tlist:
        newdoc.append(casual.remove_handles(doc))

    # Initialize algo
    counter = CountVectorizer(ngram_range=(1, 3), stop_words=en_stop)

    # Fit the model
    counts = counter.fit_transform(newdoc).toarray()

    # Summarize counts
    vocab = counter.get_feature_names()
    dist = np.sum(counts, axis=0)

    word_counts = []
    for tag, count in zip(vocab, dist):
        word_counts += [{'count': count, 'word': tag}]

    word_counts = pd.DataFrame.from_dict(word_counts)

    # Return a Pandas Dataframe
    return word_counts
