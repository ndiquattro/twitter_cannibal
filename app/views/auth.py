# Flask Imports
from flask import Blueprint, flash, redirect, request, session, url_for
from flask import current_app as app
import tweepy
from app import models
from app.logic.data import TweetGrabber

# Initiate Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/')
def authuser():
    # Initiate Handler
    tw_auth = tweepy.OAuthHandler(app.config['TWTOKE'],
                                  app.config['TWSEC'],
                                  app.config['TWCALL'])

    # Get tokens
    verifier = request.args.get('oauth_verifier')
    tw_auth.request_token = session['reqtoke']

    # Get final token, initalize API
    tw_auth.get_access_token(verifier)
    tw_api = TweetGrabber(tw_auth.access_token, tw_auth.access_token_secret)

    # Get user info
    uinfo = tw_api.api.me()

    # Save session
    session.permanent = True
    session['userid'] = uinfo.id

    # Add user to database
    # Check if we've already authed before
    curusr = models.User.lookup_user(uinfo.id)
    if not curusr:
        # Add user info
        uinfod = {'name': uinfo.name,
                  'twitterid': uinfo.id,
                  'token': tw_auth.access_token,
                  'token_secret': tw_auth.access_token_secret}

        models.User.add_user(uinfod)

    # Make alert
    flash('Thanks! Your twitter account (%s) has been authenticated!' % uinfo.screen_name)

    return redirect(url_for('splash.index'))


@auth.route('/logout')
def logout():

    # Remove session cookie
    session.clear()

    # Redirect to home
    return redirect(url_for('home.index'))
