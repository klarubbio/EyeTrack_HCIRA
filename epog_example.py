#!/usr/bin/env python3


"""
Demonstration of how to use the eye point of gaze (EPOG) tracking library.

This example application can be called like this (both args are optional):
>> ./epog_example.py 1 'log_file_prefix'

Karina: running with param 1 is wayyyy better

'1': stabilize estimated EPOG w.r.t. previous cluster of EPOGs
'0': allow spurious EPOGs that deviate from cluster (default)

'log_file_prefix': (e.g. user_id) A logfile will be created with the errors, i.e.
the Euclidean distance (in pixels) between test points and corresponding estimated EPOGs.
Log file will be e.g. test_errors/'log_file_prefix'_stab_01-12-2019_18.36.44.txt
If log_file_prefix is omitted, log file will not be created.

Check the README.md for complete documentation.
"""

import sys
import cv2
import keyboard
import numpy as np
import random
import time
import gaze_tracking as gt
import xml.etree.ElementTree as ET


def sendToXML(map):

    # iterate through each shape
    for gesture in map:

        for rep in range(0, len(map[gesture])):
            filename = "./xml/" + gesture
            if rep < 10:
                filename += "0"
            filename += str(rep + 1)
            # set up file
            data = ET.Element('Gesture')
            data.set('Name', gesture)
            for point in map[gesture][rep]:
                pt = ET.SubElement(data, 'Point')
                pt.set('X', str(point[0]))
                pt.set('Y', str(point[1]))
                pt.set('T', str(0))
            out_xml = ET.tostring(data)
            filename += '.xml'
            with open(filename, 'wb') as f:
                f.write(out_xml)

# setup_epog expects max two args, both optional,
# sets up webcam, and calibration windows
test_error_dir = '../GazeEvaluation/test_errors/'
epog = gt.EPOG(test_error_dir, sys.argv)

# create empty screen for drawing
monitor = epog.monitor
fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)

# setup gestures for random selection
gestures = ['triangle', 'x', 'rectangle', 'circle', 'check', 'caret', 'zigzag', 'arrow', 'left_square_bracket', 'right_square_bracket', 'v', 'delete', 'left_curly_brace', 'right_curly_brace', 'star', 'pigtail']
rand_gestures = []
# list of 10 of each shape
for i in range(0,10):
    for shape in gestures:
        rand_gestures.append(shape)

# setup corresponding gesture images (should be in same directory as this file)
gesture_images = {}
for gesture in gestures:
    gesture_images[gesture] = cv2.imread(gesture+'.png',0)

# create empty dictionary for points to parse to xml later
template_map = {}
for shape in gestures:
    template_map[shape] = []

# some testing counter
counter = 0
nonnone_frames = 0
curr_gesture = ""
points = []

stop_delay = 0 # 5 second delay between button press and next button press

