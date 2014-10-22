#include "Arduino.h"
#include <iostream>
#include <cstdlib>
#include <Keypad.h>
#include <math.h>

int pow10(int);
int getKeypad();
int getYN();
char* getKeypad4();
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
  int keypad_input = getKeypad();
  Serial.println(keypad_input);
}

int getKeypad() {
  int i = 0;
  int values[5] = {0};
  for (i=0; i<4; i++) {
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
  int data = 0;
  for (int j=i-1; j>=0; j--) {
    data += values[j] * power10(3-j);
  }
  
  for (i = 4-i; i>0; i--) {
    data /= 10;
  }
  return data;
}

int power10(int pow) {
  if (pow == 0) {
    return 1;
  }
  else if (pow == 1) {
    return 10;
  }
  else if (pow == 2) {
    return 100;
  }
  else if (pow == 3) {
    return 1000;
  }
}
