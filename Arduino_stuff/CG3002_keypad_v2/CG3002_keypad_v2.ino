#include "Arduino.h"
#include <iostream>
#include <cstdlib>
#include <Keypad.h>

unsigned long pow10(int);
unsigned long getKeypad8();
int getYN();
int getACK();

int getHandshake = 1;
byte number = 0;
char handshake_ACKRDY[7] = {0};
int handshakeCount = 0;
int ACKRDY_count = 0;
int establish_ACKRDY();
int compare_ACKRDY();

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {8, 7, 6, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {4, 3, 2}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup() {
  Serial.begin(9600);
}

void loop() {
//  unsigned long keypad_input = getKeypad8();
//  Serial.println(keypad_input);
  char test = Serial.read();
  while (getHandshake) {
    if (Serial.available()) {
      ACKRDY_count = establish_ACKRDY();
      while (ACKRDY_count == 0) {
        Serial.println("RDY");
        delay(200);
        ACKRDY_count = establish_ACKRDY();
      }
      while (ACKRDY_count == 1) {
        test = Serial.read();
        Serial.println("ACKACK");
        delay(200);
        if (test == '!' || test == '>') {
          getHandshake = 0;
          break;
        }
      }
    }
  }
  if (test == '!') {
    int yn_input = getYN();
    Serial.println(yn_input);
  }

  else if (test == '>') {
    unsigned long keypad_input = getKeypad8();
    Serial.println(keypad_input);
  }
}

unsigned long getKeypad8() {
  int i = 0;
  int values[9] = {0};
  for (i=0; i<8; i++) {
    char input = keypad.waitForKey();
    if (input != NO_KEY) {
      if (input == '#') {
        break;
      }
      else {
        int key = atoi(&input);
        values[i] = key;
      }
    }
  }
  unsigned long data = 0;
  for (int j=i-1; j>=0; j--) {
    data += values[j] * power10(7-j);
  }
  
  for (i = 8-i; i>0; i--) {
    data /= 10;
  }
  return data;
}

int getYN() {
    char input = keypad.waitForKey();
    if (input != NO_KEY) {
      int key = atoi(&input);
      return key;
    } 
}

unsigned long power10(int pow) {
  if (pow == 0) { return 1; }
  else if (pow == 1)  { return 10; }
  else if (pow == 2)  { return 100; }
  else if (pow == 3)  { return 1000; }
  else if (pow == 4)  { return 10000; }
  else if (pow == 5)  { return 100000; }
  else if (pow == 6)  { return 1000000; }
  else if (pow == 7)  { return 10000000; }
  else if (pow == 8)  { return 100000000; }
//  else if (pow == 9)  { return 1000000000; }
//  else if (pow == 10) { return 10000000000; }
//  else if (pow == 11) { return 100000000000; }
//  else if (pow == 12) { return 1000000000000; }
//  else if (pow == 13) { return 10000000000000; }
//  else if (pow == 14) { return 100000000000000; }
//  else if (pow == 15) { return 1000000000000000; }
//  else if (pow == 15) { return 10000000000000000; }
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
