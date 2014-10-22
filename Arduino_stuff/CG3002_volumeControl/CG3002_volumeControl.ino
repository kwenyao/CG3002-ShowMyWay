#include <Keypad.h>

int volume = 50;
int vol_HoldCount = 0;

int voiceType = 0;
int voiceType_HoldCount = 0;
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

void setup(){
  Serial.begin(9600);
  keypad.addEventListener(keypadEvent); //add an event listener for this keypad
}

void loop(){
  char key = keypad.getKey();
//
//  if (key) {
//    Serial.println(key);
//  }
}

//take care of some special events
void keypadEvent(KeypadEvent key){
  switch (keypad.getState()){
    case PRESSED:
      switch (key){
        case '0': break;
        case '#': break;
        case '*': break;
      }
    break;
    case RELEASED:
      switch (key){
        case '*': 
        if (vol_HoldCount == 1 && voiceType_HoldCount == 0) { 
          Serial.println("Volume control activated.");
          int new_volume = getKeypadVol();
          Serial.print("Your new volume is ");
          Serial.println(volume);
        }
        break;
        
        case '#':
        if (voiceType_HoldCount == 1 && vol_HoldCount == 0) {
          Serial.println("Voice type control activated.");
          int new_voiceType = getVoiceType();
          Serial.print("Your new voice type is ");
          Serial.println(voiceType);
        }
        break;
      }
    break;
    case HOLD:
      switch (key){
        case '*': 
        Serial.print(key); 
        Serial.println(" HOLD");
        vol_HoldCount = 1;
        break;
        
        case '#':
        Serial.print(key);
        Serial.println(" HOLD");
        voiceType_HoldCount = 1;
        break;
      }
    break;
  }
}

int getKeypadVol() {
  char input = '1';
  while (input != '0') {
    input = keypad.waitForKey();
    if (input == '4') { volume += 10; }
    else if (input == '7')   { volume -= 10; }
    if (volume > 100) {
      Serial.println("Volume is already at its maximum.");
      volume = 100;
    }
    else if (volume < 0) {
      Serial.println("Speaker has been muted."); //activate actuator?
      volume = 0;
    }
    Serial.print("Volume is now ");
    Serial.println(volume);
  }
  vol_HoldCount = 0;
  return volume;
}

int getVoiceType() {
  char input = '1';
  while (input != '0') {
    input = keypad.waitForKey();
    if (input == '6') { voiceType = (voiceType + 1) % 7; }
    else if (input == '9')   { voiceType = (voiceType + 6) % 7; }
    Serial.print("Voice type is now ");
    Serial.println(voiceType);
  }
  voiceType_HoldCount = 0;
  return voiceType;
}
