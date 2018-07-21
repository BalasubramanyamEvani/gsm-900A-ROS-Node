#!/usr/bin/python
'''
@Author: Balasubramanyam Evani
Manipal University Jaipur

'''
## importing required libraries

import serial
import rospy
from gsm_900.msg import AT_CENG ## importing the custom Msg

## global variable output to store the incoming string from Arduino

output = " "

## Reads Serial Data from specified port
## Change the port if it is not at ttyACM0, type /dev/ttyACM* to see all

ser = serial.Serial('/dev/ttyACM0', 2400 , timeout = 5)

init = 0

## List initialization for storing cell numbers, received signal level and strength

cell_num = []
rec_level = []
rec_quality = []

first = 0

## flag var to check the cell num
flag = False

def process(output,publisher):
    global cell_num , rec_level , rec_quality , init , first , flag             ## define the global vars

    res = output[:-2]                                                           ## removing last two chars
    res = res.split(" ")                                                        ## splitting with space as delimiter
    if int(res[2]) == first:                                                    ## sometimes the connection gets lost, check again to see if it received the cell 0 first
        flag = True

    if int(res[2]) > 6:                                                         ## checks to see if cell num received is not greater than 6, because ony 6 cells are scanned,
                                                                                ## sometimes it may happen
        init = 0
        cell_num = []
        rec_level = []
        rec_quality = []
        pass

    if flag is True:                                                            ## if flag set to true,
                                                                                ## start appending the values
        cell_num.append(int(res[2]))
        rec_level.append(int(res[4]))
        rec_quality.append(int(res[6]))

        if len(cell_num) is 7 and len(rec_level) is 7 and len(rec_quality) is 7:## once all cells information received, publish

            new_msg = AT_CENG()                                                 ## create new msg object
            new_msg.header.stamp = rospy.Time.now()                             ## Adding header
            new_msg.header.frame_id = 'gsm_frame'
            new_msg.cell_num = cell_num
            new_msg.rec_level = rec_level
            new_msg.rec_quality = rec_quality
            publisher.publish(new_msg)
            ##  rospy.loginfo("New Msg Published")                              ## uncomment to see log info stating a new msg has been published
            cell_num = []                                                       ## once publisher publishes clear all lists, for new data
            rec_level = []
            rec_quality = []
            flag = False

    else:                                                                       ## flag set to false clear lists
        cell_num = []
        rec_level = []
        rec_quality = []
        init = 0
        pass

## Main Function

if __name__ == "__main__":

    rospy.init_node("gsm_data" , anonymous = True)                              ## Register Node with ROS master
    pub = rospy.Publisher("gsm_chatter" , AT_CENG , queue_size = 10)            ## initialization publisher
    rospy.loginfo("Registering GSM DATA publisher...")                          ## Logging info

    while True:                                                                 ## Reading data from serial port
      while output != "":
        output = ser.readline()
        if len(output) > 10:                                                    ## waits for 3 machine cycles till
            if output[10] == '0' and init < 3:                                  ## cell 0 is read for parsing purposes
                init = init + 1
                if init == 3:
                    process(output,pub)
            elif init >= 3:                                                     ## After 3 MC send the incoming data
                process(output,pub)                                             ## to be parsed and published
