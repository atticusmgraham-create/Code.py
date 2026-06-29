import subprocess
import numpy as np

# Audio settings
RATE = "44100"
CHUNK_SIZE = 1024
THRESHOLD = 500.0  # Adjust based on room noise levels

# Launch the built-in system recorder silently and stream live data into Python
# -D hw:1,0 targets Card 1, Device 0. Adjust if your monitor is on a different card.
cmd = ["arecord", "-D", "hw:1,0", "-r", RATE, "-f", "S16_LE", "-c", "1", "-t", "raw", "-q"]

try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    print("Monitoring live room noise using built-in ALSA...")
    
    bytes_per_sample = 2  # 16-bit audio = 2 bytes
    read_size = CHUNK_SIZE * bytes_per_sample

    while True:
        # Pull live data directly out of the OS audio buffer
        raw_data = process.stdout.read(read_size)
        if not raw_data:
            break
            
        # Convert raw system bytes directly to integers
        audio_data = np.frombuffer(raw_data, dtype=np.int16)
        
        # Calculate real-time volume
        volume = np.sqrt(np.mean(audio_data**2))
        
        if volume > THRESHOLD:
            print(f"Noise detected! Volume: {volume:.2f}")

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
finally:
    process.terminate()
