import numpy as np

# Total pixels in a Logitech C270 frame (1280 x 720)
TOTAL_PIXELS = 1280 * 720  # 921,600

# Set your code thresholds
MIN_CHANGE_PCT = 0.1
MAX_CHANGE_PCT = 48.0

def test_percentage_logic(changed_pixel_count, test_name):
    pct_changed = (changed_pixel_count / TOTAL_PIXELS) * 100
    
    print(f"--- Running: {test_name} ---")
    print(f"Simulated Changed Pixels: {changed_pixel_count:,}")
    print(f"Calculated Percentage: {pct_changed:.2f}%")
    
    if pct_changed > MAX_CHANGE_PCT:
        print("RESULT: 🔴 IGNORED: Object Too Large\n")
    elif pct_changed >= MIN_CHANGE_PCT:
        print("RESULT: 🟢 MOUSE DETECTED!\n")
    else:
        print("RESULT: ⚪ No Movement (Camera Static)\n")

# 1. Simulate standard camera static noise (e.g., 400 pixels changing)
test_percentage_logic(400, "Camera Static Noise Test")

# 2. Simulate a mid-range mouse moving (e.g., 9,000 pixels changing)
test_percentage_logic(9000, "Real Mouse Movement Simulation")

# 3. Simulate a giant human hand passing over lens (e.g., 600,000 pixels changing)
test_percentage_logic(600000, "Human Hand / Light Flash Simulation")
