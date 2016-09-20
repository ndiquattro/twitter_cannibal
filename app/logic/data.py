from flask import current_app as app
import tweepy
import praw


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

    def get_descriptions_2levels(self):
        # Get Friend IDs
        fids = tweepy.Cursor(self.api.friends_ids).items()
        fid_list = [fid for fid in fids]

        # Loop through each friend and get their friend IDs
        fid_list2 = []
        for fid in fid_list[:14]:
            for id2 in tweepy.Cursor(self.api.friends_ids, id=fid).items():
                fid_list2.append(id2)

        # Combine lists
        all_ids = fid_list + fid_list2

        # Get descriptions from ID list
        descriptions = []
        for idx in range(0, len(all_ids), 100):
            # Get User objects for this chunk
            chunk_users = self.api.lookup_users(user_ids=all_ids[idx:idx + 100])

            # Get descriptions from this chunk
            for user in chunk_users:
                descriptions.append(user.description)

        return descriptions

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


class RedditData(object):
    def __init__(self, token, retoken):
        # Initiate praw
        r = praw.Reddit('Twitter Cannibal 1.0 by /u/box_plot')

        # Set tokens
        r.set_oauth_app_info(app.config['RDTOKE'], app.config['RDSEC'],
                             app.config['RDCALL'])

        # Set token
        r.set_access_credentials("mysubreddits subscribe", token, retoken)

        self.r = r

    def get_subs(self):
        """ Return list of subreddits of authed user"""
        sub_obs = [sub for sub in self.r.get_my_subreddits()]
        sub_names = [sub.display_name for sub in sub_obs]

        return sub_names

    def subscribe(self, sub):
        """ Subscribe user to a subreddit """

        # Subscribe
        self.r.get_subreddit(sub).subscribe()
