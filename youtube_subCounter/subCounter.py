# coding=utf-8

"""
Print basic info about a YouTube channel to the console.

This script requires an API key to work, get yours as follows:
  * get API key from console.developers.google.com
  * click on "Credentials", then on "+CREATE CREDENTIALS"
  * click on "Library", then on "YouTube Data API", then "enable" it

Inspiration: https://github.com/howCodeORG/Python-Sub-Count

Run as follows (requires python3):
    $ python subCounter.py
"""

__author__      = 'Alf Köhn-Seemann'
__email__       = 'alf.koehn@posteo.net'
__copyright__   = 'Alf Köhn-Seemann'
__license__     = 'MIT'


# import standard modules
import urllib.request
import json

# enter your own key here, see doc-string for some info
key     = "ENTER-YOUR-KEY-HERE"

# ask for YouTube username for which infos should be displayed
print()
name    = input("Enter username : ")

# get data from google's youtube API and convert it into a json string
youtube_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="
data        = urllib.request.urlopen(youtube_url+name+"&key="+key).read()

# extract available data from json object
subs        = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
views       = json.loads(data)["items"][0]["statistics"]["viewCount"]
comments    = json.loads(data)["items"][0]["statistics"]["commentCount"]
videos      = json.loads(data)["items"][0]["statistics"]["videoCount"]

# print summary to console
print( "    subscribers: {0:d}".format(int(subs)) )
print( "    views      : {0:d}".format(int(views)) )
print( "    videos     : {0:d}".format(int(videos)) )
print()

