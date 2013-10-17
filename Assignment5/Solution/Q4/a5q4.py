# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment2-question1
#Note:
#This code is an alteration version of the code on:
#http://thomassileo.com/blog/2013/01/25/using-twitter-rest-api-v1-dot-1-with-python/
#
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

#Adding my own keys
CONSUMER_KEY = "Er2mm4vGncBo9nX49Esw"
CONSUMER_SECRET = "p2jmyo7OmfgeeeJiqtoQzowZftMucjnUyeMOMRZw82Y"

OAUTH_TOKEN = "251457467-tF4mgbwex37kkkbYzzjXGRgtQd29FhFMKgXa1mdM"
OAUTH_TOKEN_SECRET = "mcRcLNMdPtlSeldfbpWdnzupdXXh70VU3cNhmxxemDk"

#Save result in file
file1 = open('twitterFollowings2.txt','w')
file2 = open('twitterlog2.txt','w')

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r=requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]
    
    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url
    
    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
                   
                   # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
                   
    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
#Here where is all the alteration starts
        oauth = get_oauth()
        r=requests.get(url="https://api.twitter.com/1.1/followers/list.json?cursor=-1&screen_name=lollleee3&skip_status=true&count=200&include_user_entities=false", auth=oauth)
        p=r.json()["users"]
        file2.write(str(p))
        file1.write("Screen Name,Number of Followings")
        file1.write("\n")
        #adding my scree name and number of followers to the list
        file1.write("lollleee3,381")
        file1.write("\n")

        for f in p:
            name=f["screen_name"]
            count=f["friends_count"]
            file1.write(name + "," + str(count) + "\n")

file1.close()
file2.close()