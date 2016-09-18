from flask import current_app as app
import tweepy


class TweetGrabber(object):
    def __init__(self, token, token_secret):
        # oAuth
        tw_auth = tweepy.OAuthHandler(app.config['TWTOKE'], app.config['TWSEC'],
                                      app.config['TWCALL'])
        tw_auth.set_access_token(token, token_secret)

        # Set up API
        self.api = tweepy.API(tw_auth)

    def get_descriptions(self):
        friends = tweepy.Cursor(self.api.friends).items(300)
        follows = []
        for friend in friends:
            # Process each follow
            follows.append(friend.description)

        return follows

    def get_retweets(self):
        # First get all tweets
        all_tweets = tweepy.Cursor(self.api.user_timeline).items()

        # Pull out the needed info
        tweets = []
        for tweet in all_tweets:
            tweets += [{
                'text': tweet.text,
                'retweeted': tweet.retweeted
            }]

        # Pull out retweets
        retweets = [t for t in tweets if t['retweeted']]

        return retweets

    def get_favorites(self):
        # Get last 300 favoirtes
        favs = tweepy.Cursor(self.api.favorites).items(300)

        # Pull out text
        fav_texts = [f.text for f in favs]

        return fav_texts
