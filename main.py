# -*- coding: utf-8 -*-
import machine
import time
import network
import ujson


from umqtt.simple import MQTTClient
from machine import I2C, Pin #for some reason needs both machine imports

#global variables
i2c = I2C(scl=Pin(5), sda=Pin(4), freq = 100000)
regc=0xb4 #clear reg high
regr=0xb6 #red reg high
regg=0xb8 #green reg high
regb=0xba #blue reg high

#need client to be accessible in multiple functions, might need to pass it as an operand
device_id=str(machine.unique_id())
client=MQTTClient(device_id, '192.168.0.10')

#function to set up the wifi connection
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

#function to set up MQTT
def connect_mqtt(client):
    client.connect()
    testmsg=ujson.dumps({'name':'successful connection'}) #print to confirm connection
    client.publish('/esys/ElectricHoes/',bytes(testmsg, 'utf-8'))

#function to read values from sensor
def read_val(reg):
    i2c.writeto(0x29, bytearray({0xa0, 0x03})) #initialise WEN and AEN
    i2c.writeto(0x29, bytearray({reg})) #ask device to read from each register
    data=int.from_bytes(i2c.readfrom(0x29, 2), 'little') #read data and convert to int
    return data #return the data

def take_reading():
    #set up needd variables
    avgcnt = 0
    luxsum = 0
    greensum = 0
    redsum = 0
    bluesum = 0
    cntmax = 100 #set up how many readings to take average of

    #take cntmax readings of each colour
    while(avgcnt < cntmax):
        luxsum = luxsum + read_val(regc)
        redsum = redsum + read_val(regr)
        greensum = greensum + read_val(regg)
        bluesum = bluesum + read_val(regb)
        avgcnt = avgcnt + 1

    lux1 = (luxsum/cntmax) #average the brightness

    #average the red readings
    red1 = (redsum/cntmax)
    red=round(((red1*255)/20000), 0)

    #average the green readings
    green1 = greensum/cntmax
    green=round(((green1*255)/20000), 0)

    #average the blue readings
    blue1 = bluesum/cntmax
    blue=round(((blue1*255)/20000), 0)

    #prepare and send payload
    payload=ujson.dumps({'brightness': lux1, 'red': red, 'green': green, 'blue':blue})
    client.publish('/esys/ElectricHoes/',bytes(payload, 'utf-8'))

    #code to seperately send each colour for individual processing to light up LEDS
    '''
    time.sleep(1) #pause to allow subscribe to complete all tasks
    red = "r"+str(red)
    redj=ujson.dumps({red})
    print(redj)
    client.publish('/esys/ElectricHoes/',bytes(redj, 'utf-8'))

    time.sleep(1)
    green = "g" + str(green)
    greenj=ujson.dumps({green})
    print(greenj)
    client.publish('/esys/ElectricHoes/',bytes(greenj, 'utf-8'))

    time.sleep(1)
    blue = "l"+str(blue)
    bluej=ujson.dumps({blue})
    print(bluej)
    client.publish('/esys/ElectricHoes/',bytes(bluej, 'utf-8'))
    '''

    #subscribe function to take readings when you send "on"
def sub_cb(topic, msg):
    print((topic,msg))
    if msg == b"on":
        take_reading()

#set up mqtt
def sub_function():
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe('/esys/ElectricHoes/')
    print("Connected to %s, subscribed to %s topic" %('192.168.1.10', '/esys/ElectricHoes/'))
    print("ready")
    try:
        while 1:
            client.wait_msg()
    finally:
        client.disconnect()

print("setting up network")
#set up wifi connection
connect_network()
print("setting up mqtt")
#connect to the mqtt server
connect_mqtt(client)
print("Ready to take readings")
#subscribe and wait for a message
sub_function()
