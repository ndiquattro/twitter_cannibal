from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import gensim


# Very basic bag of words
def word_bagger(tlist):
    # Initialize algo
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000)

    # Fit the model
    train_data_features = vectorizer.fit_transform(tlist)
    train_data_features = train_data_features.toarray()

    # Parse results into word counts
    vocab = vectorizer.get_feature_names()
    dist = np.sum(train_data_features, axis=0)  # Word counts

    # For each, print the vocabulary word and the number of times it appears
    word_counts = []
    for tag, count in zip(vocab, dist):
        word_counts += [{'count': count, 'word': tag}]

    # Return a Pandas Dataframe
    return pd.DataFrame.from_dict(word_counts)

# LDA

