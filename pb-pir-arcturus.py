'''
========================================
Arcturus : Garage Bouncer
========================================

# Author: @bencarpena

# Workflow: Level 1 AI Sense + Respond
[+]   Sense : detect movements + convert analog signal to digital
[+]   Respond : turn on lights via API + take photo and upload to Slack

# Change log:
@bencarpena:
    #       20190909 :	Initial setup; no LED; set sleep to 2 from 0.1
    #		20190909 :	Added Slack post feature and PIR
    #		20191024 :	Added subroutine for capturing images every motion is detected 
    # 		20200528 : 	Added try - catch exception 	
    # 		20210104 :	Enhance try catch, addressed asyncio error in Slack	
    # 		20210224 :	Added Hue light integration		
    #		20210226 :	Fine tuned exception handling; added catch all
    #		20210227 :	Added assertion at response_hue
    #		20210309 :	Changed Hue IP address


'''


import RPi.GPIO as GPIO
import time
import datetime

import requests
import json
import os, ssl
import slack
import sys

from slack import WebClient

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

webhook_url = 'https://hooks.slack.com/services/slack_token_here'

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
			ssl._create_default_https_context = ssl._create_unverified_context

try:
	while True:
		i=GPIO.input(11)
		if i==0:                 #When output from motion sensor is LOW
			print ("arcturus (iothub bypass) | PIR Motion sensor : No movement", i)
			time.sleep(1.5)
		elif i==1:               #When output from motion sensor is HIGH
			print ("arcturus (iothub bypass) | PIR Motion sensor : Movement detected ", datetime.datetime.now())
			slack_msg = {'text' : 'arcturus (iothub bypass) | PIR Motion sensor : Movement detected ' + str(datetime.datetime.now())}
			requests.post(webhook_url, data=json.dumps(slack_msg))
			time.sleep(0.5)

			# --- Turn on lights for extra lighting ---
			url = "http://huebridge_here/api/inline_token_here/lights/8/state"
			payload = "{\"on\":true, \"bri\":254}"
			headers = {
			'Content-Type': 'text/plain'
			}
			response_hue = requests.request("PUT", url, headers=headers, data = payload)
			assert response_hue.status_code == 200 
			time.sleep(1)

			import datetime
			import slack
			from slack import WebClient
			client = slack.WebClient('xoxb-xxxxxx-xxx-xxxxxxxxxx')
			TakePic = 'raspistill -o /home/pi/Scripts/Camera/77389-garage.jpg -ISO 200 -ev 10'
			os.system(TakePic)
			response = client.files_upload(
			channels='#cvx-iot-arcturus',
			file="/home/pi/Scripts/Camera/77389-garage.jpg",
			media="file",
			initial_comment="movement screenshot : " + str(datetime.datetime.now()))
			assert response["ok"]
			
			time.sleep(1.5)

			# --- Turn off lights  ---
			#print("Lights should be off by now") #debug only
			url = "http://huebridge_here/api/inline_token_here/lights/8/state"
			payload = "{\"on\":false, \"bri\":254}"
			headers = {
			'Content-Type': 'text/plain'
			}
			response_hue = requests.request("PUT", url, headers=headers, data = payload)
			assert response_hue.status_code == 200 


except SlackApiError as e:
	slack_msg = {'text' : 'arcturus (iothub bypass) | PIR Motion sensor : Slack API exception occurred : ' + str(datetime.datetime.now()) + " | " + str(e)}
	requests.post(webhook_url, data=json.dumps(slack_msg))
	raise e
except:
	err = sys.exc_info()[0]
	slack_msg = {'text' : 'arcturus (iothub bypass) | Exception occurred : ' + str(datetime.datetime.now()) + " | " + str(err)}
	requests.post(webhook_url, data=json.dumps(slack_msg))
	raise
finally:
	# --- Turn off lights  ---
	#print("'Finally reached': Lights should be off by now") #debug only
	url = "http://huebridge_here/api/inline_token_here/lights/8/state"
	payload = "{\"on\":false, \"bri\":254}"
	headers = {
	'Content-Type': 'text/plain'
	}
	response_hue = requests.request("PUT", url, headers=headers, data = payload)
	assert response_hue.status_code == 200 
	#print("Healing now...") #debug only
	os.execv(__file__, sys.argv) #20200605 : Heal process and restart
