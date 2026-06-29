import pyaudio
import numpy as np

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE_INDEX = 1   # Set this to your monitor's card number from arecord -l

# Set your trigger threshold for live noise
NOISE_THRESHOLD = 500.0  

p = pyaudio.PyAudio()

# Open stream to read live data from the microphone
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=DEVICE_INDEX,
                frames_per_buffer=CHUNK)

print("Monitoring live room noise...")

try:
    while True:
        # Read raw data directly from the microphone stream
        data = stream.read(CHUNK, exception_on_overflow=False)
        
        # Convert live data to a math-friendly format
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate current sound volume level
        volume = np.sqrt(np.mean(audio_data**2))
        
        # Trigger an action based on live noise
        if volume > NOISE_THRESHOLD:
            print(f"Noise detected! Volume level: {volume:.2f}")
            # You can add code here to trigger an LED or external action

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()
