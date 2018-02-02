# -*- coding: utf-8 -*-
import machine
import time
import network
import ujson
#import json
#check if json is really needed

from umqtt.simple import MQTTClient
from machine import I2C, Pin #for some reason needs both machine imports

regc=0xb5 #clear reg high
regr=0xb7 #red reg high
#regg=0xb9 #green reg high
#regb=0xbb #blue reg high
#avg_cnt = 3 #global variable for averaging purposes


# function to set up the wifi connection

def connect_network():
    ap_if = network.WLAN(network.AP_IF)     # access point false 
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)   # station true
    sta_if.active(True)
    sta_if.scan()                           #scan for wifi networks
    time.sleep(3)                           #pause to allow scan to complete
    sta_if.connect('EEERover', 'exhibition')#connect to the wifi network
    time.sleep(3)                           #pause to allow completion
    print(sta_if.isconnected())             #debug line to check connection
    return

#function to set up MQTT
def connect_mqtt():
    device_id=str(machine.unique_id())
    client=MQTTClient(device_id, '192.168.0.10')
    client.connect()
    testmsg=ujson.dumps({'name':'successful connection'})
    client.publish('/esys/ElectricHoes/',bytes(testmsg, 'utf-8'))
    return
    
    
cnter = 0

while (cnter < 100):
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq = 100000)
    i2c.writeto(0x29, bytearray({0xa0, 0x03}))
    i2c.writeto(0x29, bytearray({regr}))
    data=int.from_bytes(i2c.readfrom(0x29, 2), 'little')
    payload=ujson.dumps({'name':'lux1', 'temprecord':data})
    print(payload)
    client.publish('/esys/ElectricHoes/',bytes(payload, 'utf-8'))
    time.sleep(10)
    cnter = cnter + 1


#def readval (length):
#   data=int.from_bytes(i2c.readfrom(0x29, length), 'little')

#def readreg (length, reg):
#    i2c.writeto(0x29, bytearray({regc}))
#    data = readval(2)
    
 #   i = 0
 #   while (i<avg_cnt):
 #       readval(8)
