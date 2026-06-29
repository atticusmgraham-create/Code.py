import cv2
import datetime

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ----------------------------------------------------
    # 1. ADD TEXT (String, Coordinates, Font, Scale, Color BGR, Thickness)
    # ----------------------------------------------------
    cv2.putText(frame, "LOGITECH 720P HD", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # ----------------------------------------------------
    # 2. ADD A DYNAMIC TIMESTAMP (Updates every frame)
    # ----------------------------------------------------
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, current_time, (50, 680), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # ----------------------------------------------------
    # 3. ADD SHAPES (Target Crosshair in the Center)
    # ----------------------------------------------------
    # Draw a bounding box/rectangle (Top-Left, Bottom-Right, Color, Thickness)
    cv2.rectangle(frame, (600, 320), (680, 400), (0, 0, 255), 2)
    
    # Draw a center dot (Center point, Radius, Color, Thickness [-1 fills it])
    cv2.circle(frame, (640, 360), 5, (0, 0, 255), -1)

    # Display the modified frame
    cv2.imshow('Camera with Overlays', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
