import cv2

tracker = cv2.TrackerMedianFlow_create()
counter = 0
above_line = 1

#tracker = ask_for_tracker()
tracker_name = str(tracker).split()[0][1:]

# Read video
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("david5.mp4")

# Read first frame.
ret, frame = cap.read()

# Set Up the Initial Tracking Window
# We will first detect the face and set that as our starting box.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_rects = face_cascade.detectMultiScale(frame)

# Convert this list of a single array to a tuple of (x,y,w,h)
(face_x, face_y, w, h) = tuple(face_rects[0])
track_window = (face_x, face_y, w, h)
# set up the ROI for tracking
roi = (face_x, face_y-20, face_x + 15, face_y + 20)

## setting a bar
if face_y > 350:
    line_height=350
else:
    line_height=face_y+150

# Special function allows us to draw on the very first frame our desired ROI
#roi = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ret = tracker.init(frame, roi)

while True:
    # Read a new frame
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
        p2 = (x+w-10, y+h-10)
        cv2.rectangle(frame, p1, p2, (255,0,0), 2)
    else :
        # Tracking failure
        cv2.putText(frame, "Failure to Detect Tracking!!", (100,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)

    # Setting counter

    if y < line_height:
        above_line = 1
        position = "Above"
    if y > line_height:
        position = "Under"

    if (above_line == 1) and (y > line_height):
        above_line = 0
        counter = counter + 1


    # Line
    img2 = cv2.line(frame, pt1=(0, line_height), pt2=(640, line_height), color=(0, 255, 0), thickness=3)

    # Title
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text=str(counter), org=(10, 400), fontFace=font, fontScale=4, color=(0, 255, 0), thickness=3,
                lineType=cv2.LINE_AA)
    cv2.putText(frame, text=str(position), org=(500, 400), fontFace=font, fontScale=1, color=(255, 0, 0),
                thickness=3, lineType=cv2.LINE_AA)





    # Display result
    cv2.imshow(tracker_name, frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 :
        break

cap.release()
cv2.destroyAllWindows()
