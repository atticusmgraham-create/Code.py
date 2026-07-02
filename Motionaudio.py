import cv2
import imutils
import time
import requests
import numpy as np
import subprocess
import os
from gpiozero import Buzzer

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = ""
NOTIFICATION_COOLDOWN = 15
RECORD_DURATION = 5
FPS = 10.0

# Sensitivity (tune these)
BRIGHTNESS_THRESHOLD = 6.0
COLOR_THRESHOLD = 12.0
# ---------------------

buzzer = Buzzer(1)

# --- CAMERA SETUP ---
camera = cv2.VideoCapture(0)
time.sleep(2.0)

prev_gray = None
prev_color = None

last_notification_time = 0

print("[INFO] Brightness + Color monitoring active. Press 'q' to quit.")

# --- MAIN LOOP ---
while True:
    grabbed, frame = camera.read()
    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # --- INITIAL BASELINE ---
    if prev_gray is None:
        prev_gray = gray
        prev_color = frame.astype("float32")
        continue

    # --- BRIGHTNESS CHANGE ---
    curr_brightness = np.mean(gray)
    prev_brightness = np.mean(prev_gray)
    brightness_change = abs(curr_brightness - prev_brightness)

    # --- COLOR CHANGE ---
    color_diff = np.abs(frame.astype("float32") - prev_color)
    color_change = np.mean(color_diff)

    # --- UPDATE BASELINE (slow adaptation) ---
    prev_gray = gray
    prev_color = frame.astype("float32")

    # --- DETECTION FLAGS ---
    brightness_event = brightness_change > BRIGHTNESS_THRESHOLD
    color_event = color_change > COLOR_THRESHOLD

    # --- DEBUG DISPLAY ---
    cv2.putText(frame,
                f"B:{brightness_change:.2f} C:{color_change:.2f}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2)

    # --- BUZZER ---
    if brightness_event or color_event:
        buzzer.on()
    else:
        buzzer.off()

    # --- TRIGGER LOGIC ---
    current_time = time.time()

    if (brightness_event or color_event) and \
       (current_time - last_notification_time > NOTIFICATION_COOLDOWN):

        last_notification_time = current_time

        if brightness_event and color_event:
            print("[ALERT] BRIGHTNESS + COLOR CHANGE (HIGH CONFIDENCE)")
        elif brightness_event:
            print("[ALERT] BRIGHTNESS CHANGE ONLY")
        else:
            print("[ALERT] COLOR CHANGE ONLY")

        print(f"[INFO] Recording {RECORD_DURATION}s clip...")

        temp_video = "temp_video.avi"
        final_output = "security_alert.mp4"

        h, w, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_video = cv2.VideoWriter(temp_video, fourcc, FPS, (w, h))

        start_record = time.time()
        frame_delay = 1.0 / FPS

        while time.time() - start_record < RECORD_DURATION:
            loop_start = time.time()

            _, record_frame = camera.read()
            record_frame = imutils.resize(record_frame, width=500)

            out_video.write(record_frame)
            cv2.imshow("Security Feed", record_frame)

            cv2.waitKey(1)

            elapsed = time.time() - loop_start
            if elapsed < frame_delay:
                time.sleep(frame_delay - elapsed)

        out_video.release()

        # --- Upload to Discord ---
        print("[INFO] Uploading to Discord...")
        try:
            with open(temp_video, "rb") as f:
                requests.post(
                    DISCORD_WEBHOOK_URL,
                    data={"content": "🚨 Brightness/Color Change Detected"},
                    files={"file": f}
                )
        except Exception as e:
            print("[ERROR] Upload failed:", e)

        # --- Cleanup ---
        if os.path.exists(temp_video):
            os.remove(temp_video)

    # --- SHOW WINDOWS ---
    cv2.imshow("Security Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
