import requests


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
        if data['subreddit_type'] != "private":
            if not data['over18']:

                if data['public_description']:
                    desc = data['public_description']
                elif data['description']:
                    desc = data['description']
                else:
                    desc = "No Description :(, you'll have to check it out to see what's what!"

                subs += [{
                    'name': data['url'],
                    'description': desc,
                    'subscribers': data['subscribers']
                }]

    # Covert to pands and return
    return subs
