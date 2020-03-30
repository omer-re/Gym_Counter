import numpy as np
import cv2

# Capture a video stream
cap = cv2.VideoCapture(0)

# take first frame of the video
ret, frame = cap.read()

# initialize counter
counter = 0
above_line = 1
is_first_time=1
#position = "Above"

# Set Up the Initial Tracking Window
# We will first detect the face and set that as our starting box.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_rects = face_cascade.detectMultiScale(frame)

# Convert this list of a single array to a tuple of (x,y,w,h)
(face_x, face_y, w, h) = tuple(face_rects[0])
track_window = (face_x, face_y, w, h)
# set up the ROI for tracking
roi = frame[face_y:face_y + h, face_x:face_x + w]

# Use the HSV Color Mapping
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Find histogram to backproject the target on each frame for calculation of meanshit
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])

# Normalize the histogram array values given a min of 0 and max of 255
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

tracker = cv2.TrackerMedianFlow_create()
ret = tracker.init(frame, roi)
while True:
    ret, frame = cap.read()

    # Update tracker
    success, roi = tracker.update(frame)

    # roi variable is a tuple of 4 floats
    # We need each value and we need them as integers
    (x,y,w,h) = tuple(map(int,roi))

     # Draw Rectangle as Tracker moves
    if success:
        # Tracking success
        p1 = (x, y)
        p2 = (x+w, y+h)
        cv2.rectangle(frame, p1, p2, (0,255,0), 3)
    else :
        # Tracking failure
        cv2.putText(frame, "Failure to Detect Tracking!!", (100,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)


    if is_first_time:
        if y > 350:
            line_height=350
    else:
        line_height=y+100
        is_first_time=0

    # Setting counter

    if y < line_height:
        above_line = 1
        position = "Above"
    if y > line_height:
        position = "Under"

    if (above_line == 1) and (y > line_height):
        above_line = 0
        counter = counter + 1




    # Face rect
    img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # Line
    img2 = cv2.line(frame, pt1=(0, line_height), pt2=(640, line_height), color=(0, 255, 0), thickness=3)

    # Title
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text=str(counter), org=(10, 400), fontFace=font, fontScale=4, color=(0, 255, 0), thickness=3,
                lineType=cv2.LINE_AA)
    cv2.putText(frame, text=str(position), org=(200, 400), fontFace=font, fontScale=2, color=(255, 0, 0),
                thickness=3, lineType=cv2.LINE_AA)

    cv2.imshow('img2', img2)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

    else:
        break

cv2.destroyAllWindows()
cap.release()
