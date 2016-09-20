from data import TweetGrabber, RedditData
from nlps import word_bagger
from search import search_reddit
from app.models import Stats


def analyze_descriptions(token, token_secret):
    # Initialize Data
    tw_api = TweetGrabber(token, token_secret)

    # Descriptions
    descriptions = tw_api.get_descriptions_2levels()

    # Fit model
    word_counts = word_bagger(descriptions)

    return word_counts


def validate(terms, uobj):
    # Get current user's subreddits
    rinfo = RedditData(uobj.redtoken, uobj.redrefresh)
    user_subs = set(rinfo.get_subs())

    for term in terms:
        # Search and parse
        results = search_reddit(term)
        names_results = [sub['name'] for sub in results]
        sub_matches = user_subs.intersection(names_results)

        # Make results object
        res_ob = {'term': term, 'num_results': len(names_results),
                  'num_matches': len(sub_matches)}

        # Save to database
        Stats.add_data(res_ob, uobj)


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
