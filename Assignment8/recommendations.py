#CS595
#Assignment8
#Lulwah Alkwai
#!/usr/bin/python

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}
#
#
#The original code includes:
#
#def sim_distance(prefs,person1,person2):                    # Returns a distance-based similarity score for person1 and person2
#def sim_pearson(prefs,p1,p2):                               # Returns the Pearson correlation coefficient for p1 and p2
#def topMatches(prefs,person,n=5,similarity=sim_pearson):    # Returns the best matches for person from the prefs dictionary.
#def getRecommendations(prefs,person,similarity=sim_pearson):# Gets recommendations for a person by using a weighted average
#def transformPrefs(prefs):
#def calculateSimilarItems(prefs,n=10):                      # Create a dictionary of items showing which other items they are most similar to.
#def getRecommendedItems(prefs,itemMatch,user):
#def loadMovieLens(path='/Users/kka55/Desktop/Assignment8/data/movielens'):
#
#

from math import sqrt
import math
users={}

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)
  
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens(path='/Users/kka55/Desktop/Assignment8/data/movielens'):
  global users
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)

  #*We need to Load /u.user
  
  for line in open(path+'/u.user'):
    (user,age,gender,occupation,zipCode)=line.split('|')
    users[user]=(user,age,gender,occupation,zipCode)
  return prefs

#1.  What 5 movies have the highest average ratings? Show the movies
#    and their ratings sorted by their average ratings.
print "1.  What 5 movies have the highest average ratings? Show the movies and their ratings sorted by their average ratings.\n"

#Create movies data
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    for movie in prefs[u].keys():
        if not movie in Allmovies:
           Allmovies[movie]=[]
        Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total = total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
      av=item[1]
    if item[1]==av:
      print item
    count=count+1

print "\n"

#2.  What 5 movies received the most ratings? Show the movies and
#    the number of ratings sorted by number of ratings.

print "2.  What 5 movies received the most ratings? Show the movies and the number of ratings sorted by number of ratings.\n"

#Create movies data
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    for movie in prefs[u].keys():
        if not movie in Allmovies:
            Allmovies[movie]=[]
        Allmovies[movie].append(prefs[u][movie])

#Calculate the most rating
for movie in Allmovies.keys():
    Allmovies[movie]=len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get top 5 from list
count=1
for item in s:
    if count<=5:
        print str(count)+"- "+str(item)
    count=count+1

print "\n"

#3.  What 5 movies were rated the highest on average by women? Show
#    the movies and their ratings sorted by ratings.

print "3.  What 5 movies were rated the highest on average by women? Show the movies and their ratings sorted by ratings.\n"

#Create movies data
#Save data if gender is (F) female
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    if userGender=='F':
        for movie in prefs[u].keys():
          if not movie in Allmovies:
            Allmovies[movie]=[]
          Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
       total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"

#4.  What 5 movies were rated the highest on average by men? Show
#    the movies and their ratings sorted by ratings.

print "4.  What 5 movies were rated the highest on average by men? Show the movies and their ratings sorted by ratings.\n"

#Create movies data
#Save data if gender is (M) male
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    if userGender=='M':
        for movie in prefs[u].keys():
            if not movie in Allmovies:
                Allmovies[movie]=[]
            Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"

#5.  What movie received ratings most like Top Gun? Which movie
#    received ratings that were least like Top Gun (negative correlation)?

print "5.  What movie received ratings most like Top Gun?\n"

#Code from: calculateSimilarItems(prefs,n=10):

# Create a dictionary of items showing which other items they
# are most similar to.
result={}
# Invert the preference matrix to be item-centric
itemPrefs=transformPrefs(prefs)
c=0
for item in itemPrefs:
        # Status updates for large datasets
        c+=1
        #if c%100==0: print "%d / %d" % (c,len(itemPrefs))
        # Find the most similar items to this one
        scores=topMatches(itemPrefs,"Top Gun (1986)",n=10,similarity=sim_pearson)
        result[item]=scores

#Extract the movie with rating most like "Top Gun (1986)"
print result["Top Gun (1986)"][0][1]

print "\n"

print "Part2-5.  Which movie received ratings that were least like Top Gun (negative correlation)?\n"

#Code from: calculateSimilarItems(prefs,n=10):

# Create a dictionary of items showing which other items they
# are most similar to.
result={}
# Invert the preference matrix to be item-centric
itemPrefs=transformPrefs(prefs)
c=0
for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    #if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,"Top Gun (1986)",n=1664,similarity=sim_pearson)
    result[item]=scores

