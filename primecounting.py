import math

def evaluate_zeta(t, terms=200):
    """
    Computes zeta(0.5 + i*t) using the Dirichlet eta function.
    eta(s) = (1 - 2**(1-s)) * zeta(s)
    """
    # Define our complex test point s = 0.5 + i*t
    s_real = 0.5
    s_imag = t
    
    # 1. Compute the alternating sum for the Dirichlet eta function
    eta_real = 0.0
    eta_imag = 0.0
    
    for n in range(1, terms + 1):
        # Calculate n**(-s) = n**(-0.5) * [cos(t * ln(n)) - i * sin(t * ln(n))]
        ln_n = math.log(n)
        magnitude = 1.0 / math.sqrt(n)
        
        term_real = magnitude * math.cos(s_imag * ln_n)
        term_imag = -magnitude * math.sin(s_imag * ln_n)
        
        # Apply the alternating sign (-1)**(n-1)
        if n % 2 == 0:
            eta_real -= term_real
            eta_imag -= term_imag
        else:
            eta_real += term_real
            eta_imag += term_imag
            
    # 2. Convert the eta function back to the zeta function
    # factor = 1.0 - 2**(1 - s)
    # 1 - s = 0.5 - i*t
    factor_mag = math.sqrt(2.0)  # 2**0.5
    factor_angle = -s_imag * math.log(2.0)
    
    factor_real = 1.0 - factor_mag * math.cos(factor_angle)
    factor_imag = -factor_mag * math.sin(factor_angle)
    
    # Divide eta by the factor: zeta = eta / factor
    denominator = factor_real**2 + factor_imag**2
    
    zeta_real = (eta_real * factor_real + eta_imag * factor_imag) / denominator
    zeta_imag = (eta_imag * factor_real - eta_real * factor_imag) / denominator
    
    # Return the scalar distance from zero (magnitude)
    return math.sqrt(zeta_real**2 + zeta_imag**2)

def find_zero_bisection(t_start, t_end, tolerance=1e-5, max_steps=100):
    """
    Finds a local minimum (zero) of the zeta magnitude using gradient descent.
    Bisection normally requires a sign change, but magnitude is always positive.
    We binary-search the slope instead.
    """
    low = t_start
    high = t_end
    
    for _ in range(max_steps):
        mid = (low + high) / 2.0
        delta = 1e-6
        
        # Approximate the derivative (slope) of the magnitude curve
        val_left = evaluate_zeta(mid - delta)
        val_right = evaluate_zeta(mid + delta)
        slope = (val_right - val_left) / (2.0 * delta)
        
        if abs(slope) < tolerance and evaluate_zeta(mid) < 0.1:
            return mid
            
        if slope > 0:
            high = mid  # Zero is to the left
        else:
            low = mid   # Zero is to the right
            
    return (low + high) / 2.0

# Scan intervals for the first two non-trivial zeros
intervals = [
    (13.5, 14.5),  # Contains first zero (~14.134)
    (20.5, 21.5)   # Contains second zero (~21.022)
]

print("Calculating non-trivial zeros using pure Python mathematics:")
print("=" * 60)

for i, (start, end) in enumerate(intervals, 1):
    calculated_t = find_zero_bisection(start, end)
    magnitude = evaluate_zeta(calculated_t)
    
    print(f"Zero #{i}:")
    print(f"  Coordinates: s = 0.5 + {calculated_t:.4f}i")
    print(f"  Verification: |ζ(s)| = {magnitude:.6f}")
    print("-" * 60)
