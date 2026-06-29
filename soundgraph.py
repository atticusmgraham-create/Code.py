import os
import sys
import numpy as np

# 1. Silence messy ALSA warning logs in the terminal
os.environ['ALSA_LOG_LEVEL'] = 'none'
sys.stderr = open(os.devnull, 'w')
import pyaudio
import matplotlib.pyplot as plt
sys.stderr = sys.__stderr__  # Restore standard error stream

# 2. Audio configuration defaults
FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()

# 3. Safely auto-detect the best input device and its hardware channels
try:
    device_info = p.get_default_input_device_info()
    DEVICE_INDEX = device_info['index']
    CHANNELS = 1 if device_info['maxInputChannels'] >= 1 else int(device_info['maxInputChannels'])
    print(f"Connected to: {device_info['name']}")
    print(f"Configured Channels: {CHANNELS} | Sample Rate: {RATE}")
except IOError:
    print("Error: No working audio input devices found. Please check your mic connection.")
    p.terminate()
    sys.exit(1)

# 4. Initialize hardware audio stream
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

# 5. Set up the Matplotlib plot structure
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=2, color='teal')

# Graph aesthetics (16-bit audio limits clipping ranges)
ax.set_ylim(-15000, 15000)  
ax.set_xlim(0, CHUNK)
ax.set_title("Live Audio Waveform Visualizer")
ax.set_xlabel("Audio Samples")
ax.set_ylabel("Amplitude")
plt.grid(True)

print("\nDisplaying live graph. Close the window or press Ctrl+C to stop.")

try:
    # Activate interactive mode and render the initial window frame
    plt.ion()
    plt.show()
    fig.canvas.draw()
    
    # Cache background details for fast blit refreshing
    background = fig.canvas.copy_from_bbox(ax.bbox)
    
    while plt.fignum_exists(fig.number):
        # Read raw stream data safely buffer handling overflows
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # If stereo hardware fallback, extract only the first channel
        if CHANNELS > 1:
            audio_data = audio_data[::CHANNELS]
            
        # Handle zero padding if data chunk sizes mismatch
        if len(audio_data) < CHUNK:
            audio_data = np.pad(audio_data, (0, CHUNK - len(audio_data)), 'constant')

        # Fast UI Update (Blitting avoids re-drawing the whole window)
        fig.canvas.restore_region(background)
        line.set_ydata(audio_data)
        ax.draw_artist(line)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()

except KeyboardInterrupt:
    print("\nStopping graph execution...")

finally:
    # 6. Secure resource release
    try:
        stream.stop_stream()
        stream.close()
    except Exception:
        pass
    p.terminate()
    plt.close('all')
    print("Audio resources released cleanly.")
