"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

'''
Calibration Points
|--------------------------------|
|0             1                2|
|3             4                5|
|6             7                8|
|--------------------------------|
'''

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

x_calib = []
y_calib = []
x_points = []
y_points = []

max_y = 480
max_x = 640

#subtract 10 on all max points to account for pixel size
calib_points = [(0,10), (max_x/2,10), (max_x-10, 10), (0, max_y/2), (max_x/2, max_y/2), (max_x-10, max_y/2), (0, max_y-10), (max_x/2, max_y-10), (max_x-10, max_y-10)]

frame_counter = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    #window dimensions are 640x480

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    x_ratio = gaze.horizontal_ratio()
    y_ratio = gaze.vertical_ratio()
    #cv2.putText(frame, "x ratio:  " + str(x_ratio), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    #cv2.putText(frame, "y ratio: " + str(y_ratio), (90, 235), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    if x_ratio is not None and y_ratio is not None:
        x_ratio = x_ratio * max_x
        y_ratio = y_ratio * max_y
        cv2.putText(frame, ".", (int(x_ratio), int(y_ratio)), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 10)


    if 30 <= frame_counter and frame_counter < 330:
        # prevent adding first empty list
        if frame_counter % 30 == 0 and frame_counter > 30:
            # add lists
            x_calib.append(x_points)
            y_calib.append(y_points)
            # reset lists for new points
            x_points = []
            y_points = []
        cv2.putText(frame, ".", (int(calib_points[(frame_counter//30) - 2][0]), int(calib_points[(frame_counter//30) - 2][1])), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 10)
        if x_ratio is not None and y_ratio is not None:
            x_points.append(x_ratio)
            y_points.append(y_ratio)
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
    if x_ratio is not None:
        frame_counter += 1
'''
for list in range(0, len(x_calib)):
    total = 0
    count = 0
    for point in x_calib[list]:
        total += point
        count += 1
    print('average for list ', list, ': ', str(total/count))'''

# get x min
total = 0
count = 0
# min x is at points 0, 3, 6
for list in range(0, 7, 3):
    for point in x_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average min x: ", str(total/count))

# get x mid
total = 0
count = 0
# mid x is at points 1, 4, 7
for list in range(1, 8, 3):
    for point in x_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average mid x: ", str(total/count))


# get x max
total = 0
count = 0
# max x is at points 2,5,8
for list in range(2, 9, 3):
    for point in x_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average max x: ", str(total/count))

# get y min
total = 0
count = 0
# min y is at points 0,1,2
for list in range(0, 3, 1):
    for point in y_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average min y: ", str(total/count))

# get y mid
total = 0
count = 0
# mid y is at points 3,4,5
for list in range(3, 6, 1):
    for point in y_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average mid y: ", str(total/count))


# get y max
total = 0
count = 0
# max y is at points 6,7,8
for list in range(6,9,1):
    for point in y_calib[list]:
        if point is not None:
            total += point
            count += 1
print(count)
print("average max y: ", str(total/count))

print("x points")
for list in x_calib:
    print(list)

print("y points")
for list in y_calib:
    print(list)

webcam.release()
cv2.destroyAllWindows()
