# -*- encoding: utf-8 -*-
#Lulwah Alkwai
#
#
#Assignment4-question2
import urllib
import urllib2
import re
import os
import sys
from collections import OrderedDict


path="../Q1/Allnew100links/"

#decleare variables
#dictionary to save all uri and matching count
URIs=dict()
lineCount=0

#create a new graph viz dot file
graphviz=open("graphviz.dot", "w")
graphviz.write("digraph graphviz {\n")

#loop all files in the path
for l in os.listdir(path):
        #variable to test which line are we at
        x=0
        output=""
        output1=""
        output2=""
        site=""
        with open(path+str(l)) as Onefile:
            for line in Onefile:
                #step one:grab site name
                #site name
                if x == 1:
                    site=line.strip()
                    if not site in URIs:
                       URIs[site]=lineCount
                       output1=str(URIs[site])
                       lineCount=lineCount+1
                #step two:grab links
                #links name
                elif x >= 3:
                    links=line.strip()
                    #Checking if already in dic
                    if not links in URIs:
                        URIs[links]=lineCount
                        output2=str(URIs[links])
                        lineCount=lineCount+1
                        
                        #create final output
                        if output1 and output2:
                            output=output+output1+"->"+output2+";"+"\n"
                x+=1
        print "Site:"
        print site
        print "links:"
        print output
        #write to file output
        graphviz.write(output)

#Create all ordered lables
t=OrderedDict(sorted(URIs.items(), key=lambda t: t[1]))
print "Lables="
for item in t.items():
    print str(item[1])+"[label="+item[0]+"]"
    graphviz.write(str(item[1])+"[label="+item[0]+"];\n")
graphviz.write("}")

print "dot file created!!Hoorayyyyyy"

#delet the dictionary
del URIs
#close file
graphviz.close()
