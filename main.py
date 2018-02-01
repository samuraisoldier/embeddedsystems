# -*- coding: utf-8 -*-
import machine
import time
import network
import ujson
import json

from umqtt.simple import MQTTClient
from machine import I2C, Pin

regc=0xb5
regr=0xb7
#regg=0xb9
#regb=0xbb
#avg_cnt = 3

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
time.sleep(5)
sta_if.connect('EEERover', 'exhibition')
time.sleep(5)
print(sta_if.isconnected())

device_id=str(machine.unique_id())
#print(device_id)
client=MQTTClient(device_id, '192.168.0.10')
client.connect()

cnter = 0

while (cnter < 100):
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq = 100000)
    i2c.writeto(0x29, bytearray({0xa0, 0x03}))
    i2c.writeto(0x29, bytearray({regr}))
    data=int.from_bytes(i2c.readfrom(0x29, 2), 'little')
    payload=ujson.dumps({'name':'lux1', 'temprecord':data})
    print(payload)
    client.publish('esys/El3ctricH0es/hello',bytes(payload, 'utf-8'))
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