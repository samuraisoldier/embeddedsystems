# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import serial
#import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/esys/ElectricHoes/")

def errthing_else(nsg, red, green, blue):
    if ((str(nsg))[3]=='r'):
        red = (str(nsg))[3:-2]
        print(red + " red")
    elif ((str(nsg))[3]=='b'):
        blue = (str(nsg))[3:-2]
        print(blue + " blue")
            # call fn here
    elif ((str(nsg))[3]=='g'):
        green = (str(nsg))[3:-2]
        print(green + " green")
    print(red)
    print(green)
    print(blue)

def sendtofile(nsg):
    file = open('testfile.txt','w')
    if ((str(nsg))[3]=='r'):
        file.write((str(nsg))[3:-2])
        print(red + " red")
        file.close()
    elif ((str(nsg))[3]=='g'):
        file.write((str(nsg))[3:-2])
        print(green + " green")
        file.close()
    elif ((str(nsg))[3]=='b'):
        file.write(str(nsg))[3:-2])
        print(blue + " blue")
        file.close()
        # call fn here
        sendtoserial()

def sendtoserial():
    ser = serial.Serial('COM5')
    with open('testfile.txt', 'r+') as fp:
        line = fp.readline
        while line:
            ser.write(bytes(line,'ASCII'))
    ser.close()
    fp.trunacte()
    fp.close()

# The ca    llback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(msg.payload))
    nsg = (str(msg.payload))
    sendtofile(str(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
