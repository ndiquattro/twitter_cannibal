from nltk.corpus import stopwords


# Construct stopwords
en_stop = set(stopwords.words("english")).union(['http', 'https', 'rt', 'co',
                                                 'like'])


def text_cleaner(text):
    newdoc = []
    for doc in doc_set:
        newdoc.append(casual.remove_handles(doc))



