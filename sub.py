# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import serial
import datetime

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/esys/ElectricHoes/")

# The callback for when a PUBLISH message is received from the server.
#Fucntion receives the message and then calls the sendtofile function to process the data
def on_message(client, userdata, msg):
    nsg = (str(msg.payload))
    sendtofile(str(msg.payload)) #sends message as a string

#sendtofile detects if the message is formatted as expectted by checking the 4th character is a b
def sendtofile(nsg):
    if ((str(nsg))[4]=='b'):
        dateandtime = str(datetime.datetime.now().date())
        filename = dateandtime + 'values.txt'
        file = open(filename,'a')
        towrite = (str(nsg))[3:-2]
        file.write(str(datetime.datetime.now().time()))
        file.write(towrite)
        file.write("\n")
        #can read this live with Get-Content (date)values.txt -wait


#this section detects additional messages containing the red, green and blue values
#seperately in order to easily process them by saving to files and then sending them to serial
'''    if ((str(nsg))[4]=='r'):
        file = open('red.txt','w')
        red = (str(nsg))[5:-5]
        file.write(red)
        print(red + " red")

    elif ((str(nsg))[4]=='g'):
        file = open('green.txt','w')
        green = (str(nsg))[5:-5]
        file.write(green)
        print(green + " green")

    elif ((str(nsg))[4]=='l'):
        file = open('blue.txt','w')
        blue = (str(nsg))[5:-5]
        file.write(blue)
        print(blue + " blue")
        file.close()
        # call fn here
        sendtoserial()
'''

#unused function to process the rgb values and then send them to serial to arduino to light LEDs
'''
    # call fn here
def sendtoserial():
    rcol = 0
    gcol = 0
    bcol = 0
#first reads values from files
    with open('red.txt', 'r+') as fr:
        rcol = fr.read()
    with open('green.txt', 'r+') as fg:
        gcol = fg.read()
    with open('blue.txt', 'r+') as fp:
        bcol = fp.read()
#converts to string and zero pads to all be 3 digits
    rcols = str(rcol)
    gcols = str(gcol)
    bcols = str(bcol)
    rcol1 = rcols.zfill(3)
    gcol1 = gcols.zfill(3)
    bcol1 = bcols.zfill(3)
#combines all nmumbers into one variable with a 1 at the front to avoid 0 error in arduino
    padding_val = "1"
    colours = padding_val+rcol1+gcol1+bcol1

#send to serial to arduino - currently not working
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM5'
    ser.open()
    print(ser.is_open)
    ser.write(colours, 'ASCII')
    ser.close()
'''

#code to set up mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()



####change from serial to output to a document and add the time to it too
#import datetime
#datetime.datetime.now().time()
