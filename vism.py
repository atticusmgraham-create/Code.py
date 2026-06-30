import cv2
import imutils
import time
import requests
from datetime import datetime

# --- CONFIGURATION ---
# Paste your Discord Webhook URL below
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
# Minimum seconds to wait between sending alerts (prevents spamming your Discord channel)
ALERT_COOLDOWN_SECONDS = 10 
# ---------------------

camera = cv2.VideoCapture(0)
time.sleep(2.0)

first_frame = None
last_alert_time = 0

print("[INFO] Motion detection active. Sending alerts to Discord.")

while True:
    grabbed, frame = camera.read()
    if not grabbed:
        print("[ERROR] Camera feed lost.")
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True

    # Trigger alert if motion is detected and cooldown has passed
    current_time = time.time()
    if motion_detected and (current_time - last_alert_time > ALERT_COOLDOWN_SECONDS):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ALERT] Motion detected at {timestamp}! Sending to Discord...")
        
        # Prepare the text payload for Discord
        payload = {
            "content": f"🚨 **Motion Detected!**\nTime: `{timestamp}`"
        }
        
        try:
            # Send post request to Discord
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            if response.status_code == 240 or response.status_code == 204:
                last_alert_time = current_time
            else:
                print(f"[ERROR] Discord returned status code {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to send Discord alert: {e}")

    cv2.imshow("Security Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
