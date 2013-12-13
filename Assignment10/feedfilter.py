import feedparser
import re
import math

# Takes a filename or URL of a blog feed and classifies the entries
def read(feed,classifier):

    # Get feed entries and loop over them
    f=feedparser.parse(feed)
    print
    print '-----'
    #take first 10
    for entry in f['entries'][0:10]:
 
        # Print the contents of the entry
        title=entry['title'].encode('utf-8').replace("'","")
        # print 'Publisher: '+entry['publisher'].encode('utf-8')
        print 'Title:     '+ title
        print entry['summary'].encode('utf-8')
        
        # Combine all the text to create one item for the classifier
        #fulltext='%s\n%s\n%s' %(entry['title'],entry['publisher'],entry['summary'])
        fulltext='%s\n%s' % (entry['title'],entry['summary'])
        
        # Print the best guess at the current category
        predicted=str(classifier.classify(fulltext))
        print 'Predicted category: ', predicted
        
        # Ask the user to specify the correct category and train on that
        actual=raw_input('Actual category: ')
        feature=None
        cp=None
        classifier.train(fulltext, actual)

        print 'title: ', title
        print 'feature: ', feature
        print 'predicted ', predicted
        print 'actual', actual
        print 'cp', str(cp)

    print '----- '
    # Get feed entries and loop over them
    #f=feedparser.parse(feed)
    for entry in f['entries'][10:20]:

        # Print the contents of the entry
        title=entry['title'].encode('utf-8').replace("'","")
        print 'Title:     '+ title
        print entry['summary'].encode('utf-8')
        
        # Combine all the text to create one item for the classifier
        #fulltext='%s\n%s\n%s' %(entry['title'],entry['publisher'],entry['summary'])
        fulltext='%s\n%s' % (entry['title'],entry['summary'])
        fulltext=fulltext.replace("'","")
        # Print the best guess at the current category
        predicted=str(classifier.classify(fulltext))
        print 'Predicted: ', predicted
        
        # Ask the user to specify the correct category
        actual=raw_input('Enter actual category: ')
        feature=raw_input('Enter string feature: ')
        
        # probability the item should be in this category
        cp=round(classifier.cprob(feature,predicted),3)
  
        print 'title: ', title
        print 'feature: ', feature
        print 'predicted ', predicted
        print 'actual', actual
        print 'cp', str(cp)

#return classifier

def entryfeatures(entry):
    splitter=re.compile('\\W*')
    f={}
    
    # Extract the title words and annotate
    titlewords=[s.lower() for s in splitter.split(entry['title'])
                if len(s)>2 and len(s)<20]
    for w in titlewords: f['Title:'+w]=1
                
    # Extract the summary words
    summarywords=[s.lower() for s in splitter.split(entry['summary'])
                if len(s)>2 and len(s)<20]
                              
    # Count uppercase words
    uc=0
    for i in range(len(summarywords)):
        w=summarywords[i]
        f[w]=1
        if w.isupper(): uc+=1
                                  
    # Get word pairs in summary as features
    if i<len(summarywords)-1:
        twowords=' '.join(summarywords[i:i+1])
        f[twowords]=1
                              
    # Removed: Keep creator and publisher whole
    #f['Publisher:'+entry['publisher']]=1
                              
    # UPPERCASE is a virtual word flagging too much shouting
    if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
                              
    return f