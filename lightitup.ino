#include <Adafruit_NeoPixel.h>
#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(237, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // declare the ledPin as an OUTPUT:
  strip.begin();
  strip.clear();
  strip.show();
}

void loop() {

  int colours = 0;
  for (int i = 0; i <= 237; i++) {
    strip.setPixelColor(i, 1, 1, 1);
    strip.show();
  }

  if (Serial.available() >= 1) {
    int colours = Serial.read();

    String hello = String(colours);
    int red = hello.substring(1, 4).toInt();
    for (int i = 0; i <= 237; i++) {
      strip.setPixelColor(i, 25, 1, 1);
      strip.show();
    }

    int green = hello.substring(4, 7).toInt();
    for (int i = 0; i <= 237; i++) {
      strip.setPixelColor(i, 1, 25, 1);
      strip.show();
    }
    
    int blue = hello.substring(7, 10).toInt();
    for (int i = 0; i <= 237; i++) {
      strip.setPixelColor(i, 1, 1, 25);
      strip.show();
    }
    
    for (int i = 0; i <= 237; i++) {
      strip.setPixelColor(i, red, green, blue);
      strip.show();
    }
  }
}
