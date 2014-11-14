### CONSTANTS USED IN NAVIGATION ###
VISUALISATION = False
PROXIMITY_RADIUS = 0.6 # in meters

### CONSTANTS USED IN GUIDE ###
STEP_LENGTH = 0.4 # in meters
USER_SPEED = 0.4 # in m/s
STAIR_LIMIT = 0.40 # in meters
ORIENTATION_DEGREE_ERROR = 10
INSTRUCTIONS_FREQUENCY = 10 # in seconds
MAX_ON_PLATFORM_STEPS = 15 #counts
IR_STAIRS_CONSTANT = 0 
PEAK_ACC_VALUE = 0 #the peak accelerometer measured by arduino during the calibration phase. to be stored in memory when calibration phase is not ran again. 
WALKING_DEGREE_ERROR = 20
TIME_TO_CHECK_BEARING = 2 #time delay since last step to check user bearing
TURN_INSTRUCTION_FREQ = 5
COMPASS_OFFSET = 0;
YPR_OFFSET = 0

### CONSTANTS USED IN VOICE ###
HIGHEST_PRIORITY = 3
HIGH_PRIORITY = 2
MED_PRIORITY = 1
LOW_PRIORITY = 0
