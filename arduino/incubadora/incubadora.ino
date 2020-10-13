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

typedef struct {
  uint8_t hour;
  uint8_t minutes;
  uint8_t seconds;
} time_t;

typedef struct {
  float ts;
  uint8_t fan;
  time_t alm;
  time_t rtc;
} configs_t ;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  randomSeed(analogRead(0));
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

uint32_t count = 3590;
char buff[50];

void read_configs_val (configs_t * configs, char * in_string) {
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

void loop() {
  if(Serial.available()){
    static uint8_t pos = 0;
    while (Serial.available()) {
      if ((buff[pos++] = Serial.read()) == '\n'){
        buff[pos-1] = 0; // Remove o '/n' do fim da string
        pos = 0;
        // Serial.print(buff);
        while (Serial.available()) Serial.read(); // Esvazia o resto do buffer que tiver    
        read_configs_val(NULL, buff );
        break;  
      }
    }
  }



  // if(Serial.available()){ 
  //   delay(100);
  //   while(Serial.available()) Serial.read(); // seca o buffer de entrada para retransmitir quando receber algo novo
    
  //   long randNumber = random(370, 430);
  //   count ++;

  //   uint8_t tempVar = 0;
  //   uint8_t segundos =count%60;
  //   tempVar = (count - segundos)/60;
  //   uint8_t minutos = tempVar%60;
  //   uint8_t horas = (tempVar - minutos)/60;
    
  //   Serial.print(">TS:"); Serial.println((float)randNumber/10.0, 2);
  //   Serial.print(">TR:"); Serial.println((float)randNumber/10.0-5.0, 2);
  //   Serial.print(">HM:"); Serial.println((float)randNumber/10.0+25.0, 2);
  //   Serial.print(">FAN:"); Serial.println(segundos);
  //   Serial.println(">ALM:10:00:00");
  //   sprintf(buff, ">RTC:%02d:%02d:%02d", horas,minutos,segundos );
  //   Serial.println(buff);
  // }
}
