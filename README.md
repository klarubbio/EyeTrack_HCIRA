# Gaze Tracking

## HCIRA Readme Additions

### Experiment Materials
Link to blank consent form: https://docs.google.com/document/d/10IjtLXyvzft5OG96urfVnebuaI2phEeTElu0puQOOmg/edit?usp=sharing
Link to presentation slides: https://docs.google.com/presentation/d/1VPq9PACX7IiaSyJCXtRrTWGbEi9IFgz1U7xL3Gs_81M/edit?usp=sharing

### Running the code
1. Follow the original instructions for installing dependencies.
2. Additional libraries that may need to be installed are keyboard, numpy, and random.
3. From the command prompt, run the app with the line "python epog_example.py 1 log". If the command line args aren't included, it is kinda bad. They explain below that 1 stabilizes the calibration clusters, and log is just the name for wherever you want debug messages to go.

### Instructions for using an external camera
1. Download the iVCam app on phone and on PC (https://www.e2esoft.com/ivcam/). 
2. Open both the phone app and computer app. Connect to the computer by pressing the plus button on the phone app and entering your computer's IP address.
3. Confirm that the video stream from the phone is connected to your computer. You can do this by opening the camera app on your computer and pressing the switch camera button to see the stream from your phone. 
4. Make sure that the scripts are configured to connect to the extra camera instead of the default camera. Anywhere that you see the code "cv2.VideoCapture(0)", it should be changed to "cv2.VideoCapture(1)". 
5. Run the app!

### Project 2
Rather than extending the recognizer's capabilities itself, this project evaluates its capacity to understand user gestures through a new modality: eye gaze. Gaze is ideal for unistroke gestures, as it is a continuous stream of data (excluding blinks or other moments when the eyes are not visible). This falls within the category of collecting a new dataset. The same sixteen unistroke gestures were performed for each participants, though it is expected that the data collection medium will render significant differences from the original experiment with mouse input. Due to the complexity of implementing gaze tracking without a dedicated eye tracker, numerous libraries and already-existing open source projects were utilized in this experiment: 
- OpenCV - https://opencv.org/ - This open-source library is widely used for computer vision, and is utilized in our case to detect the eyes and record their positions. 
- GazeTracking - https://github.com/antoinelame/GazeTracking - Our project is built entirely on top of this code base. The code leverages OpenCV to provide useful insights about eye gaze, such as iris position of each eye and the overall gaze ratio (horizontal and vertical). 
- GazeTracking - Calibrated - https://github.com/ritko/GazeTracking - This code base, which extends the previous repository, provides tools and calibration for mapping the eye gaze to an estimated point on the screen. Calibration helps assume the point of gaze by recording information about gaze at each corner of the screen. This was modified to ensure that 30 frames with gaze data exist for each calibration point, while the library previously would calibrate on a frame even if gaze was undetected. 

### Project 1 Part 1 Updates: Drawing on a canvas
- Set up a development environment - The data collection development environment is python run from the command line, with camera inputs. 
- Instantiating a canvas - setup_calib_window() in epog.py - The canvas is instantiated during the gaze calibration phase using the OpenCV library. This code was not written by me. 
- Listening for mouse or touch events - lines 123-136 in epog_example.py - Once calibration is complete, the program listens for "a" button presses, which indicate drawing. 
- Clearing the canvas - lines 139-148 in epog_example.py - The button press "c" clears the canvas and allows the user to start over. 

### Project 1 Part 2 updates: Online recognition
Not relevant as we did not reimplement online recognition.

### Project 1 Part 3 updates: offline recognition
Not relevant as we did not implement a new offline recognition test. Some minor changes to the already existing code acommodated any differences in the uploaded xml files. 

### Project 1 Part 4 Updates: Collecting Data from People
- Write gesture files - SendToXML() in epog_example.py - This function iterates through a data structure containing all the eye gaze points, and is called whenever the participant quits the application.
- Prompt for specific samples - lines 122-168 in epog_example.py - The next gesture is displayed when pressing "n". Users press the "a" button to indicate when they would like to draw. Once they release the "a" button, their gaze path is visualized. The delay avoids any distraction which could influence gaze. Users may clear their gesture and try again using the "c" button.
- Recruit 6 people - consent folder - Consent forms are available in the consent folder, and anonymous identifiers are in the xml folder. 
- Submit full dataset - see xml folder

### Project 1 Part 5 Updates: Exploring Data from People
- Run an offline recognition test - main.cpp - Recognition was conducted with minor updates to previously existing code. 
- Output the result - see output file
- Analyze dataset using ghost - see image
- Extract user articulation insights

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![GitHub stars](https://img.shields.io/github/stars/antoinelame/GazeTracking.svg?style=social)](https://github.com/antoinelame/GazeTracking/stargazers)

This is a Python (2 and 3) library that provides a **webcam-based eye tracking system**. It gives you the exact position of the pupils and the gaze direction, in real time.

[![Demo](https://i.imgur.com/WNqgQkO.gif)](https://youtu.be/YEZMk1P0-yw)

In addition, you can map pupil position onto screen coordinates, for example, to determine which window the user is looking at.

[![EPOG_demo](https://i.imgur.com/8LxBNQE.gif)](https://i.imgur.com/8LxBNQE.gif)
(See demo at https://i.imgur.com/8LxBNQE.gif)

User is fixating at the red dots on the screen. The small white dots mark the EPOG estimate.
## Installation

Clone this project:

```
git clone https://github.com/antoinelame/GazeTracking.git
```

In case you want to version handle this project in your own repo, you will need to use git-lfs to track the large .dat-file 
that is the trained face recognition model used for detecting facial landmarks. 
Install git-lfs: https://gitlab.ida.liu.se/help/workflow/lfs/manage_large_binaries_with_git_lfs.md

Install dependencies (NumPy, OpenCV, Dlib), as well as other dependencies:

```
pip install -r requirements.txt
```

> The Dlib library has four primary prerequisites: Boost, Boost.Python, CMake and X11/XQuartx. If you do not have them, you can [read this article](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/) to know how to easily install them.

In addition, if you want screen-size handling:
```
pip install pypiwin32  # for Windows
```
```
pip install pyobjc  # for MacOS
```
Screen-size handling in MacOS also requires AppKit, which is included in XCode.
```
pip install python3-xlib  # for Linux
```

Run the demo:

```
./epog_example.py
```

## Simple Demo

```python
#!/usr/bin/env python3


"""
Demonstration of how to use the eye point of gaze (EPOG) tracking library.

This example application can be called like this (both args are optional):
>> ./epog_example.py 1 'log_file_prefix'

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
import gaze_tracking as gt

# setup_epog expects max two args, both optional,
# sets up webcam, and calibration windows
test_error_dir = '../GazeEvaluation/test_errors/'
epog = gt.EPOG(test_error_dir, sys.argv)


while True:
    # We get a new frame from the webcam
    _, frame = epog.webcam.read()
    if frame is not None:
        # Analyze gaze direction and map to screen coordinates
        screen_x, screen_y = epog.analyze(frame)

        # Access gaze direction
        text = ""
        if epog.gaze_tr.is_right():
            text = "Looking right"
        elif epog.gaze_tr.is_left():
            text = "Looking left"
        elif epog.gaze_tr.is_center():
            text = "Looking center"

        # Use gaze projected onto screen surface
        # Screen coords will be None for a few initial frames,
        # before calibration and tests have been completed
        if screen_x is not None and screen_y is not None:
            text = "Looking at point {}, {} on the screen".format(screen_x, screen_y)

        # Press Esc to quit the video analysis loop
        if cv2.waitKey(1) == 27:
            # Release video capture
            epog.webcam.release()
            cv2.destroyAllWindows()
            break
        # Note: The waitkey function is the only method in HighGUI that can fetch and handle events,
        # so it needs to be called periodically for normal event processing unless HighGUI
        # is used within an environment that takes care of event processing.
        # Note: The waitkey function only works if there is at least one HighGUI window created and
        # the window is active. If there are several HighGUI windows, any of them can be active.
        # (https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html)

```

## Documentation

In the following examples, `gaze` refers to an instance of the `GazeTracking` class.

### Refresh the frame

```python
gaze.refresh(frame)
```

Pass the frame to analyze (numpy.ndarray). If you want to work with a video stream, you need to put this instruction in a loop, like the example above.

### Position of the left pupil

```python
gaze.pupil_left_coords()
```

Returns the coordinates (x,y) of the left pupil.

### Position of the right pupil

```python
gaze.pupil_right_coords()
```

Returns the coordinates (x,y) of the right pupil.

### Looking to the left

```python
gaze.is_left()
```

Returns `True` if the user is looking to the left.

### Looking to the right

```python
gaze.is_right()
```

Returns `True` if the user is looking to the right.

### Looking at the center

```python
gaze.is_center()
```

Returns `True` if the user is looking at the center.

### Horizontal direction of the gaze

```python
ratio = gaze.horizontal_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the horizontal direction of the gaze. The extreme right is 0.0, the center is 0.5 and the extreme left is 1.0.

### Vertical direction of the gaze

```python
ratio = gaze.vertical_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the vertical direction of the gaze. The extreme top is 0.0, the center is 0.5 and the extreme bottom is 1.0.

### Blinking

```python
gaze.is_blinking()
```

Returns `True` if the user's eyes are closed.

### Webcam frame

```python
frame = gaze.annotated_frame()
```

Returns the main frame with pupils highlighted.

## You want to help?

Your suggestions, bugs reports and pull requests are welcome and appreciated. You can also starring ⭐️ the project!

If the detection of your pupils is not completely optimal, you can send me a video sample of you looking in different directions. I would use it to improve the algorithm.

## Licensing

This project is released by Antoine Lamé under the terms of the MIT Open Source License. View LICENSE for more information.
