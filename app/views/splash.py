from flask import Blueprint, render_template, session, redirect, url_for
from flask import current_app as app
import tweepy
from app.logic.analysis import analyze_descriptions
from app.models import User, Clicks
from app.logic.search import search_reddit
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

        # Check if we need to run analysis again
        if timecheck(session.get('timestamp')):
            # Reterive user tokens
            uinfo = User.lookup_user(session['userid'])

            # Analyze Descriptions and save to session
            descdat = analyze_descriptions(uinfo.token, uinfo.token_secret)
            topdat = descdat.sort_values('count', ascending=False).head(10)
            session['topterms'] = topdat.word.tolist()
            session['timestamp'] = datetime.datetime.now()

        # Get first term
        fterm = session['topterms'][0]

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
