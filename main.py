# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
import time
from time import sleep
import Adafruit_DHT
import httplib, urllib2
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("digitalelectronicssir@gmail.com", "anwar2911")

DEBUG = 1
# Setup the pins we are connect to
RCpin = 24 # yellow
DHTpin = 4 # orange
vib = 23 
buzzer=18
fault1=16
fault2=20
fault3=21
#Setup our API and delay
myAPI = "YQVBBMFTR1GVTY7G"
myDelay = 10 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
GPIO.setup(fault1, GPIO.IN)
GPIO.setup(fault2, GPIO.IN)
GPIO.setup(fault3, GPIO.IN)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(vib, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer,GPIO.OUT)

#GPIO.setup for sensor (pin 4) is defined inside Adafrut_DHT library

def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+28
   
    # return dict
    return (str(RHW), str(TW),str(TWF))

def RCtime(RCpin):
    LT = 0
    
    if (GPIO.input(RCpin) == True):
        LT += 1
    return (str(LT))

def viberation(vib):
    VB = 0
    
    if (GPIO.input(vib) == True):
        VB += 1
    return (str(VB))  
  
# main() function
def main():
    
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            RHW, TW, TWF = getSensorData()
            LT = RCtime(RCpin)
	    VB = viberation(vib)
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s" % (TW, TWF, RHW, LT, VB))
	    #print f.read()
            print "Temp in C: "+ TW + " Temp in F: " + TWF+ " Humidity: " + RHW + " Light: " + LT + " Vibration: "+ VB
	    f.close()
	    #print TW
	    if TW=='29.0':
		print 'please wait sending Email alert for temperature rised'
	    	server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("digitalelectronicssir@gmail.com", "anwar2911")
		msg = "Temperature is above thershold level!"
		server.sendmail("digitalelectronicssir@gmail.com", "shaik.anwar10@gmail.com", msg)
		server.quit()
		print 'email send'
            	# f.close()
	    elif LT=='1':
		GPIO.output(buzzer,1)
		time.sleep(2)
		GPIO.output(buzzer,0)
		print'Please wait sending Email alert for No Light'
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("digitalelectronicssir@gmail.com", "anwar2911")
		msg = "No ligt in the working Area!"
                server.sendmail("digitalelectronicssir@gmail.com", "shaik.anwar10@gmail.com", msg)
                server.quit()
                print 'email send'
	    if GPIO.input(fault1)== 1:
                GPIO.output(buzzer,1)
                time.sleep(2)
                GPIO.output(buzzer,0)
                print'Please wait f1 gone wrong sending email'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("digitalelectronicssir@gmail.com", "anwar2911")
                msg = "Machine1 gone fault!"
                server.sendmail("digitalelectronicssir@gmail.com", "shaik.anwar10@gmail.com",msg)
                server.quit()
                print 'email send'
	    if GPIO.input(fault2)== 1:
                GPIO.output(buzzer,1)
                time.sleep(2)
                GPIO.output(buzzer,0)
                print'Please wait f2 gone wrong sending email'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("digitalelectronicssir@gmail.com", "anwar2911")
                msg = "Machine2 gone fault!"
                server.sendmail("digitalelectronicssir@gmail.com", "shaik.anwar10@gmail.com", msg)
                server.quit()
                print 'email send'
	    if GPIO.input(fault3)== 1:
                GPIO.output(buzzer,1)
                time.sleep(2)
                GPIO.output(buzzer,0)
                print'Please wait f3 gone wrong sending email'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("digitalelectronicssir@gmail.com", "anwar2911")
                msg = "Machine3 gone fault!"
                server.sendmail("digitalelectronicssir@gmail.com", "shaik.anwar10@gmail.com", msg)
                server.quit()
                print 'email send'
	    #f.close()
            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

# call main"""
if __name__ == '__main__':
    main()

