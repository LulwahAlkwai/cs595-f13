# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment4-question1
import urllib
import urllib2
import re
import os
import sys
import md5
import BeautifulSoup
import subprocess
from subprocess import call

path="../Q1/Allnew100links"

#Creating a new directory to save links
try:
    os.makedirs(path)
except OSError:
    if os.path.exists(path):
        pass
    else:
        print "Directory Error"
        raise

#input file with 1000 links
file1=open("finallinks.txt","r")

#count links
lineCount=0

#loop through the file
for line in file1:
    lineCount=lineCount+1
    
    if lineCount<=100:
        #delete new line
        Oneline=line.rstrip("\n")
        print "lineCount="
        print lineCount
        
        #use beautiful Soup
        try:
            request = urllib2.Request(Oneline)
            response = urllib2.urlopen(request)
            soup = BeautifulSoup.BeautifulSoup(response)
        except:
            continue
            pass
        
        #Create a hash name for the file
        test=md5.new(Oneline)
        hashfilename=test.hexdigest()
        
        internallinklist=[]
        del internallinklist[:]
        
        
        #getting all inner links
        for a in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            link2=a['href']
            
            #Some exceptions on link (.png and .jpj and # and javascript)
            #No redudant links
            if "png" not in link2 and "jpg" not in link2 and "#" not in link2 and "javascript" not in link2 and link2 not in internallinklist:
                internallinklist.append(link2)
        
        #No inner links
        if not internallinklist:
            lineCount=lineCount-1
        
        else:
            with open(os.path.join(path,hashfilename), 'w') as file4:
                print "hash name="
                print hashfilename
                
                print "site:"
                print Oneline
                
                file4.write("site:")
                file4.write("\n")
                file4.write(Oneline)
                file4.write("\n")
                
                print "links:"
                
                file4.write("links:")
                file4.write("\n")
                
                for item in internallinklist:
                    print item
                    
                    file4.write(item)
                    file4.write("\n")
    else:
        print "One Hundred Files Created!!Hoorayyyyyy"
        sys.exit()

file1.close()
file4.close()