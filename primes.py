import math

def pure_python_li(x, steps=100000):
    if x <= 2:
        return 0
    
    total_area = 0.0
    start = 2.0
    width = (x - start) / steps
    
    for i in range(steps):
        # Evaluate density at the midpoint of each slice
        t = start + (i + 0.5) * width
        total_area += (1 / math.log(t)) * width
        
    return total_area

print()  # Outputs: 177
