import os, time
import serial
import subprocess

#initialise serial port with Arduino
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
ser.open()

#convert audio output to audio jack
os.system("amixer cset numid=3 1")

#formatting of syntax and defining speech quality
variation = {'female1': ' -ven+f3', 'female2': ' -ven+f4', \
        'male1': ' -ven+m2', 'male2': ' -ven+m3'}
volume = str(100)
syntax_head = 'espeak -s150 -a'
syntax_tail = " ' 2>/dev/null"
step_count = str(5)
startloc = ['0', '0', '0', '0']
dest = ['0', '0', '0', '0']
yninput = 0

#library of messages
message = {1: 'Welcome', 2: 'Please key in your', \
        3: 'you have keyed in', 4: 'as your', 5: 'shall I proceed?', \
        6: 'please take a step', 7: 'please take another step', \
        8: 'thank you', 9: 'calculating path', 10: 'process complete', \
        11: 'please turn', 12: 'please go straight', \
        13: 'you have reached the edge of a staircase. please be careful and', \
        14: 'please open the door to your', 15: 'you have arrived at your destination', \
        16: 'object detected', 17: 'please proceed with caution', \
        18: 'path is blocked. would you like to stay on the same path?', \
        19: 'path is clear', 20: 'goodbye', 21: 'calibrating your stride', \
        22: 'please wait', 23: 'you have reached the end of the staircase', \
        24: 'please try again.', \
        #message chips
        31: 'starting location', 32: 'destination', \
        41: 'please press', 42: '1 for yes', 43: '2 for no', \
        51: 'left', 52: 'right', 53: 'front', 54: 'start ascending', 55: 'start desecnding', \
        56: 'stop', \
        #inputs needed
        61: 'in' , 62: step_count, 63: 'steps', \
        64: '|'.join(startloc), 65: '|'.join(dest), 66: yninput}


message_str = {\
        #startup processes: start location, destination, calibration and path calculations
        'startup':              message[1] + ". " + message[2] + " " + message[31] + ".", \
        'get_dest':             message[2] + " " + message[32] + ".", \
        'confirm_startloc':     message[3] + " " + message[64] + " " + message[4] + " " + \
                                message[31] + ". " + message[5], \
        'confirm_dest':         message[3] + " " + message[65] + " " + message[4] + " " + \
                                message[32] + ". " + message[5], \
        'yn_inst':              message[41] + " " + message[42] + ". " + message[41] + " " + \
                                message[43] + ".",
        'confirm_yes':          message[3] + " " + message[42] + ".", \
        'confirm_no':           message[3] + " " + message[43] + ".", \
        'cali_header':          message[21] + ".", \
        'cali_inst1':           message[6] + ".", \
        'cali_inst2':           message[7] + ".", \
        'path_calc':            message[9] + ". " + message[22], \
        #directional messages
        'left':                 message[11] + " " + message[51] + ".", \
        'right':                message[11] + " " + message[52] + ".", \
        'left_st':              message[11] + " " + message[51] + " " + message[61] + " " + \
                                message[62] + " " + message[63] + ".", \
        'right_st':             message[11] + " " + message[52] + " " + message[61] + " " + \
                                message[62] + " " + message[63] + ".", \
        'straight':             message[12] + ".", \
        'stairs_a':             message[13] + " " + message[54] + ".", \
        'stairs_d':             message[13] + " " + message[55] + ".", \
        'stairs_end':           message[23] + ".", \
        'door_left':            message[14] + " " + message[51] + ".", \
        'door_right':           message[14] + " " + message[52] + ".", \
        'door_front':           message[14] + " " + message[53] + ".", \
        'dest_arrived':         message[15] + ".", \
        #object detection
        'obj_det':              message[16] + ".", \
        'obj_det_st':           message[16] + " " + message[61] + " " + message[62] + " " + \
                                message[63] + ".", \
        'caution':              message[17] + ".", \
        'path_blocked':         message[18], \
        'path_clear':           message[19], \
        #miscelleanous messages
        'error':                message[24], \
        'wait_inst':            message[22] + ".",
        'process_done':         message[10] + ".", \
        'thankyou':             message[8] + ".", \
        'goodbye':              message[20] + "."}

def getAck():
        #to be done by Alvin/Jiayi
        return 1

def getYNInput():
        print message_str['yn_inst']
        voiceOut('yn_inst')
        ser.write("!")
        yn_response = ''
        while (not yn_response):
                yn_response = ser.readline()
        return yn_response

def getLocationInput():
        ser.write(">")
        response = ''
        while (not response):
                response = ser.readline()
        return response

