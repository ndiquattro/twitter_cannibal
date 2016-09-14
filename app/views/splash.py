from flask import Blueprint, render_template, session, redirect, url_for
from flask import current_app as app
import tweepy
from app.logic.analysis import analyze_descriptions, analyze_retweets
from app.models import User
from app.logic.search import search_reddit

# Register blueprint
splash = Blueprint('splash', __name__)


@splash.route('/')
def index():
    # Check if this person has authed
    if 'userid' in session:
        # Reterive user tokens
        uinfo = User.lookup_user(session['userid'])

        # Analyze this user
        descdat = analyze_descriptions(uinfo.token, uinfo.token_secret)
        topdat = descdat.sort_values('count', ascending=False).head(10)

        # Search Reddit
        search_results = search_reddit(topdat.word.head(1).tolist()[0])

        return render_template("splash/index.html", descdat=search_results)

    else:
        # Generate oAuth URL
        tw_auth = tweepy.OAuthHandler(app.config['TWTOKE'],
                                      app.config['TWSEC'],
                                      app.config['TWCALL'])

        aurl = tw_auth.get_authorization_url()

        # Save request token
        session['reqtoke'] = tw_auth.request_token

        return render_template("splash/index.html", authurl=aurl)
