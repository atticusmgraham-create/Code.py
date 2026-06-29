import os
import struct
import sys

# Linux system file that aggregates all connected mice/touchpads
mouse_device = "/dev/input/mice"

print("Reading raw hardware mouse data... Press CTRL+C to exit.\n")

x_coord = 0
y_coord = 0

try:
    # Open the hardware device file in binary read mode
    with open(mouse_device, "rb") as f:
        while True:
            # Each standard mouse movement event sends exactly 3 bytes of data
            # Byte 1: Button clicks & status info
            # Byte 2: X-axis relative movement
            # Byte 3: Y-axis relative movement
            data = f.read(3)
            
            if not data:
                break
                
            # Unpack the 3 raw bytes as signed characters (integers from -128 to 127)
            status, delta_x, delta_y = struct.unpack('3b', data)
            
            # Add the relative hardware movement to your running totals
            x_coord += delta_x
            y_coord += delta_y
            
            # Print and format on a single self-overwriting line
            output = f"\rRaw X: {str(x_coord).ljust(6)} | Raw Y: {str(y_coord).ljust(6)}"
            sys.stdout.write(output)
            sys.stdout.flush()

except PermissionError:
    print("\nError: You must run this script with 'sudo' to read direct hardware files.")
except KeyboardInterrupt:
    print("\nTracking stopped.")
