# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment2-question1
#Note:
#This code is an alteration version of the code on:
#http://thomassileo.com/blog/2013/01/25/using-twitter-rest-api-v1-dot-1-with-python/
#
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import httplib2


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

#Adding my own keys
CONSUMER_KEY = "Er2mm4vGncBo9nX49Esw"
CONSUMER_SECRET = "p2jmyo7OmfgeeeJiqtoQzowZftMucjnUyeMOMRZw82Y"

OAUTH_TOKEN = "251457467-tF4mgbwex37kkkbYzzjXGRgtQd29FhFMKgXa1mdM"
OAUTH_TOKEN_SECRET = "mcRcLNMdPtlSeldfbpWdnzupdXXh70VU3cNhmxxemDk"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
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

#Here is where the alteration starts:

#Creating a function to follow redirected links to ultimate ones
#code from http://stackoverflow.com/questions/6158895/httplib-is-not-getting-all-the-redirect-codes/11617817#11617817
#need to install a package:httplib2
#http://code.google.com/p/httplib2/downloads/list

def getContentLocation(link):
    h = httplib2.Http(".cache_httplib")
    h.follow_all_redirects = True
    resp = h.request(link, "GET")[0]
    contentLocation = resp['content-location']
    return contentLocation

if __name__ == "__main__":
    if not OAUTH_TOKEN:
      token, secret = setup_oauth()
      print "OAUTH_TOKEN: " + token
      print "OAUTH_TOKEN_SECRET: " + secret
      print
    else:
      #defining a list of screen names to extract links from
      #list from http://www.techrepublic.com/blog/tech-sanity-check/techies-the-top-10-people-you-should-follow-on-twitter/
      #http://www.teachthought.com/learning/100-scientists-on-twitter-by-category/
        
      ScreenName = {'timoreilly','Enderle','thurrott','Jeremiah Owyang','LanceUlanoff','charleneli','jsnell','Rafe','davezatz','Padmasree','harrymccracken','leolaporte','inafried','abbielundberg','mattcutts','mattcutts','saschasegan','comp_science','timberners_lee','geminodreal','SebastianThrun','BobMetcalfe','lemire','fortnow','geomblog','DrQz','TheScienceGuy','carlzimmer','edyong209','Jorge_Salazar','Bill_Romanos','QuantumDottie','Happy_Scientist'}

      #creating a new file for saving raw links
      file1 = open('rawlinks.txt','w')
      #creating a new file for saving ultimate links
      file2 = open('ultimatelinks.txt','w')

      oauth = get_oauth()

      #Creating a list to save initial links
      Initial_List=[]
      #Creating a list to save final distination of link
      Redirected_List=[]

      #by using specification in links :
      #https://dev.twitter.com/docs/api/1.1
      #https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
      #Specifying the uri
      #Specifying the person that we want to take the links from his stream
      #Specifying the number of output
      for n in ScreenName:
         r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+ n +"&count="+"200", auth=oauth)
         p = r.json()
         for tweet in p:
            try:
                  u=tweet['entities']['urls'][0]['expanded_url']
                 
                  print "Original link="
                  print u
                  #Getting the response code
                  #from http://stackoverflow.com/questions/1140661/python-get-http-response-code-from-a-url
                  r = requests.head(u)
                  print "responce code=" 
                  print r.status_code
                  
                  #Adding to the list-for testing purposes,this step may be removed
                  Initial_List.append(u)
                  #Writing to a file
                  file1.write(u)
                  file1.write('\n')

                  #Finding the ultimate link
                  e=getContentLocation(u)
                  print "Redirected link="
                  print e
                  #Getting the response code
                  r = requests.head(e)
                  print "responce code=" 
                  print r.status_code

                  #Adding to the list-for testing purposes,this step may be removed
                  Redirected_List.append(e)
                  #Writing to a file
                  file2.write(e)
                  file2.write('\n')
            except:
                pass

      #Checking the number of links obtained
      print "Number of raw links="+ str(len (Initial_List))
      print "Number of ultimate links="+ str(len (Redirected_List))

      #Closing the files
      file1.close()
      file2.close()
