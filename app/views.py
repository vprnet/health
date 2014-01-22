from index import app
from query import api_feed, reporter_list
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    page_url = BASE_URL + request.path
    stories = api_feed([245948266, 186100276], numResults=10)
    most_recent = stories[:4]
    stories = stories[4:]
    reporters = reporter_list([245948266, 186100276])
    follow_the_money = api_feed([255414453])[0]

    social = {
        'title': "VPR: Healthcare Coverage 2014",
        'subtitle': 'www.vpr.net/apps/health/',
        'img': 'http://mediad.publicbroadcasting.net/p/vpr/files/201401/statehouse-january.jpg',
        'description': "VPR's guide to the healthcare in Vermont. Latest coverage, exchange updates and the road to single payer, all in one place.",
        'twitter_text': "VPR's guide to healthcare in VT. Latest coverage, exchange updates and the road to single payer",
        'twitter_hashtag': 'VTpoli'
    }

    return render_template('home.html',
        most_recent=most_recent,
        stories=stories,
        social=social,
        page_url=page_url,
        reporters=reporters,
        follow=follow_the_money)


@app.route('/network')
def network():
    page_url = BASE_URL + request.path
    social = {'title': 'Vermont Health Connect: An Interactive Visualization',
        'subtitle': "How It Works and Where it Doesn't",
        'img': 'http://www.vpr.net/apps/health/static/img/vt-health-connect.png',
        'twitter_text': "What's wrong with VT Health Connect in one interactive graphic",
        'twitter_hashtag': "ACA",
        'description': "Walk through Vermont Health Connect from account creation to insurance confirmation, discovering how the system works and where it currently doesn't."}
    return render_template('network.html', social=social, page_url=page_url)

# TEMPLATING: Modularize things further. {% include social %} instead of that block in base
# Also: an analytics include. Really break things down.

#Make a bunch of templates so that any tag can be queried and you've got a template for it
#Modularize design chunks too
