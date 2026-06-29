import cv2

# Initialize the webcam (usually 0 if it's the only camera connected)
cap = cv2.VideoCapture(0)

# Set resolution to 720p (1280x720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Optional: Set the framerate to 30 FPS
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press 'q' to quit the live feed window.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Display the resulting frame in a window
    cv2.imshow('Logitech 720p Live Feed', frame)

    # Break the loop when 'q' is pressed on the keyboard
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
