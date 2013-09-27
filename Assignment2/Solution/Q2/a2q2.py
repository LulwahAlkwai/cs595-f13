# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment2-question2
#Using the ODU Memento Aggregator
#Creating a Histogram URI vs.number of mementos
#
#import request
import urllib2
import re

#input file file to find memento
file1=open("uniq-ultimate-links.txt","r")

#Create a new file for results
file2=open("histogram.txt","w")
#Writing the first line in results
file2.write("url"+","+"memento"+"\n")

#the link that we add to url
uri = "http://mementoproxy.cs.odu.edu/aggr/timemap/link/"

#loop through the file
for line in file1:
    
    #delete new line
    link=line.rstrip("\n")
    
    #opening the new link
    n = uri + link
    
    try:
        #opening the new link
        r = urllib2.Request(n)
        l = urllib2.urlopen(r)
        
        #Display link on screen
        print "link=" + n
        
        #Checking if responce is 200
        if l.code==200:
            timeMap = l.read()
            TOKENIZER_RE = re.compile('(<[^>]+>|[a-zA-Z]+="[^"]*"|[;,])\\s*')
            URI_DATETIME_RE = re.compile('/([12][90][0-9][0-9][01][0-9][0123][0-9]'
                                         '[012][0-9][0-5][0-9][0-5][0-9])/',
                                         re.IGNORECASE)
            URI_DATETIME_FORMAT = '%Y%m%d%H%M%S'
            
            #Memento count
            mc=0
            tokens=TOKENIZER_RE.findall(timeMap)
            
            #Loop in tokens
            for word in tokens:
                if word[:4] == "rel=":
                    rel=word[5:-1]
                    
                    #if memento found we add count
                    if "memento" in rel:
                        mc=mc+1
                    elif "first memento" in rel:
                        mc=mc+1
                    elif "last memento" in rel:
                        mc=mc+1
                    elif "memento first" in rel:
                        mc=mc+1
                    elif "memento last" in rel:
                        mc=mc+1
                    elif "first last memento" in rel:
                        mc=mc+1
            #Print the result on the screen
            print mc
            
            #Write result to file
            file2.write(link + "," + str(mc)+"\n")
    
    #Error printed on screen for tracing
    except urllib2.HTTPError,e:
        print "HTTP Error", e
        mc=0
        #Write result to file with zero memento
        file2.write(link + "," + str(mc)+"\n")
        continue

file1.close()
file2.close()
