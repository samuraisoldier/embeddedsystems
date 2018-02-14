# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import serial
import datetime
#import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/esys/ElectricHoes/")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    nsg = (str(msg.payload))
    sendtofile(str(msg.payload))

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

    if ((str(nsg))[4]=='r'):
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



    # call fn here
def sendtoserial():
    rcol = 0
    gcol = 0
    bcol = 0
    with open('red.txt', 'r+') as fr:
        rcol = fr.read()
    with open('green.txt', 'r+') as fg:
        gcol = fg.read()
    with open('blue.txt', 'r+') as fp:
        bcol = fp.read()

    rcols = str(rcol)
    gcols = str(gcol)
    bcols = str(bcol)
    rcol1 = rcols.zfill(3)
    gcol1 = gcols.zfill(3)
    bcol1 = bcols.zfill(3)

    padding_val = "1"
    colours = padding_val+rcol1+gcol1+bcol1

    print(colours)

    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM5'
    ser.open()
    print(ser.is_open)
    ser.write(colours, 'ASCII')
    ser.close()



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
