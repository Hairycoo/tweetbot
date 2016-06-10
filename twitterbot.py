#!/usr/bin/env python
# ==================================================================================
# ==== script for a domoticz enabled tweet bot that listens to a domotica owner
# ==== Built for RasPi with Raspberian
# ====  version: v0.1
# ==== Developed by Webgnome aka Hairycoo
# ==================================================================================

# imports
# ==================================================================================
import sys, os, string, datetime, subprocess, json, httplib, urllib, urllib2, base64   

from twython import Twython
from twython import TwythonStreamer
from twython import TwythonError

import random  # this one gaver me so much trouble
print 'importing Python libraries...' #loaded needed libs
#key stuff needed for the api call to twython
# ==================================================================================
CONSUMER_KEY = '<TWITTER API CONSUMER KEY HERE>'
CONSUMER_SECRET = '<TWITTER API CONSUMER SECRET HERE> '
ACCESS_KEY = '<TWITTER API ACCES KEY HERE>'
ACCESS_SECRET = '<TWITTER API ACCESS SECRET HERE>'
#set twython params
# ==================================================================================
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

print 'twitter API values loaded...' #we loaded the API values here

#Set variables for the bot
# ===================================================================================

DefaultTweetReply ='I obey your command master'
NotAuthorizedTwitterResponse ='I only obey my master'
InvalidCommandTweetResponse = 'I am sorry master but I do not understand'  

streamfilter = '<YOUR TWITTERBOT TWITTER HANDLE HERE>'
BotsTwitterId = '<YOUR TWITTERBOT TWITTER HANDLE HERE>'
MastersTwitterHandle ='<YOUR CONTROL TWITTER ACCOUNT HANDLE HERE>'
MastersTwitterId = '<YOUR CONTROL ACCOUNT TWITTER ID HERE>' #You can find it by typing your twitter username here

print 'Twitter API values loaded...' #we loaded the API values here
#key stuff needed for the api call to domoticz
# ==================================================================================

DomoticzServer = '<DOMOTICZ SERVER:PORT>' #servername + port eg 127.0.0.1:8080
DomoticzUsername = '<DOMOTICZ USER>' # always try to create a system user for security
DomoticzPassword = '<DOMOTICZ USER PASSWORD>' #the sys users password
# ==================================================================================

base64string = base64.encodestring('%s:%s' % (DomoticzUsername, DomoticzPassword)).replace('\n', '')
DomoticzUrl = 'http://'+DomoticzServer


#Set variables for the bot
# ===================================================================================

DefaultTweetReply ='I obey your command master'
NotAuthorizedTwitterResponse ='I only obey my master'
InvalidCommandTweetResponse = 'I am sorry master but I do not understand'  

streamfilter = '<DOMOTICA SERVER TWITTER HANDLE>'
BotsTwitterId = '<DOMOTICA SERVER TWITTER HANDLE>'
MastersTwitterHandle ='<CONTROL ACCOUNT TWITTER HANDLE>'
MastersTwitterId = '<CONTROL ACCOUNT TWITTER ID'# can be fould here: http://mytwitterid.com/

#DON'T touch these variables
DefaultResponses = []
NotAuthorizedTwitterResponses = []
InvalidCommandTweetResponses = []
pleasedTweetReplies = []

# File locations
# ===================================================================================
# The below files can be edited to change tweet responses 
# CAUTION the below files should not be to short and contain no empty lines or the bot might crash
#====================================================================================
DefaultResponseFile='/home/pi/tweetbot/defaultresponselist.txt'
NotAuthorizedTwitterHandleFile='/home/pi/tweetbot/notauthorizedtweet.txt'
InvalidCommandTweetResponseFile='/home/pi/tweetbot/InvalidCommandTweet.txt'
pleasedTweetReplyFile='/home/pi/tweetbot/pleasedtweetreply.txt'
#====================================================================================
#LogOutputFile ='/var/log/tweetbot.log' #Future function

print 'variables and file locations loaded....' #message that the bot has loaded all till now

# ===================================================================================
# ===== some functions to reduce the ammount of code
# ===================================================================================

# File load into an array
# ==================================================================================
def LoadList(FileName,Array):
	with open(FileName, "r") as ins:
		for line in ins:
			Array.append(line)
			
		ins.close
# get the current system time always a nice to have
# ===================================================================================
def GetTime():
	CurrentTimeDate = datetime.datetime.now()
	return CurrentTimeDate

# ===================================================================================
# ======== Domoticz functions & Classes
# ===================================================================================

def open_port():
    pass

def close_port():
    pass
