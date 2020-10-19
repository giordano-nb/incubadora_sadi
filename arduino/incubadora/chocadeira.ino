
#include <DHT.h>
#include <Wire.h>
#include "RTClib.h"
#include <string.h>

/////////////////////////////////////////////////////////////////////////

#define DHTPIN 7 
#define DHTTYPE DHT22 
#define BUZZERPIN 9
#define RELAY 4

#define FAN1 10
#define FAN2 11
#define FAN3 12

/////////////////////////////////////////////////////////////////////////

DHT dht(DHTPIN, DHTTYPE);
RTC_DS1307 rtc; 

float hum;  //Stores humidity value
float temp; //Stores temperature value
float temph; //Holds temperature value
int alm_time==0
float T;
int ALM1,ALM2,ALM3;
uint32_t count = 3590;
char buff[50]; 

/////////////////////////////////////////////////////////////////////////

void setup() {
  
  pinMode(BUZZERPIN, OUTPUT);
  pinMode(RELAY, OUTPUT);  
  pinMode(FAN1, OUTPUT);  
  pinMode(FAN2, OUTPUT);  
  pinMode(FAN3, OUTPUT);  
  digitalWrite(RELAY,HIGH);
  
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  dht.begin(); 
  if (! rtc.begin()) {                        
    while (1);                                
  }
  if (! rtc.isrunning()) {    
    // Aktuelles Datum und Zeit setzen, falls die Uhr noch nicht läuft
    rtc.adjust(DateTime(__DATE__, __TIME__));    
    }
  delay(2000); 
  temph= dht.readTemperature();
  T=37.5;
}

/////////////////////////////////////////////////////////////////////////

void ParseData()                          // split the data into its parts
{                                         
    char * Data;                    // this is used by strtok() as an index

    Data = strtok(buff," :"); 
      
    Data = strtok(NULL, " ");  
    T = atof(Data); //Temp

    Data = strtok(NULL, " ");  
    Fan = atof(Data); //Fan?

    Data = strtok(NULL, " ");
    ALM1 = atoi(Data);    // Hora
    
    Data = strtok(NULL, ":");
    ALM2 = atoi(Data);    // Min
    
    Data = strtok(NULL, ":");
    ALM3 = atoi(Data);    // Seg
}// T Fan H:M:S
/////////////////////////////////////////////////////////////////////////
/*void read_configs_val (configs_t * configs, char * in_string) {
  char * str_pos = in_string;
  char * last_pos = str_pos;

  char buff[10];
  char current_char = in_string[0];
  str_pos ++; // O primeiro elemento já está em current_char

  uint8_t buff_pos = 0;

  while(1) {
    while (current_char != ' ' && current_char != 0) {
      buff[buff_pos++] = current_char;
      current_char = *(str_pos++);
    }

    buff[buff_pos] = 0;
    buff_pos = 0;

    while (current_char == ' ') current_char = *(str_pos++);

    last_pos = str_pos-1;
    Serial.println(buff);
    
    if (current_char == 0) break;
  }
}
*/
/////////////////////////////////////////////////////////////////////////

void loop() {

   if(Serial.available()){ //Teste papra recebimendo de dados da interface
    static uint8_t pos = 0;
    while (Serial.available()) {
      if ((buff[pos++] = Serial.read()) == '\n'){
        buff[pos-1] = 0; // Remove o '/n' do fim da string
        pos = 0;
        // Serial.print(buff);
        while (Serial.available()) Serial.read(); // Esvazia o resto do buffer que tiver    
        break;  
      }
    }
        ParseData();
        alm_time=0; 
  } 
    delay(2000);
    
    //Read data and store it to variables hum and temp
    char buffer_v[50];
    hum = dht.readHumidity();
    temp= dht.readTemperature();
    DateTime tempoRTC = rtc.now();
    sprintf (buffer_v, "T%f H%f %d:%d:%d",tempo,hum,tempoRTC.hour(),tempoRTC.minute(),tempoRTC.second());                             
    Serial.println(buffer_v);
      
    if(alm_time==0){ 
    Alm_h = tempoRTC.hour() + ALM1;
    Alm_m= tempoRTC.minute() + ALM2;
    Alm_s = tempoRTC.second() + ALM3;
    
    if(Alm_s>60){
    Alm_h = Alm_h-60;
    Alm_m = Alm_m+1;}
    if(Alm_m>60){
    Alm_m = Alm_m-60;
    Alm_h = Alm_h+1;}
    if(Alm_h>24){Alm_h = Alm_h-24;}
    
    alm_time=1;
   }
        
    temp1 = T-0.5;
    temp2 = T+0.5;
     
    if((temp<temp1){ //Temperatua baixa
      if(temp>temp1-0.5){ //Próximo ao valor ideal
      if(temp>temph){ //Temperatura aumentando, esperar
       delay(1000);}
       else{ //Temperatura Diminuindo, ligar lâmpada
        digitalWrite(RELAY,LOW); 
        delay(1000);}}
        else{ // Temperatura muito baixa, desligar ventilador, ligar lâmpada
          digitalWrite(RELAY,LOW); 
          delay(1000);
          digitalWrite(FAN1,LOW);       
          digitalWrite(FAN2,LOW);      
          digitalWrite(FAN3,LOW);
          delay(1000); 
         }}
         
      else if(temp>temp2){//Temperatura alta
       if(temp<temp2+0.5){ //Próximo ao valor ideal
       if(temp<temph){ //Temperatura diminuindo, esperar
        delay(1000);}
        else{ //Temperatura Aumentando, desligar lâmpada
        digitalWrite(RELAY,HIGH); 
        delay(1000);}}
        else{ // Temperatura muito alta, ligar ventilador, desligar lâmpada
          digitalWrite(RELAY,HIGH); 
          delay(1000);
          digitalWrite(FAN1,HIGH);      
          digitalWrite(FAN2,HIGH);         
          digitalWrite(FAN3,HIGH);
          delay(1000); 
         }}
         else{
           if(temp>temph){ // Temperatura aumentando
           digitalWrite(FAN1,HIGH);
           digitalWrite(FAN2,LOW);      
           digitalWrite(FAN3,LOW);
           delay(1000);          
           }
           if(temp<temph){ // Temperatura diminuindo
           digitalWrite(RELAY,LOW);
           delay(1000); 
           }
         }
  if(tempoRTC.hour()==alm_h){
    if(tempoRTC.minute() - alm_m<=2){
    tone(BUZZERPIN, 1000); 
    delay(1000);        
    noTone(BUZZERPIN);     
    delay(1000);
    }
  }
 temph = temp;  
}

/////////////////////////////////////////////////////////////////////////
