### MESSAGE TEMPLATES ###
HANDSHAKE_FAIL_TEMPLATE = "Handshake failed with exit code {code}"
INPUT_START_CONFIRMATION_TEMPLATE = "Your starting building name is {building}, level {level}, start location is {start}. Press 1 to confirm, 2 to re-enter."
INPUT_END_CONFIRMATION_TEMPLATE = "Your ending building name is {building}, level {level}, destination is {end}. Press 1 to confirm, 2 to re-enter."
NODE_REACHED_TEMPLATE = "You have reached {node}."
NEXT_NODE_TEMPLATE = "Your next node is {node}."
TURN_TEMPLATE = "Turn {direction} {angle} degrees."
WALK_FORWARD_TEMPLATE = "Walk forward {steps} steps."
HEAD_OBSTACLE_TEMPLATE = "Obstacle at head level {distance} meters away."

VOICE_CMD_TEMPLATE = "espeak -s150 -a{volume} {voice} '{msg}' 2>/dev/null"
### INITIALISATION MESSAGES ###
CALIBRATION_START = "Running calibration phase. Start walking 10 meters."
CALIBRATION_END = "Calibration completed."
INPUT_START_BUILDING_NUMBER = "Please enter your starting building number."
INPUT_START_BUILDING_LEVEL = "Please enter your starting building level."
INPUT_END_BUILDING_NUMBER = "Please enter your ending building number."
INPUT_END_BUILDING_LEVEL = "Please enter your ending building level."
INPUT_START_NODE = "Please enter your start node."
INPUT_END_NODE = "Please enter your end node."
INPUT_CONFIRMATION_SUCCESS = "Confirmation successful."
MAP_DOWNLOAD_FAILED = "Map download failed. Please enter a new map"

### GUIDE MESSAGES ###
DESTINATION_REACHED = "You have reached your destination."
DOWN_STAIRS = "Downward stairs detected."
UP_STAIRS = "Upward stairs detected."
TAKE_ONE_STEP_TEMPLATE = "Take one step {direction} carefully."
