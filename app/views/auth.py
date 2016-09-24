# Flask Imports
from flask import Blueprint, flash, redirect, request, session, url_for
from flask import current_app as app
import tweepy
import praw
from app import models
from app.logic.data import TweetGrabber

# Initiate Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/twitter')
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
    print 'From Twitter ID: {}'.format(uinfo.id)
    print 'In session ID: {}'.format(session['userid'])

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


@auth.route('/reddit')
def authreddit():
    # Initiate PRAW
    r = praw.Reddit('Twitter Cannibal 1.0 by /u/box_plot')
    r.set_oauth_app_info(app.config['RDTOKE'], app.config['RDSEC'],
                         app.config['RDCALL'])

    # Get tokens
    cbacktoken = request.args.get('code')
    access_info = r.get_access_information(cbacktoken)
    print access_info

    # Add info to database
    curusr = models.User.lookup_user(session['userid'])
    models.User.add_reddit_info(curusr, access_info)

    session['reddit_authed'] = True

    # Make alert
    flash('Thanks! Your Reddit account has been authenticated!')

    return redirect(url_for('splash.index'))


@auth.route('/logout')
def logout():

    # Remove session cookie
    session.clear()

    # Redirect to home
    return redirect(url_for('splash.index'))