def updateDictionaryValues(new_value, update_field):
        if (update_field == 'startloc'):
                for x in range (0,4):
                        startloc[x] = new_value[x]
                print startloc
                del message[64]
                del message_str['confirm_startloc']
                message[64] = '|'.join(startloc)
                message_str['confirm_startloc'] = message[3] + " " + message[64] + " " + \
                        message[4] + " " + message[31] + ". " + message[5]

        elif (update_field == 'dest'):
                for x in range(0,4):
                        dest[x] = new_value[x]
                print dest
                del message[65]
                del message_str['confirm_dest']
                message[65] = '|'.join(dest)
                message_str['confirm_dest'] = message[3] + " " + message[65] + " " + \
                        message[4] + " " + message[32] + ". " + message[5]

        else:
                print ('****ERROR IN UPDATING VALUES****')
                return 0
        return 1

def YNHandler(yn_response):
        if (yn_response[0] == '1'):
                print message_str['confirm_yes']
                voiceOut('confirm_yes')
                return 1

        else:
                print message_str['confirm_no']
                voiceOut('confirm_no')
                return 0

def voiceOut(messagetype):
        p = subprocess.Popen(syntax_head + volume + variation['female1'] + " '" + \
                message_str[messagetype] + syntax_tail,
                shell=True, stdout=subprocess.PIPE, ) # This runs the process on a separte process from the main. DO NOT call this too many times.

        # os.system(syntax_head + volume + variation['female1'] + " '" + \
        #         message_str[messagetype] + syntax_tail)
        return

try:
        if getAck():
                while 1:
                        #on startup
                        print message_str['startup']
                        voiceOut('startup')

                        #get starting location and update values in dictionary
                        response = getLocationInput()
                        if (updateDictionaryValues(response, 'startloc')):
                                print message_str['confirm_startloc']
                                voiceOut('confirm_startloc')
                                yn_response = getYNInput()

                                if (YNHandler(yn_response)):
                                        break
                while 1:
                        print message_str['get_dest']
                        voiceOut('get_dest')
                        response = getLocationInput()

                        if (updateDictionaryValues(response, 'dest')):
                                print message_str['confirm_dest']
                                voiceOut('confirm_dest')
                                yn_response = getYNInput()

                                if (YNHandler(yn_response)):
                                        print message_str['cali_header']
                                        voiceOut('cali_header')
                                        break

                ####### NOT COMPLETED. TO DO: GET DATA FROM SENSORS AND SEND BACK #########
                print message_str['cali_inst1']
                voiceOut('cali_inst1')
                time.sleep(2) #time delay to simulate sensor calibration
                print message_str['cali_inst2']
                voiceOut('cali_inst2')
                time.sleep(2)

                print message_str['path_calc']
                voiceOut('path_calc')
                print message_str['wait_inst']
                voiceOut('wait_inst')
                time.sleep(2) #time delay to simulate path calculation
                ###########################################################################

                print message_str['process_done']
                voiceOut('process_done')

                ####### USE LIST TO GIVE INSTRUCTIONS   #######
                ## 0 - turn left                             ##
                ## 1 - go straight                           ##
                ## 2 - turn right                            ##
                ## 3 - destination arrived                   ##
                ## 4 - open door on left                     ##
                ## 5 - open door in front                    ##
                ## 6 - open door on right                    ##
                ## 7 - climb up stairs                       ##
                ## 8 - climb down stairs                     ##
                ## 9 - end of stairs                         ##
                ## everytime the user changes level,         ##
                ## generate a new directions list.           ##
                ###############################################
                ## INCOMPLETE: incorporate number of steps before turning left ##
                directions_list = [0, 1, 2, 3, 4, 5, 6]
                for x in directions_list:
                        if x == 0:
                                print message_str['left']
                                voiceOut('left')
                        elif x == 1:
                                print message_str['straight']
                                voiceOut('straight')
                        elif x == 2:
                                print message_str['right']
                                voiceOut('right')
                        elif x == 3:
                                print message_str['dest_arrived']
                                voiceOut('dest_arrived')
                        elif x == 4:
                                print message_str['door_left']
                                voiceOut('door_left')
                        elif x == 5:
                                print message_str['door_front']
                                voiceOut('door_front')
                        elif x == 6:
                                print message_str['door_right']
                                voiceOut('door_right')
                        elif x == 7:
                                print message_str['stairs_a']
                                voiceOut('stairs_a')
                        elif x == 8:
                                print message_str['stairs_d']
                                voiceOut('stairs_d')
                        elif x == 9:
                                print message_str['stairs_end']
                                voiceOut('stairs_end')
                ##########################################################################


                ############################## OBJECT DETECTION ##########################
                # message strings have been prepared but waiting on alvin & jiayi for data structure

        else:
                print ('ACK FAILED')
except KeyboardInterrupt:
        ser.close()
        print message_str['error']
        voiceOut('error')
        print ('program stop')

