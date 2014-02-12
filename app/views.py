from index import app
from query import api_feed, reporter_list
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    page_url = BASE_URL + request.path
    page_title = 'Health Care In Vermont'
    stories = api_feed([245948266, 186100276], numResults=10, thumbnail=True)
    reporters = reporter_list([245948266, 186100276])
    follow_the_money = api_feed([255414453])[0]

    social = {
        'title': "VPR: Healthcare Coverage 2014",
        'subtitle': 'www.vpr.net/apps/health/',
        'img': 'http://www.vpr.net/apps/health/static/img/under_the_hood_share_photo_vpr.png',
        'description': "VPR's guide to health care in Vermont. Includes coverage of the health care exchange, the latest in state policy and implementation of a single payer system in Vermont.",
        'twitter_text': "VPR's guide to healthcare in VT. Latest coverage, exchange updates and the road to single payer",
        'twitter_hashtag': 'VTpoli'
    }

    return render_template('content.html',
        page_title=page_title,
        stories=stories,
        social=social,
        page_url=page_url,
        reporters=reporters,
        follow=follow_the_money)


@app.route('/network')
def network():
    page_title = "Under The Hood: VT Health Connect"
    page_url = BASE_URL + request.path
    social = {'title': 'Vermont Health Connect: An Interactive Visualization',
        'subtitle': "How It Works and Where it Doesn't",
        'img': 'http://www.vpr.net/apps/health/static/img/vt-health-connect.png',
        'twitter_text': "What's wrong with VT Health Connect in one interactive graphic",
        'twitter_hashtag': "ACA",
        'description': "Walk through Vermont Health Connect from account creation to insurance confirmation, discovering how the system works and where it currently doesn't."}
    return render_template('network.html',
        page_title=page_title,
        social=social,
        page_url=page_url)
