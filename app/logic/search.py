import requests
import pandas as pd
import json


def search_reddit(term):
    # Create URL and search
    headers = {
        'User-Agent': 'Twitter Cannibal 1.0 by /u/box_plot',
    }
    url = "https://www.reddit.com/subreddits/search.json?q=%s" % term
    r = requests.get(url, headers=headers)

    # Convert to dictionary list
    rdict = r.json()
    sublist = rdict['data']['children']

    # Iterate and pull out info
    subs = []
    for sub in sublist:
        data = sub['data']
        subs += [{
            'name': data['url'],
            'description': data['public_description'],
            'subscribers': data['subscribers']
        }]

    # Covert to pands and return
    return subs
