/*
  ASCII table

  Prints out byte values in all possible formats:
  - as raw binary values
  - as ASCII-encoded decimal, hex, octal, and binary values

  For more on ASCII, see http://www.asciitable.com and http://en.wikipedia.org/wiki/ASCII

  The circuit: No external hardware needed.

  created 2006
  by Nicholas Zambetti <http://www.zambetti.com>
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/ASCIITable
*/

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  randomSeed(analogRead(0));
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

uint32_t count = 3590;
char buff[20];

void loop() {
  if(Serial.available()){ 
    delay(100);
    while(Serial.available()) Serial.read(); // seca o buffer de entrada para retransmitir quando receber algo novo
    
    long randNumber = random(370, 430);
    count ++;

    uint8_t tempVar = 0;
    uint8_t segundos =count%60;
    tempVar = (count - segundos)/60;
    uint8_t minutos = tempVar%60;
    uint8_t horas = (tempVar - minutos)/60;
    
    Serial.print(">TS:"); Serial.println((float)randNumber/10.0, 2);
    Serial.print(">TR:"); Serial.println((float)randNumber/10.0-5.0, 2);
    Serial.print(">HM:"); Serial.println((float)randNumber/10.0+25.0, 2);
    Serial.print(">FAN:"); Serial.println(segundos);
    Serial.println(">ALM1:10:00:00");
    Serial.println(">ALM2:18:00:00");
    sprintf(buff, ">RTC:%02d:%02d:%02d", horas,minutos,segundos );
    Serial.println(buff);
    Serial.println(">PI:2.3:5.1");
  }
}
