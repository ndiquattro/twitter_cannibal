from flask import Blueprint, render_template, session, redirect, url_for
from flask import current_app as app
import tweepy
import praw
from app.logic.analysis import analyze_descriptions, validate
from app.models import User, Clicks, Subscriptions
from app.logic.search import search_reddit
from app.logic.data import RedditData
import datetime

# Register blueprint
splash = Blueprint('splash', __name__)


# Functions
def timecheck(stamp):
    if stamp:
        # Has it been 15 minutes since this analysis was run?
        tdelta = datetime.datetime.now() - stamp

        return tdelta > datetime.timedelta(minutes=15)
    else:
        return True


@splash.route('/')
def index():
    # Check if this person has authed
    if 'userid' in session:

        # Check for reddit authentication
        if not session.get('reddit_authed'):
            # Generate reddit auth url
            r = praw.Reddit('Twitter Cannibal 1.0 by /u/box_plot')
            r.set_oauth_app_info(app.config['RDTOKE'], app.config['RDSEC'],
                                 app.config['RDCALL'])

            reddit_aurl = r.get_authorize_url('twcan', 'mysubreddits subscribe',
                                              True)

            return render_template("splash/index.html", raurl=reddit_aurl)

        # Check if we need to run analysis again
        if timecheck(session.get('timestamp')):
            # Reterive user tokens
            uinfo = User.lookup_user(session['userid'])

            # Analyze Descriptions and save to session
            descdat = analyze_descriptions(uinfo.token, uinfo.token_secret)
            topdat = descdat.sort_values('count', ascending=False).head(10)
            topterms = topdat.word.tolist()
            session['topterms'] = topterms
            session['timestamp'] = datetime.datetime.now()

            # Validate results
            validate(topterms, uinfo)

        # Get first term to preload search
        fterm = session['topterms'][0]
        # uinfo = User.lookup_user(session['userid'])
        # validate(session['topterms'], uinfo)
        return redirect(url_for('splash.search', term=fterm))

    else:
        # Generate oAuth URL
        tw_auth = tweepy.OAuthHandler(app.config['TWTOKE'],
                                      app.config['TWSEC'],
                                      app.config['TWCALL'])

        aurl = tw_auth.get_authorization_url()

        # Save request token
        session['reqtoke'] = tw_auth.request_token

        return render_template("splash/index.html", authurl=aurl)


@splash.route('/search/<string:term>')
def search(term):
    # Search Reddit
    search_results = search_reddit(term)

    # Found terms
    topterms = session['topterms']

    return render_template("splash/search.html", redresults=search_results,
                           terms=topterms)


@splash.route('/sendtosub/<string:sub>')
def sendtosub(sub):
    # Look up current user
    curusr = User.lookup_user(session['userid'])

    # Add click to database
    Clicks.add_click(sub, curusr)

    # Construct URL
    sub_url = 'http://www.reddit.com/r/' + sub

    return redirect(sub_url)


@splash.route('/subtosub/<string:sub>')
def subtosub(sub):
    # Get user info
    uobj = User.lookup_user(session['userid'])

    # Set up praw
    redapi = RedditData(uobj.redtoken, uobj.redrefresh)

    # Subscribe to the subreddit
    redapi.subscribe(sub)
    Subscriptions.rec_sub(sub, uobj)

    # Construct URL
    sub_url = 'http://www.reddit.com/r/' + sub

    return redirect(sub_url)
