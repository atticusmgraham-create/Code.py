import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Audio Configuration (Built-in ALSA)
RATE = "44100"
CHUNK_SIZE = 1024
bytes_per_sample = 2  # 16-bit audio = 2 bytes
read_size = CHUNK_SIZE * bytes_per_sample

# Start the audio stream process
# Note: 'hw:1,0' targets Card 1. Change to 'hw:2,0' if your monitor is on card 2.
cmd = ["arecord", "-D", "hw:1,0", "-r", RATE, "-f", "S16_LE", "-c", "1", "-t", "raw", "-q"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# 2. Setup Matplotlib Plot
fig, ax = plt.subplots()
ax.set_title("Live Room Noise Volume")
ax.set_ylabel("Volume Level")
ax.set_xlabel("Time (Frames)")
ax.set_ylim(0, 3000)  # Adjust max height based on your mic sensitivity

# Data tracking for a scrolling window of the last 100 updates
max_data_points = 100
volume_history = [0] * max_data_points
line, = ax.plot(volume_history, color='blue', lw=2)

# 3. Animation Update Function
def update_graph(frame):
    global volume_history
    
    # Read live data bytes straight from the audio stream
    raw_data = process.stdout.read(read_size)
    if not raw_data:
        return line,
        
    # Convert bytes to numeric array and calculate volume
    audio_data = np.frombuffer(raw_data, dtype=np.int16)
    volume = np.sqrt(np.mean(audio_data**2))
    
    # Update history: drop oldest point, add newest volume point
    volume_history.pop(0)
    volume_history.append(volume)
    
    # Redraw the line data
    line.set_ydata(volume_history)
    return line,

# 4. Run the Live Animation
# interval=20 means the graph updates roughly every 20 milliseconds
ani = animation.FuncAnimation(fig, update_graph, blit=True, interval=20, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("\nClosing graph.")
finally:
    process.terminate()
