import re
from nltk.corpus import stopwords


def text_cleaner(text):
    # Keep only letters
    letters_only = re.sub("[^a-zA-Z]", " ", text)

    # Split into words
    words = letters_only.lower().split()

    # Keep words of a certain length
    words = [w for w in words if len(w) > 3]

    # Remove stop words
    stops = set(stopwords.words("english"))
    badwords = stops.union(['http', 'https'])  # Add custom words to remove
    meaningful_words = [w for w in words if not w in badwords]

    # Recombine
    return (" ".join(meaningful_words))



