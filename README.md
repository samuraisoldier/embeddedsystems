# embeddedsystems
2017/2018 year 3 IoT coursework

Our product is a paint or hair dye colour sensor. Builders would use it to match paint samples and send the data to their office to get the correct paint ordered. Similar for people wanting to get their hair dyed. Digital Artists would be able to sample coloours in the real world for use in their digital masterpieces, to capture their inspiration exactly.

Main.py is the code for the esp8266 to take readings and send via MQTT to the broker as a JSON payload.
sub.py is the code to subscribe and process the data to a text file and send via serial to arduino.
lightitup.ino processes colour data sent by serial to arduino to light the LEDs.
