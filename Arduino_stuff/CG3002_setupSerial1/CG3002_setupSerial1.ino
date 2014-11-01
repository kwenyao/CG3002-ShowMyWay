byte number = 0;

void setup(){
  //Raspberry Pi baud rate = 9600
  Serial1.begin(11500);
  
  //Setup serial monitor
  Serial.begin(9600);
}

void loop(){
  if (Serial1.available())  {
    //Read input from Raspberry Pi
    number = Serial1.read();
    
    //Print to Raspberry Pi
    Serial1.print("Serial1 Character received: ");
    Serial1.println(number, DEC);
    
    //Only used to display character on serial monitor
    //Serial.print("Serial0 Character received: ");
    //Serial.println(number, DEC);
    
  }
}

