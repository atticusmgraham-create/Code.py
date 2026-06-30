import cv2
import imutils
import time

# Initialize the Logitech USB camera (0 is usually the default web cam)
camera = cv2.VideoCapture(0)
time.sleep(2.0)  # Allow the camera sensor to warm up

first_frame = None

print("[INFO] Motion detection started. Press 'q' to quit.")

while True:
    # Grab the current frame
    grabbed, frame = camera.read()
    if not grabbed:
        print("[ERROR] Camera feed lost.")
        break

    # Resize frame, convert to grayscale, and blur it to smooth out noise
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize the first frame as the baseline background reference
    if first_frame is None:
        first_frame = gray
        continue

    # Compute absolute difference between current frame and reference frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes/gaps
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours (shapes) of the moving regions
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    motion_detected = False

    # Loop over the contours
    for contour in contours:
        # Ignore contours that are too small to filter out background noise
        if cv2.contourArea(contour) < 500:
            continue

        # Compute the bounding box for the contour and draw it on the frame
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True

    # Print log to console if movement is found
    if motion_detected:
        print("[ALERT] Movement detected!")

    # Show the live video streams
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh (Movement Mask)", thresh)

    # Clear the stream buffer and check if 'q' key is pressed to break loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Cleanup and close windows
camera.release()
cv2.destroyAllWindows()
