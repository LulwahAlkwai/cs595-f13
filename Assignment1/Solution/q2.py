#cs595
#Assignment1-q2
#Lulwah Alkwai
#!/usr/bin/python
import sys
import time
import urllib2
import BeautifulSoup

if len(sys.argv) == 4:
  InputTeamName=sys.argv[1]
  TimeInSeconds=int(sys.argv[2])
  URI=sys.argv[3]

#Handling exception
#Arguments not correctly inputed
#using default input

else:
  print('***********************************************************************************************')
  print('Please try again by entering: q2.py "TeamName" TimeInSeconds "URI"')
  print('	Default:')
  print('	Team Name: Old Dominion')
  print('	Time In Seconds: 60 ')
  print('	URI: http://scores.espn.go.com/ncf/scoreboard?confId=80&seasonYear=2013&seasonType=2&weekNumber=2')
  print('***********************************************************************************************')
  
  InputTeamName="Old Dominion"
  TimeInSeconds=60
  URI="http://scores.espn.go.com/ncf/scoreboard?confId=80&seasonYear=2013&seasonType=2&weekNumber=2"

condition = True
while condition:

    redditFile = urllib2.urlopen(URI)
    redditHtml = redditFile.read()
    redditFile.close();

    soup = BeautifulSoup.BeautifulSoup(redditHtml)
    
    for allteams in soup.findAll('a',{'title':InputTeamName}):
        game = allteams.findParent().findParent().findParent().findParent().findParent()

        Team1 = game.find('div', {"class":"team home"})  
	Team1Name = Team1.find('p', {"class":"team-name"}).find('a').string
        Team1Points = Team1.find('li', {"class":"final"}).string

        Team2 = game.find('div', {"class":"team visitor"})
        Team2Name = Team2.find('p', {"class":"team-name"}).find('a').string
        Team2Points = Team2.find('li', {"class":"final"}).string
        
	print(Team1Name + ' ' + Team1Points)
	print(Team2Name + ' ' + Team2Points)
	print('. . .')

    time.sleep(TimeInSeconds)