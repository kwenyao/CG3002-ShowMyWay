#include "Arduino.h"
#include <iostream>
#include <cstdlib>
#include <Keypad.h>
#include <string.h>

byte number = 0;
//char handshake_RDY[3] = {0};
char handshake_ACKRDY[7] = {0};
int handshakeCount = 0;
int ACKRDY_count = 0;
void setup(){
  Serial.begin(9600);
}

void loop(){
  if (Serial.available()) {
    ACKRDY_count = establish_ACKRDY();
    //Serial.println(ACKRDY_count);
    if (ACKRDY_count == 0) {
      Serial.println("RDY");
      delay(200);
    }
    else if (ACKRDY_count == 1) {
      Serial.println("ACKACK");
      delay(200);
    }
  }
}

int establish_ACKRDY() {
  int i = 0;
  if (Serial.available()) {
    for (i=0; i<6; i++) {
      handshake_ACKRDY[i] = Serial.read();
    }
  }
  if (compare_ACKRDY()) {
    return 1;
  }
  return 0;
}

int compare_ACKRDY() {
  char ackrdy_str[7] = "ACKRDY";
  int cmp_count = 0;
  int i = 0;
  for (i=0; i<6; i++) {
    if (handshake_ACKRDY[i] == ackrdy_str[i]) { cmp_count++; }
    else
      return 0;
  }
  
  if (cmp_count == 6) { return 1; }
  return 0;
}
