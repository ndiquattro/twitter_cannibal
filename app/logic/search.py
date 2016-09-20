import requests


def search_reddit(term):
    # Create URL and search
    headers = {
        'User-Agent': 'Twitter Cannibal 1.0 by /u/box_plot',
    }
    url = "https://www.reddit.com/subreddits/search.json?q=%s&limit=100" % term
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
                # elif data['description']:
                #     desc = data['description']
                else:
                    desc = "No Description Provided."

                subs += [{
                    'url': data['url'],
                    'name': data['display_name'],
                    'description': desc,
                    'subscribers': data['subscribers'],
                    'is_subbed': data['user_is_subscriber']
                }]

    # Covert to pands and return
    return subs
