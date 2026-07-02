import cv2
import imutils
import time
import requests
import numpy as np
import subprocess
import os
import sounddevice as sd
from scipy.signal import butter, lfilter

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = ""
NOTIFICATION_COOLDOWN = 15
RECORD_DURATION = 5
FPS = 10.0

BRIGHTNESS_THRESHOLD = 6.0
COLOR_THRESHOLD = 12.0

# AUDIO SETTINGS
AUDIO_WINDOW = 0.2
SAMPLE_RATE = 44100
RMS_THRESHOLD = 0.03
ENERGY_THRESHOLD = 0.0008
# ---------------------


# --- BANDPASS FILTER (300–3500 Hz) ---
def bandpass_filter(data, lowcut=300, highcut=3500, fs=44100, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)


# --- AUDIO DETECTION (RMS + FREQUENCY) ---
def get_audio_event():
    recording = sd.rec(
        int(AUDIO_WINDOW * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()

    audio = recording.flatten()

    # RMS (volume energy)
    rms = np.sqrt(np.mean(audio ** 2))

    # Frequency filtered energy
    filtered = bandpass_filter(audio, fs=SAMPLE_RATE)
    energy = np.sqrt(np.mean(filtered ** 2))

    return rms, energy, (rms > RMS_THRESHOLD and energy > ENERGY_THRESHOLD)


# --- CAMERA SETUP ---
camera = cv2.VideoCapture(0)
time.sleep(2.0)

prev_gray = None
prev_color = None

last_notification_time = 0

print("[INFO] Brightness + Color + Audio monitoring active. Press 'q' to quit.")

# --- MAIN LOOP ---
while True:
    grabbed, frame = camera.read()
    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # --- INIT BASELINE ---
    if prev_gray is None:
        prev_gray = gray
        prev_color = frame.astype("float32")
        continue

    # --- BRIGHTNESS CHANGE ---
    brightness_change = abs(np.mean(gray) - np.mean(prev_gray))

    # --- COLOR CHANGE ---
    color_change = np.mean(np.abs(frame.astype("float32") - prev_color))

    # --- AUDIO CHANGE ---
    try:
        rms, energy, audio_event = get_audio_event()
    except:
        rms, energy, audio_event = 0, 0, False

    # --- UPDATE BASELINE ---
    prev_gray = gray
    prev_color = frame.astype("float32")

    # --- EVENTS ---
    brightness_event = brightness_change > BRIGHTNESS_THRESHOLD
    color_event = color_change > COLOR_THRESHOLD

    # --- DEBUG DISPLAY ---
    cv2.putText(frame,
                f"B:{brightness_change:.2f} C:{color_change:.2f}",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2)

    cv2.putText(frame,
                f"RMS:{rms:.3f} ENG:{energy:.4f}",
                (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 100, 0),
                2)

    # --- TRIGGER LOGIC ---
    current_time = time.time()

    if (brightness_event or color_event or audio_event) and \
       (current_time - last_notification_time > NOTIFICATION_COOLDOWN):

        last_notification_time = current_time

        if audio_event and (brightness_event or color_event):
            print("[ALERT] VISUAL + AUDIO EVENT (HIGH CONFIDENCE)")
        elif audio_event:
            print("[ALERT] AUDIO EVENT ONLY")
        else:
            print("[ALERT] VISUAL CHANGE EVENT")

        print(f"[INFO] Recording {RECORD_DURATION}s clip...")

        temp_video = "temp_video.avi"

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

        # --- Upload ---
        print("[INFO] Uploading to Discord...")
        try:
            with open(temp_video, "rb") as f:
                requests.post(
                    DISCORD_WEBHOOK_URL,
                    data={"content": "🚨 Event detected (Light/Color/Audio)"},
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
