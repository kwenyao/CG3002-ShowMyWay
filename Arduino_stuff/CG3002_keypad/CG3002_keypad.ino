#include "Arduino.h"
#include <iostream>
#include <cstdlib>
#include <Keypad.h>

int getYN();
int getKeypad4();
int getACK();
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
  if (Serial.available()) {
    //arbitrarily using '>' as a command from RPi to signify the start of getting user input
    char test = Serial.read();
    //Serial.println(test);
    if (test == '!') {
      //Serial.print("here");
      int yn_input = getYN();
      Serial.println(yn_input);
    }
    else if (test == '>') {
      int keypad_input = getKeypad4();
      //Serial.print("here");
      Serial.println(keypad_input);
    }
  }
}

int getKeypad4() {
  int i = 0;
  int values[4] = {0};
  for (i = 0; i<4; i++) {
    char input = keypad.waitForKey();
    if (input != NO_KEY) {
      int key = atoi(&input);
      values[i] = key;
    }
  }
  int data = values[0] * 1000 + values[1] * 100 + values[2] * 10 + values[3];
  return data;
}

int getYN() {
    char input = keypad.waitForKey();
    if (input != NO_KEY) {
      int key = atoi(&input);
      return key;
    } 
}
