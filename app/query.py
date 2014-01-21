#!/usr/bin/python
import json
import requests
import Image
import ImageOps
import urllib
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from cStringIO import StringIO

size = 220, 165


def api_feed(tag, numResults=10):
    """Query the NPR API using given tag ID, generate thumbnail when a story
    has an image. Return dictionary of results"""

    stories = query_api(tag, numResults=10)

    story_list = []
    for story in stories:
        #try:
        #    image_url = story['image'][0]['crop'][0]['src']
        #    image = generate_thumbnail(image_url)
        #except KeyError:
        #    image = 'static/img/thumbnails/irene-thumb.jpg'
        try:
            image = story['image'][0]['crop'][0]['src']
            width = story['image'][0]['crop'][0]['width']
            height = story['image'][0]['crop'][0]['height']
            if int(width) > int(height):
                landscape = True
            else:
                landscape = False
        except KeyError:
            image = ''
            landscape = False
            #image = 'http://www.vpr.net/apps/legislature/static/img/vpr-legislature-no-photo.png'
        link = story['link'][0]['$text']
        date = convert_date(story['storyDate']['$text'])
        title = story['title']['$text'].strip()
        byline = story['byline'][0]['name']['$text']
        print title, landscape
        try:
            text = story['text']['paragraph'][0]['$text']
            if len(text) < 240:
                text = text + '</p><p>' + story['text']['paragraph'][1]['$text']

        except KeyError:
            try:
                text = story['text']['paragraph'][1]['$text']
            except KeyError:
                text = story['text']['paragraph'][2]['$text']

        story_list.append({
            'title': title,
            'date': date,
            'link': link,
            'image': image,
            'text': text,
            'byline': byline,
            'landscape': landscape
        })
    return story_list


def reporter_list(tag, numResults=50):
    """Queries the API for bylines and returns an ordered list of name
    and a path to a photo. Ordered by number of stories"""

    stories = query_api(tag, numResults)

    name_list = []
    reporters = []
    for story in stories:
        name = story['byline'][0]['name']['$text']
        if name not in name_list:
            name_list.append(name)
            byline = {}
            byline['name'] = name
            try:
                url = story['byline'][0]['link'][0]['$text']
                byline['url'] = reporter_image(url)
            except KeyError:
                byline['url'] = False
            byline['count'] = 1
            reporters.append(byline)
        else:
            for reporter in reporters:
                if reporter['name'] == name:
                    reporter['count'] += 1

    reporters = sorted(reporters, key=lambda k: k['count'], reverse=True)

    ranked_list = []
    for reporter in reporters:
        if reporter['url'] and reporter['count'] > 1:
            ranked_list.append(reporter)

    return ranked_list


def query_api(tag, numResults=10):
    url1 = ('http://api.npr.org/query?orgid=692&fields=title,byline,storyDate,image' +
        ',text&sort=dateDesc&action=Or&output=JSON&numResults=')
    url2 = '&apiKey=MDAyMTYyNjQyMDEyMjg5MzU3MTRhNDY5MA001&id='

    url = url1 + str(numResults) + url2
    query = url + str(tag)

    r = requests.get(query)
    j = json.loads(r.text)
    stories = j['list']['story']

    return stories


def reporter_image(url):
    """Takes reporter URL from byline and returns URL to reporter's image"""

    r = requests.get(url)
    page = r.text
    soup = Soup(page)
    person_card = soup.find_all(id="person-card")[0]
    try:
        image = person_card.find_all('img')[0].get('src')
    except IndexError:
        image = False

    return image


def generate_thumbnail(image_url):
    thumbnail_path = 'static/img/thumbnails/'
    unicorn = image_url
    filename = unicorn.rsplit('/', 1)[1]
    f = thumbnail_path + filename
    f_save = '../' + f

    img_file = urllib.urlopen(image_url)
    img = StringIO(img_file.read())
    image = Image.open(img)
    im = ImageOps.fit(image, size, Image.ANTIALIAS)
    im.save(f_save)
    return f


def convert_date(timestamp):
    day = timestamp[5:7]
    month = datetime.strptime(timestamp[8:11], '%b').strftime('%B')
    year = timestamp[12:16]
    date = month + ' ' + day + ", " + year
    return date
