#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# James Geddes wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# James Geddes | GeekZone | hq@geekzone.org.uk | GeekZone.org.uk
# ----------------------------------------------------------------------------
#

import os
import time
import wave
import picamera
import RPi.GPIO as GPIO
import tweepy
import pygame
from subprocess import call
from datetime import datetime
import sys
import contextlib
from tweepy import OAuthHandler
os.system('clear')
GPIO.cleanup()
GPIO.setwarnings(False)

pygame.mixer.init()
c = pygame.mixer.Sound("thunderbirdscount.wav")
s = pygame.mixer.Sound("thunderbirdsarego.wav")
#w = pygame.mixer.Sound("welcome.wav")
deploy = pygame.mixer.Sound("Turret_turret_deploy_2.wav")
active = pygame.mixer.Sound("Turret_turret_deploy_4.wav")
hello = pygame.mixer.Sound("Turret_turret_active_5.wav")
speakertest = pygame.mixer.Sound("Turret_turretwitnessdeath13.wav")

fname = 'thunderbirdscount.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)
	#print(duration)
hello.play()
os.system('clear')
print("*** GeekZone Photobooth ***\n\n              ____\n         _[]_/____\__n_\n        |_____.--.__()_|\n        |[]  /    \    |\n        |    \ __ /    |\n        |     '--'     |\n        |______________|")
time.sleep(3)
os.system('clear')
print("Setup\n\n1. Please turn on the speaker")

speakerstate = input("Have your turned the speaker on?\n\n1 = yes\n0 = no\n\n")
while speakerstate < 1:
	os.system('clear')
	print("Playng speaker test...\n")
	speakertest.play()
	time.sleep(2)
	os.system('clear')
	speakerstate = input("Please turn the speaker on. If the speaker is on, you should have heard the speaker test\n\nHave your turned the speaker on?\n\n1 = yes\n0 = no\n\n")
os.system('clear')
print ("Sound system setup complete")
time.sleep(2)
os.system('clear')

## Operating mode allows you to select one of up to three twitter accounts to publish to at each runtime

print ("2. Please select operating mode\n1 = LIVE - GeekZone\n2 = LIVE - JamesGeddes\n3 = TEST - TestSandbox42\n")
opMode = input("Operating Mode: ")

if opMode == 1:
	# GeekZone Twitter - LIVE
	print "Now operating in mode: LIVE - GeekZone"
	consumer_key = 'xxx'		## Replace xxx with your code from dev.twitter.com
	consumer_secret = 'xxx'		## Replace xxx with your code from dev.twitter.com
	access_token = 'xxx'		## Replace xxx with your code from dev.twitter.com
	access_token_secret = 'xxx'     ## Replace xxx with your code from dev.twitter.com
elif opMode == 2:
	# JamesGeddes Twitter - LIVE
	print "Now operating in mode: LIVE - JamesGeddes"
        consumer_key = 'xxx'            ## Replace xxx with your code from dev.twitter.com
        consumer_secret = 'xxx'         ## Replace xxx with your code from dev.twitter.com
        access_token = 'xxx'            ## Replace xxx with your code from dev.twitter.com
        access_token_secret = 'xxx'     ## Replace xxx with your code from dev.twitter.com

elif opMode == 3:
	# TestSandbox42 Twitter - TEST
	print "Now operating in mode: TEST - TestSandbox42"
        consumer_key = 'xxx'            ## Replace xxx with your code from dev.twitter.com
        consumer_secret = 'xxx'         ## Replace xxx with your code from dev.twitter.com
        access_token = 'xxx'            ## Replace xxx with your code from dev.twitter.com
        access_token_secret = 'xxx'     ## Replace xxx with your code from dev.twitter.com

else:
	print "operating mode not selected"

time.sleep(3)
os.system('clear')

## Set content of tweet ##

print "3. Enter tweet text. This must be under 100 characters\n"

uiStatus = raw_input("Tweet text: ")

## check that tweet length is less than 100 chars. This allows space for image URL.

while len(uiStatus) > 100:
	print "\nTweet text must be 100 characters or shorter. You entered " + str(len(uiStatus)) + " characters"
	uiStatus = raw_input("Tweet text: ")

## Compile tweet and add a hashtag on to the end of the tweet

if opMode < 3:
	status = uiStatus + " " + chr(35) + "GeekZonePhotobooth"
else:
	status = uiStatus + " " + chr(35) + "HelloWorld"

print "\n\nTwitter Status set to: " + status
time.sleep(3)
os.system('clear')
print "Saving settings..."
deploy.play()
time.sleep(1)
os.system('clear')
raw_input("Setup complete. Press Enter to Load Photobooth...")
os.system('clear')
print "Photobooth Running\n\n"
active.play()
time.sleep(1)

os.system('clear')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

led = 18
switch = 17
count = 0
numdur = duration / 5
ledtime = numdur / 4

#Debuging maths printouts
#print "duration = " + str(duration)
#print "ledtime = " + str(ledtime)

GPIO.setmode(GPIO.BCM)
#GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(switch, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

GPIO.output(led, 1)

#prev_input = 0
os.system('clear')

## initilise camera ##
with picamera.PiCamera() as camera:


## start camera preview. ##

###########################
## does NOT record video ##
###########################

	camera.start_preview()


## main loop ##
	while True:
#		GPIO.output(led, 1)
### debounce the button press ###
		while True:
			time.sleep(0.1)
			os.system('clear')
			input_state = GPIO.input(switch)
			if input_state == False:
				break
#		GPIO.wait_for_edge(17, GPIO.FALLING)
#		w.play()
### play the count down sound ###
		c.play()
### flash the LED ###
		while count < 10:
			time.sleep(ledtime)
			GPIO.output(led, 0)
			time.sleep(ledtime)
        	        GPIO.output(led, 1)
			count = count + 1
			os.system('clear')
		s.play()
## reset the counter ##
		count = 0
## flash the LED faster to indicate imminent image capture ##
                while count < 10:
                        time.sleep(0.1)
                        GPIO.output(led, 0)
                        time.sleep(0.1)
                        GPIO.output(led, 1)
                        count = count + 1
                        os.system('clear')
## reset counter ##
		count = 0
## set time strings to current values ##
		hnow = time.strftime("%H")
		minnow = time.strftime("%M")
		snow = time.strftime("%S")
		dnow = time.strftime("%d")
		monow = time.strftime("%m")
		ynow = time.strftime("%Y")
## set image name to include datetime stamp for uniqueness - prevents over writing ##
		imgname = str("D" + dnow + "M" + monow + "Y" + ynow + "--H" + hnow + "M" + minnow + "S" + snow + ".jpg")
## capture the image with the camera  ##
		camera.capture('/home/pi/captures/photobooth-' + imgname)
#		camera.capture('/home/pi/Desktop/image.jpg')
		# Send the tweet with photo  
		photo_path = '/home/pi/captures/photobooth-' + imgname
		api.update_with_media(photo_path, status=status)
		os.system('clear')
		time.sleep(0.5)
#		GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)
		

#except KeyboardInterrupt:  
#	GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
#GPIO.cleanup()           # clean up GPIO on normal exit
