# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment3-question1

import urllib2
import re
import subprocess
from subprocess import call
import md5
import os

dir1_name='../All'
#Creating a new directory to pages
try:
    os.makedirs(dir1_name)
except OSError:
    if os.path.exists(dir1_name):
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
    
    print "lineCount="
    print lineCount

    #delete new line
    Oneline=line.rstrip("\n")

    #step one is to use curl
    try:
      r = urllib2.Request(Oneline)
      l = urllib2.urlopen(r)

      #make sure page still existed
      if l.code==200:
       allData=l.read()
       #Display link on screen
       print "link="
       print Oneline

       #step two is to creat hash to save in
       #calling md5 found on:
       #http://www.velocityreviews.com/forums/t357410-md5-from-python-different-then-md5-from-command-line.html
       print "hash name="
       test=md5.new(Oneline)
       filename=test.hexdigest()
       print filename
       
       with open(os.path.join(dir1_name,filename+'.txt'), 'w') as file3:
          file3.write(allData)
       
       #loop through the file to remove (most) of the HTML markup
       #Step three to use lynx
       #remove tags
       cmd = os.popen("lynx -dump -force_html %s %s" %(line,filename))
       output_no_tags = cmd.read()
       cmd.close()
       with open(os.path.join(dir1_name,filename+'.processed.txt'), 'w') as file4:
          file4.write(output_no_tags)
            
    except: 
       print 'error'

file1.close()
