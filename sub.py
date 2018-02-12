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
    print(str(msg.payload))
    nsg = (str(msg.payload))
    sendtofile(str(msg.payload))

def sendtofile(nsg):
    dateandtime = str(datetime.datetime.now().date())
    filename = dateandtime + ' values.txt'
    file = open(filename,'a')
    towrite = (str(nsg))[3:-2]
    file.write(str(datetime.datetime.now().time()))
    file.write(towrite)
    file.write("\n")
    print(towrite)
    # call fn here
    #sendtoserial()



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
