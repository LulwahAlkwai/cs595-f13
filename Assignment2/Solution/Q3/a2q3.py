# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment2-question3
#Estimate the age of each of the 1000 URIs using the "Carbon Date" tool
#Create a graph with age (in days) on one axis and number of mementos on the other

import urllib2
import re
from server import *
import time
from datetime import date
from datetime import datetime

#input file file to find memento
file1=open("histogram.txt","r")

#Create a new file for carbon results
file2=open("Alldate.txt","w")

#Create a new file for extracted results
file3=open("histogram2.txt","w")

#Writing the first line in results
file3.write("url"+","+"memento"+","+"Estimated Creation Date"+"\n")

#counter to skip and count lines
lineCount=0

#print todays date so we know what is the age calculated from
today=date.today()
print "todays date is=" + str(today)

#loop through the file
for line in file1:
    lineCount=lineCount+1
    
    #to skip the first line which has the text url,memento
    if lineCount!=1:
    
      #delete new line
      Oneline=line.rstrip("\n")
      splitLine={}
      splitLine=Oneline.split(",")
      link=splitLine[0]
      memento=splitLine[1]
        
      #send link to carbon tool
      CDate=carbonDate(link)

      #Open file for writing
      file2=open("Alldate.txt","w")
        
      #Write result to file
      file2.write("link= " + link + "\n" + CDate + "\n")
      file2.close()
      
      #Open file for reading
      file2=open("Alldate.txt","r")
      
      #Read all data and extract important stuff
      for line in file2:
          l=line.rstrip("\n")
          if l.find("Estimated Creation Date") != -1:
            if l[37:38] != "":
              #Create date format
              d1=l[38:40]
              m1=l[35:37]
              y1=l[30:34]
              edate=date(int(y1), int(m1), int(d1))
              
              #Calculate Age
              Age=abs(today-edate)
                
              #Write result to file
              file3=open("histogram2.txt","w")
              file3.write(link + "," + memento + "," + str(Age.days) + "\n")
              file3.flush()

file1.close()
file2.close()
file3.close()
