import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Audio stream configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DEVICE_INDEX = 0  # CHANGE THIS to your monitor's index number

p = pyaudio.PyAudio()

# Open connection to the monitor's microphone
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=DEVICE_INDEX,
                frames_per_buffer=CHUNK)

# Setup the matplotlib live graph
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(0, 2 * CHUNK, 2)  # X-axis points for 1024 samples
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=2, color='teal')

# Graph limits (16-bit audio ranges from -32768 to 32767)
ax.set_ylim(-15000, 15000)  
ax.set_xlim(0, CHUNK)
ax.set_title("Live Monitor Microphone Waveform")
ax.set_xlabel("Audio Samples")
ax.set_ylabel("Amplitude")
plt.grid(True)

print("Displaying live graph. Close the graph window or press Ctrl+C to stop.")

try:
    # Use plt.ion() for interactive real-time updating
    plt.ion()
    plt.show()
    
    while plt.fignum_exists(fig.number):
        # Read raw data and convert to 16-bit integers
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Update the graph line data
        line.set_ydata(audio_data)
        
        # Redraw the plot canvas
        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    print("\nStopping graph...")

finally:
    # Clean up hardware resources safely
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.close('all')
