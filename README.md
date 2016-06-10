TwitterBot
Twitterbot script for a domoticz enabled twitter bot that listens to a domotica server owners twitter account
This script enables the user to manage a domotica domoticz server through twitter
It is written in python 2.7 for raspberry pi running raspberian
The bot talks to twitter's API using Twyhton and to the domoticz server API using JSON
It only responds to one twitter ID based on the twitterhandle of the servers twitter account and the control twitter account 
tweets from other users will be replied with some smart ass remarks telling them they are not allowed to controls by means of a return tweet.

The bot answers to its master in 3 ways:
  default reply - based on a '@Twitter_handle answer me' tweet
  Command tweet - based on tweets of your own choosing to the twitter handle of the domotica server
  invalid command tweet - all tweets that do not have a command specified to will recieve a reply from the bot that it does not understand the command.

It works quite well if configured correctly with built in avoidance for duplicate tweets.
It does not handle any errors very well at the moment may be for v x+ so make sure you follow the instructions commented in the code.


Prerequisites
What you need first is a twitter account for your domotica server
a twitter account that is able to send control commands (usually the servers owner)
and your own twitter application to connect to the twitter API(get it here: https://dev.twitter.com/)
Domoticz installed on a Paspberry Pi
Python 2.7
Twython
Drop the .py file and the textfile in a directory currently setup with  /home/pi/tweetbot/ as the folder but this can be altered by
editing the script

File description 
twitterbot.py = the bot's script
defaultresponselist.txt = a list of random default responses to the control account
InvalidCommandTweet.txt = random list of responses to invalid commands
notauthorizedtweet.txt  = random list of responses to metions of the server twitter accounts by accounts except the control account
pleasedtweetreply.txt =  random list of responses whenever you thank the servers twitter account





v0.1  is able to switch on\off lights, groups and scene's
handle incomming tweets from the master account 
handle incomming tweets from other account
restart domoticz
switch lights and groups in domoticz
