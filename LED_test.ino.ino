#include <Adafruit_NeoPixel.h>
#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(237, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.clear();
  strip.show();
  Serial.begin(9600);
  Serial.print("Ready");
}

void loop() {
  if (Serial.available() >= 0) {
    int red = Serial.parseInt();
    int green = Serial.parseInt();
    int blue = Serial.parseInt();
    //int strength = Serial.parseInt();
    Serial.print("colours");
    Serial.print(red);
    Serial.print(":");
    Serial.print(green);
    Serial.print(":");
    Serial.print(blue);
    Serial.print('\n');

    int r = round((red/65000)*255)
    int g = round((green /65000)*255);
    int b = round((green /60)*255);

    for (int i=0; i <= 237; i++){
      strip.setPixelColor(i,r,g,b);
    }
    //int brightness = (200*strength)/brightness;
    //strip.setBrightness(brightness);
    strip.show();
  }
}
