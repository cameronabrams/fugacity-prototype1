#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "SPI.h"
#include "Adafruit_BMP280.h"
#include "DHT.h"

#define DHTPIN1 2     // Digital pin connected to the DHT sensor
#define DHTPIN2 4
#define DHTTYPE DHT11   // DHT 11
#define ONE_WIRE_BUS 5

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

float t_cal=0;

void setup(void)
{
  Serial.begin(9600);
  sensors.begin();
  dht1.begin();
  dht2.begin();
}

void loop(void)
{ 
  sensors.requestTemperatures(); 
  t_cal=sensors.getTempCByIndex(0);
  float h_in = dht1.readHumidity();
  float t_in = dht1.readTemperature();
  float f_in = dht1.readTemperature(true);
  float h_out = dht2.readHumidity();
  float t_out = dht2.readTemperature();
  float f_out = dht2.readTemperature(true);
  float pressure = bmp.readPressure();
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h_in) || isnan(t_in) || isnan(f_in)) {
    Serial.println(F("Failed to read from 'in' DHT sensor!"));
    return;
  }
  if (isnan(h_out) || isnan(t_out) || isnan(f_out)) {
    Serial.println(F("Failed to read from 'out' DHT sensor!"));
    return;
  }
  Serial.print(h_in);
  Serial.print(" ");
  Serial.print(t_in);
  Serial.print(" ");
  Serial.print(h_out);
  Serial.print(" ");
  Serial.print(t_out);
  Serial.print(" ");
  Serial.print(pressure);
  Serial.print(" ");
  Serial.println(t_cal);
  delay(1000);
}
