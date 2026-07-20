import cv2
import imutils
import time
import requests
import sounddevice as sd
from scipy.io import wavfile
import subprocess
import os
import numpy as np
from gpiozero import Buzzer

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = ""
MIC_DEVICE_ID = 1          # Set to your webcam mic ID (e.g. 1 or "hw:1,0")
NOTIFICATION_COOLDOWN = 15  # Cooldown time in seconds between alerts
RECORD_DURATION = 5        # Duration of the captured video/audio clip in seconds
FPS = 10.0                 # Target frame rate for video recording
# ---------------------

buzzer = Buzzer(1)

# Function to auto-detect device sample rate
def get_supported_sample_rate(device_id):
    rates = [16000, 48000, 44100, 32000, 8000]
    for r in rates:
        try:
            sd.check_input_settings(device=device_id, samplerate=r, channels=1)
            print(f"[INFO] Using verified sample rate: {r} Hz")
            return r
        except Exception:
            continue
    raise RuntimeError("Could not find a supported sample rate for this microphone.")

# Auto-detect rate before starting
SAMPLE_RATE = get_supported_sample_rate(MIC_DEVICE_ID)

# Initialize the webcam
camera = cv2.VideoCapture(0)
time.sleep(2.0)  # Warm up sensor

first_frame = None
last_notification_time = 0

print("[INFO] Security Monitor active with Auto-Audio Capture. Press 'q' to quit.")

while True:
    grabbed, frame = camera.read()
    if not grabbed:
        print("[ERROR] Camera feed lost.")
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # Total pixels in a Logitech C270 frame (1280 x 720)
    
    if first_frame is None:
        first_frame = gray
        continue

    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 15, 255, cv2.THRESH_BINARY)[1]
    cpc=np.sum(thresh==255)
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

    if motion_detected:
        print("[ALERT] Movement detected!")
        buzzer.on()
        
        current_time = time.time()
        if current_time - last_notification_time > NOTIFICATION_COOLDOWN:
            last_notification_time = current_time
            print(f"[INFO] Recording {RECORD_DURATION}s clip...")
            
            temp_video = "temp_video.avi"
            temp_audio = "temp_audio.wav"
            final_output = "security_alert.mp4"
            
            # Setup video writer matching current frame dimensions
            h, w, _ = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out_video = cv2.VideoWriter(temp_video, fourcc, FPS, (w, h))
            
            # Start synchronous audio recording safely using auto-detected rate
            audio_recording = sd.rec(int(RECORD_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, device=MIC_DEVICE_ID, dtype='int16')
            
            # Precisely timed video loop
            start_record = time.time()
            frame_delay = 1.0 / FPS
            
            while time.time() - start_record < RECORD_DURATION:
                loop_start = time.time()
                _, record_frame = camera.read()
                record_frame = imutils.resize(record_frame, width=500)
                out_video.write(record_frame)
                
                cv2.imshow("Security Feed", record_frame)
                cv2.waitKey(1)
                
                # Sleep to maintain accurate frame rate pacing
                elapsed = time.time() - loop_start
                if elapsed < frame_delay:
                    time.sleep(frame_delay - elapsed)
                
            out_video.release()
            sd.wait()  # Complete audio recording array
            
            wavfile.write(temp_audio, SAMPLE_RATE, audio_recording)
            
            # Merge Video and Audio using FFmpeg CLI backend
            print("[INFO] Merging media tracks...")
            ffmpeg_cmd = f"ffmpeg -y -i {temp_video} -i {temp_audio} -c:v libx264 -c:a aac -preset ultrafast {final_output}"
            subprocess.run(ffmpeg_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Upload clip to Discord Webhook
            print("[INFO] Uploading alert clip to Discord...")
            try:
                with open(final_output, "rb") as video_file:
                    payload = {"content": "🚨 **Security Notice:** Motion detected with audio!"}
                    files = {"file": (final_output, video_file, "video/mp4")}
                    response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
                print(f"[SUCCESS] Discord Upload complete: Status {response.status_code}")
            except Exception as e:
                print(f"[ERROR] Failed uploading to Discord: {e}")
                
            # File system cleanup
            for file in [temp_video, temp_audio, final_output]:
                if os.path.exists(file):
                    os.remove(file)
    else:
        buzzer.off()
        
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh (Movement Mask)", thresh)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()