#Extract the movie with rating least like "Top Gun (1986)"
print result["Top Gun (1986)"][-1][1]
print "\n"

#6.  Which 5 raters rated the most films? Show the raters' IDs and
#    the number of films each rated.

print "6.  Which 5 raters rated the most films? Show the raters' IDs and the number of films each rated.\n"

#Calculate number of ratings for each user
UserRates={}
for u in prefs.keys():
    UserRates[u]=len(prefs[u])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(UserRates.items(), key=lambda x: x[1], reverse=True)

#Get top 5 from list
count=1
for item in s:
    if count<=5:
        print str(count)+"- "+str(item)
    count=count+1
print "\n"


#7.  Which 5 raters most agreed with each other? Show the raters'
#    IDs and Pearson's r, sorted by r.

print "7.  Which 5 raters most agreed with each other? Show the raters IDs and Pearson's r, sorted by r.\n"
#This part takes forevvvvvvver on my computer to run
#so I uploaded all the result in a file
#so I can take whatever result needed for Q8

file1=open("Q7.txt","w")
#Create movies data
Allmovies={}
prefs=loadMovieLens()

SimScore=[]
for u in prefs.keys():
    for x in prefs.keys():
        if u != x:
            Sim=sim_pearson(prefs,u,x)
            if (x,u,Sim) not in SimScore:
                    SimScore.append((u,x,Sim))
                    file1.write(u+","+x+","+str(Sim)+"\n")
s=sorted(SimScore, key=lambda x: x[2])


count=0
for i in s:
    if count<6:
        if i[2]=="1.0":
            print i
            count=count+1

print "\n"
file1.close()

'''
#for testing purpuse I use this part

file2=open("Q7m.txt","r")

d_list = [line.strip() for line in open("Q7m.txt")]
d_list.sort(key = lambda line: line.split(",")[-1])
d_list.reverse()

count=0
for i in d_list:
    if count<6:
      if i[2]=="1":
       print i
       count=count+1
'''

#8.  Which 5 raters most disagreed with each other (negative
#    correlation)? Show the raters' IDs and Pearson's r, sorted by r.

print "8.  Which 5 raters most disagreed with each other (negative correlation)? Show the raters' IDs and Pearson's r, sorted by r.\n"

#s is from question7

count=0
for i in s:
    if count<6:
      if i[2]=="-1.0":
        print i
        count=count+1
print "\n"

#9.  What movie was rated highest on average by men over 40? By men
#    under 40?

print "9.  What movie was rated highest on average by men over 40?\n"

#Create movies data
#Save data if gender is (M) male
#And age>40
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    userAge=int(users[u][1])
    if userGender=='M' and userAge>40:
        for movie in prefs[u].keys():
            if not movie in Allmovies:
                Allmovies[movie]=[]
            Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"


print "Part2-9.  By men under 40?\n"

#Create movies data
#Save data if gender is (M) male
#And age<40
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    userAge=int(users[u][1])
    if userGender=='M' and userAge<40:
        for movie in prefs[u].keys():
            if not movie in Allmovies:
                Allmovies[movie]=[]
            Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"


#10. What movie was rated highest on average by women over 40? By
#    women under 40?

print "10. What movie was rated highest on average by women over 40? \n"

#Create movies data
#Save data if gender is (F) female
#And age>40
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    userAge=int(users[u][1])
    if userGender=='F' and userAge>40:
        for movie in prefs[u].keys():
            if not movie in Allmovies:
                Allmovies[movie]=[]
            Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"

print "Part2-10.  By women under 40?\n"

#Create movies data
#Save data if gender is (F) female
#And age<40
Allmovies={}
prefs=loadMovieLens()
for u in prefs.keys():
    userGender=users[u][2]
    userAge=int(users[u][1])
    if userGender=='F' and userAge<40:
        for movie in prefs[u].keys():
            if not movie in Allmovies:
                Allmovies[movie]=[]
            Allmovies[movie].append(prefs[u][movie])

#Calculate average rating
for movie in Allmovies.keys():
    total=0
    for AverageRating in Allmovies[movie]:
        total=total+AverageRating
    Allmovies[movie]=total/len(Allmovies[movie])

#Sort items and reverse them
#http://docs.python.org/2/howto/sorting.html
s=sorted(Allmovies.items(), key=lambda x: x[1], reverse=True)

#Get movies with highset average from list
#Assume highest is the first and take all equal values
count=0
for item in s:
    if count==0:
        av=item[1]
    if item[1]==av:
        print item
    count=count+1

print "\n"
