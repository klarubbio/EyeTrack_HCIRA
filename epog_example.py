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
import gaze_tracking as gt

# setup_epog expects max two args, both optional,
# sets up webcam, and calibration windows
test_error_dir = '../GazeEvaluation/test_errors/'
epog = gt.EPOG(test_error_dir, sys.argv)

# webcam = cv2.VideoCapture(0)
circle_rad = 20



monitor = epog.monitor
fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)



gestures = ['triangle', 'x', 'rectangle', 'circle', 'check', 'caret', 'zigzag', 'arrow', 'left_square_bracket', 'right_square_bracket', 'v', 'delete', 'left_curly_brace', 'right_curly_brace', 'star', 'pigtail']
rand_gestures = []
# list of 10 of each shape
for i in range(0,10):
    for shape in gestures:
        rand_gestures.append(shape)

gesture_images = {}
for gesture in gestures:
    gesture_images[gesture] = cv2.imread(gesture+'.png',0)

# create empty dictionary for points to parse to xml later
template_map = {}
for shape in gestures:
    template_map[shape] = []

counter = 0
nonnone_frames = 0
curr_gesture = ""
points = []

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
        # Use gaze projected onto screen surface
        # Screen coords will be None for a few initial frames,
        # before calibration and tests have been completed
        if screen_x is not None and screen_y is not None:
            nonnone_frames += 1
            text = "Looking at point {}, {} on the screen".format(screen_x, screen_y)
            
            epog.test_error_file.write("str(screen_x): ")
            epog.test_error_file.write(str(screen_x))

            # cv2.circle(frame, (screen_x, screen_y), circle_rad // 4, (170, 170, 170), -1)
            if keyboard.is_pressed('a'): # polling for input is causing a serious lag
                points.append((screen_x,screen_y))
            else:
                # draw line of all points
                if len(points) > 0:
                    for i in range(1, len(points)):
                        cv2.line(fullscreen_frame, (points[i-1][0], points[i-1][1]), (points[i][0], points[i][1]), (170,170,170), 1)
                        cv2.imshow(epog.calib_window, fullscreen_frame)
                        cv2.waitKey(1)
#
        #                if max > 1:
 #                   cv2.line(fullscreen_frame, (points[max - 2][0], points[max - 2][1]), (points[max - 1][0], points[max - 1][1]), (170, 170, 170), 1)
  #                  cv2.imshow(epog.calib_window, fullscreen_frame)
   #                 cv2.waitKey(1)
        # cv2.imshow(epog.calib_window, frame)
        # cv2.putText(frame, text, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 10)
        # print(text)
        # Press Esc to quit the video analysis loop
        if keyboard.is_pressed('n'):
            # clear off screen and handle old points
            fullscreen_frame = np.zeros((monitor['height'], monitor['width'], 3), np.uint8)
            if len(points) > 0:
                # add to template map
                template_map[curr_gesture].append(points)
            points = []
            # get next gesture to display and remove that item from possible gestures list
            if len(rand_gestures) > 0:
                remove_index = random.randint(0,len(rand_gestures)-1)
                curr_gesture = rand_gestures[remove_index]
                cv2.imshow(epog.calib_window, gesture_images[curr_gesture])
                cv2.putText(fullscreen_frame, curr_gesture, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,255,0), 1)
                # cv2.imshow(epog.calib_window, fullscreen_frame)
                rand_gestures.pop(remove_index)



        if cv2.waitKey(1) == 27:
            # Release video capture
            epog.webcam.release()
            cv2.destroyAllWindows()
            print(len(points))
            print(counter)
            print(nonnone_frames)
            print(template_map)
            break

        
        #elif wait == 39:
        #    print("next")
        # Note: The waitkey function is the only method in HighGUI that can fetch and handle events,
        # so it needs to be called periodically for normal event processing unless HighGUI
        # is used within an environment that takes care of event processing.
        # Note: The waitkey function only works if there is at least one HighGUI window created and
        # the window is active. If there are several HighGUI windows, any of them can be active.
        # (https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html)
