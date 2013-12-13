import urllib
import urllib2
import re
import os
import sys
import md5
from BeautifulSoup import BeautifulSoup
import subprocess
from subprocess import call

count = 1
f1 = open('girlsgonechild.txt', 'r')
f2 = open('blogstitle.txt', 'w')

data= f1.read()
soup = BeautifulSoup(data)
contents = soup.findAll('title')
for content in contents:
    print str(count) +"_"+ content.text
    count=count+1
    f2.write(content.text)
    f2.write("\n")