# -*- coding: utf-8 -*-
import machine
import time
import network
import ujson


from umqtt.simple import MQTTClient
from machine import I2C, Pin #for some reason needs both machine imports
#import paho.mqtt.client as mqtt

#global variables
i2c = I2C(scl=Pin(5), sda=Pin(4), freq = 100000)
regc=0xb5 #clear reg high
regr=0xb7 #red reg high
regg=0xb9 #green reg high
regb=0xbb #blue reg high

#need client to be accessible in multiple functions, might need to pass it as an operand
device_id=str(machine.unique_id())
client=MQTTClient(device_id, '192.168.0.10')

#sideting function to set up the wifi connection
def connect_network():
    ap_if = network.WLAN(network.AP_IF)     # access point false
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)   # station true
    sta_if.active(True)
    sta_if.scan()                           #scan for wifi networks
    time.sleep(4)                           #pause to allow scan to complete
    sta_if.connect('EEERover', 'exhibition')#connect to the wifi network
    time.sleep(4)                           #pause to allow completion
    print(sta_if.isconnected())             #debug line to check connection

#sideting function to set up MQTT
def connect_mqtt(client):
    #device_id=str(machine.unique_id())
    #client=MQTTClient(device_id, '192.168.0.10')
    client.connect()
    testmsg=ujson.dumps({'name':'successful connection'})
    client.publish('/esys/ElectricHoes/',bytes(testmsg, 'utf-8'))

#sideting function to test mqtt
def mqtt_test(client):
    i2c.writeto(0x29, bytearray({0xa0, 0x03}))
    i2c.writeto(0x29, bytearray({regc}))
    test_data=int.from_bytes(i2c.readfrom(0x29, 2), 'little')
    test_load=ujson.dumps({'name':'test', 'temprecord':test_data})
    print(test_load)
    client.publish('/esys/ElectricHoes/',bytes(test_load, 'utf-8'))

#sideting function to read values from sensor
def read_val(reg):
    i2c.writeto(0x29, bytearray({0xa0, 0x03}))
    i2c.writeto(0x29, bytearray({reg}))
    data=int.from_bytes(i2c.readfrom(0x29, 2), 'little')
    return data

def take_reading():
    avgcnt = 0
    luxsum = 0
    greensum = 0
    redsum = 0
    bluesum = 0
    cntmax = 100
    while(avgcnt < cntmax):
        luxsum = luxsum + read_val(regc)
        redsum = redsum + read_val(regr)
        greensum = greensum + read_val(regg)
        bluesum = bluesum + read_val(regb)
        avgcnt = avgcnt + 1
    #lux1 = luxsum/cntmax
    #lux = "l"+

    '''red1 = redsum/cntmax
    red = "r"+str(red1)
    green1 = greensum/cntmax
    green = "g" + str(green1)
    blue1 = bluesum/cntmax
    blue = "b"+str(blue1)

    #luxj=ujson.dumps({lux})
    #print(luxj)
    #client.publish('/esys/ElectricHoes/',bytes(luxj, 'utf-8'))

    redj=ujson.dumps({red})
    print(redj)
    client.publish('/esys/ElectricHoes/',bytes(redj, 'utf-8'))

    greenj=ujson.dumps({green})
    print(greenj)
    client.publish('/esys/ElectricHoes/',bytes(greenj, 'utf-8'))

    bluej=ujson.dumps({blue})
    print(bluej)
    client.publish('/esys/ElectricHoes/',bytes(bluej, 'utf-8'))
'''

    red = redsum/cntmax
    green = greensum/cntmax
    blue = bluesum/cntmax
    payload=ujson.dumps({'clear':lux, 'red': red, 'green': green, 'blue':blue})
    print(payload)
    client.publish('/esys/ElectricHoes/',bytes(payload, 'utf-8'))

def sub_cb(topic, msg):
    print((topic,msg))
    if msg == b"on":
        print("1")
        take_reading()

def main():
    #server=
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe('/esys/ElectricHoes/')
    #print("Connected to %s, subscribed to %s topic" %('192.168.1.10', '/esys/ElectricHoes/'))
    print("ready")
    try:
        while 1:
            client.wait_msg()
    finally:
        print("0")
        client.disconnect()

print("setting up network")
#set up wifi connection
connect_network()
print("setting up mqtt")
#connect to the mqtt server
connect_mqtt(client)
print=("Gucci Gang")
#subscribeee and wait
main()






'''
#mainting inni
def main():
    cnter = 1
    while (cnter < 201):
        avgcnt = 0
        luxsum = 0
        greensum = 0
        redsum = 0
        bluesum = 0
        cntmax = 100
        while(avgcnt < cntmax):
            luxsum = luxsum + read_val(regc)
            redsum = redsum + read_val(regr)
            greensum = greensum + read_val(regg)
            bluesum = bluesum + read_val(regb)
            avgcnt = avgcnt + 1
        lux = luxsum/cntmax
        red = redsum/cntmax
        green = greensum/cntmax
        blue = bluesum/cntmax
        #reading = time
        payload=ujson.dumps({'count':cnter, 'clear':lux, 'red': red, 'green': green, 'blue':blue}) #need to add time library for this
        print(payload)
        client.publish('/esys/ElectricHoes/',bytes(payload, 'utf-8'))
        time.sleep(4)
        cnter = cnter + 1
'''
