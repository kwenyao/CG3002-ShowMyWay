byte number = 0;

void setup(){
  Serial.begin(9600);
}

void loop(){
  if (Serial.available())  {
    number = Serial.read();
    Serial.print("character received: ");
    Serial.println(number, DEC);
  }
}