# basic on/off switch for domoticz based on the domoticz XID value in devices
# ==================================================================================
class DomoticzOnOffSwitch():
    
	def __init__(self, url):
        
		self.baseurl = url
        
	def __execute__(self, url):

		req = urllib2.Request(url)
		return urllib2.urlopen(req, timeout=5)
       
	def SwitchOn(self, xid):
		"""
		Get the Domoticz device information.
		"""
		url = "%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=On" % (self.baseurl, xid)
		data = json.load(self.__execute__(url))
		return data

	def SwitchOff(self, xid):
		"""
		Get the Domoticz device information.
		"""
		url = "%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=Off" % (self.baseurl, xid)
		data = json.load(self.__execute__(url))
		return data

	def GroupOn(self, xid):
		"""
		Get the Domoticz device information.
		"""
		url = "%s/json.htm?type=command&param=switchscene&idx=%s&switchcmd=On" % (self.baseurl, xid)
		data = json.load(self.__execute__(url))
		return data
		
	def GroupOff(self, xid):
		"""
		Get the Domoticz device information.
		"""
		url = "%s/json.htm?type=command&param=switchscene&idx=%s&switchcmd=Off" % (self.baseurl, xid)
		data = json.load(self.__execute__(url))
		return data

	
# ===================================================================================
# ====  the bots main routine
# ===================================================================================
print "loading main classes..."	
class MyStream(TwythonStreamer):
		
	# Load list of default responses from file
	# ===============================================================================
	print 'loading default responses for bot' #This is where we are loading the script
	#with open(DefaultResponseFile, "r") as ins:
	#	for line in ins:
	#		DefaultResponses.append(line)
			
	#	ins.close
	# load responses to avoid duplicate messages on twitter
	dummy=LoadList(DefaultResponseFile,DefaultResponses)
	#for word in DefaultResponses:
	#	print word
	dummy=LoadList(NotAuthorizedTwitterHandleFile,NotAuthorizedTwitterResponses)
	dummy=LoadList(DefaultResponseFile,DefaultResponses)
	dummy=LoadList(InvalidCommandTweetResponseFile,InvalidCommandTweetResponses)
	dummy=LoadList(pleasedTweetReplyFile,pleasedTweetReplies)
	# ===============================================================================
	
	def on_success(self, data):
                # Recycle default response
				# ===================================================================
				random.seed()
				randnr=random.randrange(0,len(DefaultResponses))
				DefaultTweetReply = DefaultResponses[randnr]
				random.seed()
				randnry=random.randrange(0,len(NotAuthorizedTwitterResponses))
				NotAuthorizedTwitterResponse = NotAuthorizedTwitterResponses[randnry]
				random.seed()
				randnri=random.randrange(0,len(InvalidCommandTweetResponses))
				InvalidCommandTweetResponse = InvalidCommandTweetResponses[randnri]
				random.seed()
				randnrj=random.randrange(0,len(pleasedTweetReplies))
				pleasedTweetReply=pleasedTweetReplies[randnrj]

				if 'text' in data:
					#debug info
					# ===============================================================
					tweetpayload=data['text'].encode('utf-8') 
					tweet=data['id_str'].encode('utf-8')
					friend=data['user']['id_str'].encode('utf-8')
					isretweet=data['retweeted']	
					istweetfriendscreenname=data['user']['screen_name'].encode('utf-8')
					#tweetsender=data['from_user'].encode('utf-8')
					#print 'tweet full payload: %r' % data
					#print 'tweet id: %r' % tweet
					#print 'friend id: %r'% friend
					#print istweetfriendscreenname
					# end debug stuff
					now=GetTime()
					timevar = now.strftime("%Y-%m-%d %H:%M:%S") #get current time stats for logging
					print '%s : Message: %r' % (timevar,tweetpayload) # print tweet for logging purposes 
					#check if the master is tweeting
					if MastersTwitterId in friend:
						# ======================================================================================================================
						# =========   Twitter commands 
						#=======================================================================================================================
						# To remove commands remove an elif section
						# To create a new one see the commented example right here:
						#
						#elif '<TEXT TO WATCH FOR IN TWEET>' in tweetpayload:
						#   <ENTER COMMAND TO DO HERE>
						#	timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
						#	print '%s : <LOG ENTRY FOR COMMAND>' % timevar
						#	response= '<RETURN TWEET TEXT>, %s %s at %s' % (DefaultTweetReply,MastersTwitterHandle,timevar)
						#	api.update_status(status=response)	
						#
						#
						#=========================================================================================================================
						#
						#check if twitter id called then do a default response to master twitterhandle
						DefaultTwitterCommand = '%s answer me' % BotsTwitterId 
						if DefaultTwitterCommand in tweetpayload:
							timevar = now.strftime("%Y-%m-%d %H:%M")
							print '%s : Returning response to master' % timevar
							DefaultTweetReply= '%s %s' % (DefaultTweetReply, MastersTwitterHandle)
							api.update_status(status=DefaultTweetReply)
						#now ask the bot to start a command based on a string text in a tweet
						#====================================================================
						elif '<COMMAND TO RESTART DOMOTICA DEAMOM>' in tweetpayload:
							#log the order
							timevar = now.strftime("%Y-%m-%d %H:%M:%S")
							print '%s : Executing command sent by twitter' % timevar
							p=subprocess.Popen(['sudo','/etc/init.d/domoticz.sh','restart'])#change path if this is not your default location
							now=GetTime()
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Returning response to master' % timevar
							DefaultTweetReply= 'Executing, %s %s' % (DefaultTweetReply,MastersTwitterHandle)
							api.update_status(status=DefaultTweetReply)
						# example commands
						#light switch casper bedroom	
						elif '<YOUR TWITTERHANDLE> bedroom light on' in tweetpayload:
							cmdresult= DomoticzOnOffSwitch(DomoticzUrl).SwitchOn(<YOUR DOMOTICA DEVICE IDX>) #call to Domoticz
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Light Casper on. Result:%s. Returning reply' % (timevar,cmdresult)
							DefaultTweetReply= 'Executing at: %s, Casper light on, %s %s' % (timevar,DefaultTweetReply,MastersTwitterHandle)
							api.update_status(status=DefaultTweetReply)
							
						elif '<YOUR TWITTERHANDLE> bedroom light off' in tweetpayload:
							cmdresult= DomoticzOnOffSwitch(DomoticzUrl).SwitchOff(<YOUR DOMOTICA DEVICE IDX>) #call to domoticz
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Light Casper off. Result:%s. Returning reply' % (timevar,cmdresult)
							DefaultTweetReply= 'Executing at: %s, Casper light off, %s %s' % (timevar,DefaultTweetReply,MastersTwitterHandle)
							api.update_status(status=DefaultTweetReply)
						
						#all light switches		
						elif '<YOUR TWITTERHANDLE> light the house' in tweetpayload:
							cmdresult= DomoticzOnOffSwitch(DomoticzUrl).GroupOn(<YOUR DOMOTICA GROUP DEVICE IDX>) #call to domoticz
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Returning response to master. Result:%s - all lights on' % (timevar,cmdresult)
							DefaultTweetReply= 'Lighting the house, %s %s at %s' % (DefaultTweetReply,MastersTwitterHandle,timevar)
							api.update_status(status=DefaultTweetReply)
							
						elif '<YOUR TWITTERHANDLE> darken the house' in tweetpayload:
							cmdresult= DomoticzOnOffSwitch(DomoticzUrl).GroupOff(<YOUR DOMOTICA GROUP DEVICE IDX>) #call to domoticz
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Returning response to master. Result:%s - all lights off' % (timevar,cmdresult)
							DefaultTweetReply= 'Turning the house to darkness, %s %s at %s' % (DefaultTweetReply,MastersTwitterHandle,timevar)
							api.update_status(status=DefaultTweetReply)
						
							
						# ====================================================================================================================
						# thank you responses
						# ====================================================================================================================
						elif '<YOUR TWITTERHANDLE> good job' in tweetpayload:
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Returning response to master - thanks' % timevar
							response= '%s %s at %s' % (pleasedTweetReply,MastersTwitterHandle,timevar)
							api.update_status(status=response)
							
						elif '<YOUR TWITTERHANDLE> thank' in tweetpayload:
							timevar = now.strftime("%Y-%m-%d %H:%M:%S") # get the time after execution of command
							print '%s : Returning response to master - thanks' % timevar
							response= '%s %s at %s' % (pleasedTweetReply,MastersTwitterHandle,timevar)
							api.update_status(status=response)	
							
						# =====================================================================================================================	
						# if command is not understood return an reply that tweetbot did not understand
						# =====================================================================================================================
						else:
							print '%s : Invalid command by master,returning response ' % timevar
							response='%s %s at %s'  % (timevar,InvalidCommandTweetResponse,MastersTwitterHandle)
							api.update_status(status=response)
					# =========================================================================================================================
					# =====  If not authorised respond to tweeter
					# =========================================================================================================================			
					else: 
						now=GetTime()
						timevar = now.strftime("%Y-%m-%d %H:%M:%S") #get current time stats for logging
						print '%s : Tweet not sent by authorised user , Replying with a default reply' % timevar
						response=' %s @%s' % (NotAuthorizedTwitterResponse,istweetfriendscreenname)
						api.update_status(status=response)
		# =====================================================================================================================================
		# ====== on error
		#======================================================================================================================================
	def on_error(self, status_code, data):
		now=GetTime()
		timevar = now.strftime("%Y-%m-%d %H:%M:%S") #get current time stats for logging
		print '%s : error in stream: %r' % (timevar,status_code)
		# Want to stop trying to get data because of the error?
        # Uncomment the next line! 
        # self.disconnect()
# ====================================================================================

		
# =====================================================================================
# ===== execute stuff
# =====================================================================================	

print 'loaded bot succesfully checking twitter chatter now....' #so you know it is running
try:
	streamer = MyStream(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) #listen to twitterchatter 		
		
	streamer.statuses.filter(track=streamfilter) #master filter for tweets	
	
except TwythonError as e:
	now=GetTime()
	timevar = now.strftime("%Y-%m-%d %H:%M:%S") #get current time stats for logging
	pass
	