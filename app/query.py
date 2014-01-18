#!/usr/bin/python
import json
import requests
import Image
import ImageOps
import urllib
from datetime import datetime
from cStringIO import StringIO

size = 220, 165


def api_feed(tag, numResults=10):
    """Query the NPR API using given tag ID, generate thumbnail when a story
    has an image. Return dictionary of results"""

    url1 = ('http://api.npr.org/query?orgid=692&fields=title,storyDate,image' +
        ',text&sort=dateDesc&action=Or&output=JSON&numResults=')
    url2 = '&apiKey=MDAyMTYyNjQyMDEyMjg5MzU3MTRhNDY5MA001&id='

    url = url1 + str(numResults) + url2
    query = url + str(tag)

    r = requests.get(query)
    j = json.loads(r.text)
    stories = j['list']['story']

    story_list = []
    for story in stories:
        #try:
        #    image_url = story['image'][0]['crop'][0]['src']
        #    image = generate_thumbnail(image_url)
        #except KeyError:
        #    image = 'static/img/thumbnails/irene-thumb.jpg'
        try:
            image = story['image'][0]['crop'][0]['src']
        except KeyError:
            image = ''
            #image = 'http://www.vpr.net/apps/legislature/static/img/vpr-legislature-no-photo.png'
        link = story['link'][0]['$text']
        date = convert_date(story['storyDate']['$text'])
        title = story['title']['$text'].strip()
        try:
            text = story['text']['paragraph'][0]['$text']
            if len(text) < 140:
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
        })
    return story_list


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
