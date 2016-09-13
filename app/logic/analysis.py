from data import TweetGrabber
from preprocess import text_cleaner
from nlps import word_bagger


def analyze_descriptions(screen_name):
    # Initialize Data
    tw_api = TweetGrabber(screen_name)

    # Descriptions
    descriptions = tw_api.get_descriptions()
    desc_clean = []
    for desc in descriptions:
        desc_clean.append(text_cleaner(desc))

    # Fit model
    word_counts = word_bagger(desc_clean)

    return word_counts


def analyze_retweets(token, token_secret):
    # Initialize Data
    tw_api = TweetGrabber(token, token_secret)

    # Descriptions
    raw = tw_api.get_retweets()
    clean = []
    for text in raw:
        clean.append(text_cleaner(text))

    # Fit model
    word_counts = word_bagger(clean)

    return word_counts