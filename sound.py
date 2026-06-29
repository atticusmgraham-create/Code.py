import sounddevice as sd
import numpy as np

# Audio configuration
DURATION = 0.1  # Check the microphone every 0.1 seconds
RATE = 44100    # Standard sampling rate
NOISE_THRESHOLD = 0.05  # Sensitivity threshold (0.0 to 1.0)

print("Monitoring live room noise using sounddevice...")

try:
    while True:
        # Capture live audio snapshot directly into a numpy array
        recording = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1, dtype='float32')
        sd.wait()  # Wait until the 0.1-second snapshot finishes
        
        # Calculate live noise volume level
        volume = np.sqrt(np.mean(recording**2))
        
        # Trigger when live noise crosses the threshold
        if volume > NOISE_THRESHOLD:
            print(f"Noise detected! Level: {volume:.4f}")

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
