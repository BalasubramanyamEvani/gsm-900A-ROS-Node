#include <SoftwareSerial.h>
SoftwareSerial SIM900A(10,11);                                    //define the pins for rx,tx

String str = "";                                                  //global variable for storing incoming string

void setup() {                                                    //setup loop, called once
  
  Serial.begin(2400);                                             // baud rate
  while(!Serial);
  Serial.println("Arduino with SIM900A is ready");
  
  SIM900A.begin(2400); 
  Serial.println("SIM900A started at 2400");
  delay(1000);
  Serial.println("Setup Complete! SIM900A is Ready!");

  SIM900A.write("AT+CENG=2\r");                                   //starts the engineering mode of gsm
  
}
void loop(){                                                      //continuous loop
  
  if (SIM900A.available()){ 
    
    char c = SIM900A.read();                                      //reads data from UART
    str = String(str+c);

    if(str[str.length() - 1] == '\n'){                            // waits for new line
      
      //Serial.println(str);                                      //uncomment to see the data
      unsigned char rec_level = ( int(str[14] - '0') * 10 + int(str[15] - '0') );  // parse the received level
      unsigned char rec_quality = ( int(str[17] - '0') * 10 + int(str[18] - '0') ); // parse the received strength
      
      if(isDigit(str[19]))                                                                            
        rec_quality = ( int(str[17] - '0') * 100 + int(str[18] - '0') * 10 + int(str[19] - '0') ); // if three chars received

      unsigned char num = int(str[6] - '0');

      Serial.print("Cell Num: ");           // sending the result to serial monitor so that it can be read from the python script
      Serial.print(num);
      Serial.print(" rec_level: ");
      Serial.print(rec_level);
      Serial.print(" rec_quality: ");
      Serial.println(rec_quality);
          
      str = "";                             // clears out the string for storing new data
    }
  }
}
