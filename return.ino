#include "DHT.h"
#define dhtPin 8    
#define dhtType DHT11    

DHT dht(dhtPin, dhtType); 
void setup() {
  Serial.begin(9600);
  dht.begin();//啟動DHT
  pinMode(9,OUTPUT);
  }

void loop() { 
  delay(5000);//延時5秒
  float h = dht.readHumidity();//讀取濕度
  float t = dht.readTemperature();//讀取攝氏溫度
  int mois = analogRead(A0);
  int light = analogRead(A1);
  if (isnan(h) || isnan(t)) {
    Serial.println("無法從DHT傳感器讀取！");
    return;
  }
 if(mois >= 700){
    digitalWrite(9,HIGH); //高電平觸發
   // Serial.print("power of watet on \n");
  }
  else if (mois <= 500){
    digitalWrite(9,LOW);
    //Serial.print("power of watet off \n");
 }
  
   Serial.print("hum: ");
   Serial.print(h);
   Serial.print("tem: ");
   Serial.print(t);
   Serial.print("moi: ");
   Serial.print(mois);
  if(mois<=999){
   Serial.print(" ");
    }
   Serial.print("light:");
   Serial.println(light);
   Serial.println(" ");

}
