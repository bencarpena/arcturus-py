#!/usr/bin/python
#--------------------------------------
# Edited and enhanced  	: @bencarpena
#      
#	Script Notes: 
#		20190909 :	Initial setup; no LED; set sleep to 2 from 0.1
#		20190909 :	Added Slack post feature and PIR
#		20191024 :	Added subroutine for capturing images every motion is detected 
# 		20200528 : 	Added try - catch exception 				
#--------------------------------------

import RPi.GPIO as GPIO
import time
import datetime

import requests
import json
import os, ssl
import slack
import sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

webhook_url = 'https://hooks.slack.com/services/yourwebhookhere'

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
			ssl._create_default_https_context = ssl._create_unverified_context

try:
	while True:
		i=GPIO.input(11)
		if i==0:                 #When output from motion sensor is LOW
			print ("arcturus (iothub bypass) | PIR Motion sensor : No movement", i)
			time.sleep(2.5)
		elif i==1:               #When output from motion sensor is HIGH
			print ("arcturus (iothub bypass) | PIR Motion sensor : Movement detected ", datetime.datetime.now())
			slack_msg = {'text' : 'arcturus (iothub bypass) | PIR Motion sensor : Movement detected ' + str(datetime.datetime.now())}
			requests.post(webhook_url, data=json.dumps(slack_msg))
			time.sleep(0.5)


			from slack import WebClient
			client = slack.WebClient('xoxb-yourSlackTOKENhere')
			TakePic = 'raspistill -o /home/pi/Scripts/Camera/77389-garage.jpg -ISO 200 -ev 10'
			os.system(TakePic)
			response = client.files_upload(
			channels='#cvx-iot-arcturus',
			file="/home/pi/Scripts/Camera/77389-garage.jpg")
			assert response["ok"]

except:
            slack_msg = {'text' : 'arcturus (iothub bypass) | PIR Motion sensor : Exception occurred [TakePic]! ' + str(datetime.datetime.now())}
            requests.post(webhook_url, data=json.dumps(slack_msg))
            os.execv(__file__, sys.argv) #20200605 : Heal process and restart

time.sleep(2.5)