while True:
    # print("while loop ran")
    # We get a new frame from the webcam

    _, frame = epog.webcam.read()
    if frame is not None:
        counter += 1
        # Analyze gaze direction and map to screen coordinates
        screen_x, screen_y = epog.analyze(frame)
        '''
        # Access gaze direction
        text = ""
        if epog.gaze_tr.is_right():
            text = "Looking right"
        elif epog.gaze_tr.is_left():
            text = "Looking left"
        elif epog.gaze_tr.is_center():
            text = "Looking center"
        '''
        # Use gaze projected onto screen surface (only count if gaze is detected)
        # Screen coords will be None for a few initial frames,
        # before calibration and tests have been completed
        if screen_x is not None and screen_y is not None:
            nonnone_frames += 1
            text = "Looking at point {}, {} on the screen".format(screen_x, screen_y)

            epog.test_error_file.write("\nstr(screen_x): ")
            epog.test_error_file.write(str(screen_x))
            epog.test_error_file.write("\nstr(screen_y): ")
            epog.test_error_file.write(str(screen_y))

            # add points if user is pressing a
            if keyboard.is_pressed('a'):
                points.append((screen_x,screen_y))
            else:
                # draw line of all points when user releases a
                if len(points) > 0:
                    cv2.destroyWindow('Gesture')
                    for i in range(1, len(points)):
                        cv2.line(fullscreen_frame, (points[i-1][0], points[i-1][1]), (points[i][0], points[i][1]), (170,170,170), 1)
                        cv2.imshow(epog.calib_window, fullscreen_frame)
                        cv2.waitKey(1) # still not really sure what wait key does but seems to work ?

                    cv2.putText(fullscreen_frame, curr_gesture, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
                    cv2.putText(fullscreen_frame, 'gestures left: ' + str(len(rand_gestures)), (90, 230),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
                    cv2.putText(fullscreen_frame, 'press n for next', (900, 130),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
                    cv2.putText(fullscreen_frame, 'press c to try again', (900, 230),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)

                    cv2.imshow(epog.calib_window, fullscreen_frame)
                    cv2.waitKey(0)

        # clear screen and try again if user presses c
        if keyboard.is_pressed('c') and time.time() > stop_delay:
            stop_delay = time.time() + 5.0
            fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)
            # don't save last points
            if len(points) > 0:
                points = []
            fullscreen_frame = cv2.resize(gesture_images[curr_gesture], (800, 800))
            cv2.imshow('Gesture', fullscreen_frame)
            cv2.moveWindow('Gesture', round(monitor['width']/2.0 - 400), 0)
            cv2.waitKey(0)
            fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)
            cv2.putText(fullscreen_frame, 'press a to draw', (1300, 130),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
            cv2.putText(fullscreen_frame, 'trace the shape with your eyes,', (1300, 230),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(fullscreen_frame, 'starting at the dot', (1300, 280),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
            cv2.imshow(epog.calib_window, fullscreen_frame)
        # clear screen and move on, saving points if user presses n
        if keyboard.is_pressed('n') and time.time() > stop_delay:
            stop_delay = time.time() + 5.0
            # clear off screen and handle old points
            if len(points) > 0:
                # add to template map
                template_map[curr_gesture].append(points)
            points = []
            # get next gesture to display and remove that item from possible gestures list
            if len(rand_gestures) > 0:
                remove_index = random.randint(0,len(rand_gestures)-1)
                curr_gesture = rand_gestures[remove_index] # curr gesture is saved even if the screen is cleared (clearing does not use up additional gestures)
                # cv2.imshow(epog.calib_window, gesture_images[curr_gesture])
                # cv2.waitKey(1)
                # cv2.putText(fullscreen_frame, curr_gesture, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,255,0), 1)
                fullscreen_frame = cv2.resize(gesture_images[curr_gesture], (800, 800))
                cv2.imshow('Gesture', fullscreen_frame)
                cv2.moveWindow('Gesture', round(monitor['width'] / 2.0 - 400), 0)
                cv2.waitKey(0)
                fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)
                rand_gestures.pop(remove_index)
                cv2.putText(fullscreen_frame, 'press a to draw', (1250, 130),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
                cv2.putText(fullscreen_frame, 'trace the shape with your eyes,', (1200, 230),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(fullscreen_frame, 'starting at the dot', (1250, 280),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                cv2.imshow(epog.calib_window, fullscreen_frame)
                # cv2.putText(fullscreen_frame, 'gestures left: ' + str(len(rand_gestures)), (90, 230), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
            else:
                sendToXML(template_map)

        if cv2.waitKey(1) == 27:
            # Release video capture
            epog.webcam.release()
            cv2.destroyAllWindows()
            print(len(points))
            print(counter)
            print(nonnone_frames)
            print(template_map)
            sendToXML(template_map)
            break

        
        #elif wait == 39:
        #    print("next")
        # Note: The waitkey function is the only method in HighGUI that can fetch and handle events,
        # so it needs to be called periodically for normal event processing unless HighGUI
        # is used within an environment that takes care of event processing.
        # Note: The waitkey function only works if there is at least one HighGUI window created and
        # the window is active. If there are several HighGUI windows, any of them can be active.
        # (https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html)
