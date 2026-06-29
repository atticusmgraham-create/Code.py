import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

# 1. Audio configuration
FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()

# 2. Auto-detect default hardware microphone
try:
    device_info = p.get_default_input_device_info()
    DEVICE_INDEX = device_info['index']
    CHANNELS = 1 if device_info['maxInputChannels'] >= 1 else int(device_info['maxInputChannels'])
    print(f"--> Audio Device Found: {device_info['name']}")
    print(f"--> Channels: {CHANNELS} | Sample Rate: {RATE}")
except IOError:
    print("CRITICAL ERROR: No audio input devices found. Is your mic plugged in?")
    p.terminate()
    sys.exit(1)

# 3. Open hardware stream
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

# 4. Set up the Matplotlib window structure
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=2, color='teal')

# Setup graph boundaries
ax.set_ylim(-16000, 16000)  
ax.set_xlim(0, CHUNK)
ax.set_title("Live Audio Waveform Visualizer")
ax.set_xlabel("Audio Samples")
ax.set_ylabel("Amplitude")
plt.grid(True)

# 5. Core update loop managed by Matplotlib animation framework
def update_plot(frame):
    try:
        # Read the raw byte data from mic (non-blocking overflow protection)
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # If the microphone defaults to stereo channel, slice it down to mono
        if CHANNELS > 1:
            audio_data = audio_data[::CHANNELS]
            
        # Prevent length mismatches from breaking the plot array size
        if len(audio_data) < CHUNK:
            audio_data = np.pad(audio_data, (0, CHUNK - len(audio_data)), 'constant')

        # Push data to the graphic line object
        line.set_ydata(audio_data)
        
    except Exception as e:
        print(f"Warning during loop read: {e}")
        
    return line, # Return trailing comma for blitting tracking

# 6. Initialize Native Animation (Interval=1ms triggers loop as fast as possible)
# blit=True lets the internal Matplotlib engine cleanly optimize redraws
ani = animation.FuncAnimation(
    fig, 
    update_plot, 
    interval=1, 
    blit=True, 
    cache_frame_data=False
)

print("\nDisplaying live graph. Close the graphic window to stop cleanly.")
plt.show()

# 7. Safe fallback termination loop if user closes window
print("Closing stream resources...")
try:
    stream.stop_stream()
    stream.close()
except Exception:
    pass
p.terminate()
print("Audio resources released.")
