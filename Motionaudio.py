import cv2
import imutils
import time
import requests
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import subprocess
import os
from gpiozero import Buzzer

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = ""
MIC_DEVICE_ID = 1
NOTIFICATION_COOLDOWN = 15
RECORD_DURATION = 5
FPS = 10.0

AUDIO_THRESHOLD = 0.04
AUDIO_WINDOW = 0.2
# ---------------------

buzzer = Buzzer(1)

# --- AUDIO SETUP ---
def get_supported_sample_rate(device_id):
    rates = [16000, 48000, 44100, 32000, 8000]
    for r in rates:
        try:
            sd.check_input_settings(device=device_id, samplerate=r, channels=1)
            print(f"[INFO] Using sample rate: {r}")
            return r
        except:
            continue
    raise RuntimeError("No valid sample rate found")

SAMPLE_RATE = get_supported_sample_rate(MIC_DEVICE_ID)


def get_audio_level(device_id, samplerate):
    recording = sd.rec(
        int(AUDIO_WINDOW * samplerate),
        samplerate=samplerate,
        channels=1,
        device=device_id,
        dtype='float32'
    )
    sd.wait()
    return float(np.sqrt(np.mean(recording**2)))  # RMS


# --- CAMERA SETUP ---
camera = cv2.VideoCapture(0)
time.sleep(2.0)

first_frame = None
last_notification_time = 0

print("[INFO] Security system active. Press 'q' to quit.")

# --- MAIN LOOP ---
while True:
    grabbed, frame = camera.read()
    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    # --- MOTION DETECTION ---
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

    # --- AUDIO DETECTION ---
    try:
        audio_level = get_audio_level(MIC_DEVICE_ID, SAMPLE_RATE)
        audio_event = audio_level > AUDIO_THRESHOLD
    except:
        audio_level = 0
        audio_event = False

    # --- DISPLAY DEBUG ---
    cv2.putText(frame,
                f"Audio: {audio_level:.3f}",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2)

    # --- BUZZER ---
    if motion_detected or audio_event:
        buzzer.on()
    else:
        buzzer.off()

    # --- TRIGGER LOGIC ---
    current_time = time.time()

    if (motion_detected or audio_event) and \
       (current_time - last_notification_time > NOTIFICATION_COOLDOWN):

        last_notification_time = current_time

        if motion_detected and audio_event:
            print("[ALERT] MOTION + AUDIO (HIGH CONFIDENCE)")
        elif motion_detected:
            print("[ALERT] MOTION ONLY")
        else:
            print("[ALERT] AUDIO ONLY")

        print(f"[INFO] Recording {RECORD_DURATION}s clip...")

        temp_video = "temp_video.avi"
        temp_audio = "temp_audio.wav"
        final_output = "security_alert.mp4"

        h, w, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_video = cv2.VideoWriter(temp_video, fourcc, FPS, (w, h))

        audio_recording = sd.rec(
            int(RECORD_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            device=MIC_DEVICE_ID,
            dtype='int16'
        )

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
        sd.wait()

        wavfile.write(temp_audio, SAMPLE_RATE, audio_recording)

        # Merge audio + video
        print("[INFO] Merging media...")
        ffmpeg_cmd = f"ffmpeg -y -i {temp_video} -i {temp_audio} -c:v libx264 -c:a aac -preset ultrafast {final_output}"
        subprocess.run(ffmpeg_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Upload to Discord
        print("[INFO] Uploading...")
        try:
            with open(final_output, "rb") as f:
                requests.post(
                    DISCORD_WEBHOOK_URL,
                    data={"content": "🚨 Motion + Audio Event Detected"},
                    files={"file": f}
                )
        except Exception as e:
            print("[ERROR] Upload failed:", e)

        # Cleanup
        for file in [temp_video, temp_audio, final_output]:
            if os.path.exists(file):
                os.remove(file)

    # --- SHOW WINDOWS ---
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Motion Mask", thresh)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
