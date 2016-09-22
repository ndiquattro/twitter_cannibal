from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import casual

# Construct stopwords
custom_stop = ['http', 'https', 'co', 'rt', 'like', 'official', 'twitter',
               'account', 'tweets']
en_stop = set(stopwords.words("english")).union(custom_stop)


# Bag of words
def word_bagger(tlist):

    # Take out twitter handles
    newdoc = []
    for doc in tlist:
        newdoc.append(casual.remove_handles(doc))

    # Initialize algo
    counter = CountVectorizer(ngram_range=(1, 3), stop_words=en_stop, min_df=4)

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


# Kmeans based approach
def cluster_terms(docs):
    # Set up vectorizor
    vectorizer = HashingVectorizer(stop_words=en_stop, norm='l2',
                                   ngram_range=(1, 2))

    # Vectorize
    counts = vectorizer.fit_transform(docs)

    # Fit Kmeans model
    km = KMeans(n_clusters=5)
    idx = km.fit_predict(counts)

    # Label descriptions
    clust_docs = pd.DataFrame(zip(docs, idx))
    clust_docs.columns = ['text', 'cluster']
    clust_docs = clust_docs.groupby(['cluster'])

    # Term Finder
    def term_finder(docs, counter):
        # Count up terms for this cluster
        counts = counter.fit_transform(docs).toarray()

        # Combine with vocab into a dataframe
        vocab = counter.get_feature_names()
        dist = np.sum(counts, axis=0)

        word_counts = []
        for tag, count in zip(vocab, dist):
            word_counts += [{'count': count, 'word': tag}]

        word_counts = pd.DataFrame.from_dict(word_counts)
        word_counts = word_counts.sort_values('count', ascending=False)

        # Get top unigrams and bigrams
        unis = word_counts[
            word_counts.word.apply(lambda x: len(x.split()) == 1)].head(2)
        bis = word_counts[
            word_counts.word.apply(lambda x: len(x.split()) == 2)].head(2)

        # Combine
        topdf = pd.concat([unis, bis])

        return topdf

    # Get Term Frequency for each cluseter
    counter = CountVectorizer(ngram_range=(1, 2), stop_words=en_stop)
    term_counts = clust_docs['text'].apply(term_finder, counter)

    return term_counts.sort_values('count', ascending=False)
