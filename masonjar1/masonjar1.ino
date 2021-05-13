/***************************************************************************
  Sketch for generating temperature, pressure and relative humidity
  in a BME280-instrumented mason jar
 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;

unsigned long delayTime;
unsigned long readoutcounter;
unsigned long labelsevery;
void setup() {
    Serial.begin(9600);
    while(!Serial);
    unsigned status;
    status = bme.begin();  
    // You can also pass in a Wire library object like &Wire2
    // status = bme.begin(0x76, &Wire2)
    if (!status) {
        Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
        Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(),16);
        Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
        Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
        Serial.print("        ID of 0x60 represents a BME 280.\n");
        Serial.print("        ID of 0x61 represents a BME 680.\n");
        while (1) delay(10);
    }
    
    //Serial.println("-- Default Test --");
    delayTime = 1000;
    readoutcounter = 0;
    labelsevery = 100;
    //Serial.println("#LABELS time(s) T(C) P(bar) RH(%)");
}


void loop() { 
    printValues();
    delay(delayTime);
}


void printValues() {
    if ((readoutcounter%labelsevery)==0) {
      Serial.println("#LABELS time(s) T(C) P(bar) RH(%)");
    }
    Serial.print(millis()/1000.0F);
    Serial.print(" ");
    Serial.print(bme.readTemperature(),2);
    Serial.print(" ");
    Serial.print(bme.readPressure() / 100000.000F, 4);
    Serial.print(" ");
    Serial.print(bme.readHumidity(),4);
    Serial.println();
    readoutcounter++;
}
