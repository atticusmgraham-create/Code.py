import math

def riemann_siegel_z(t, terms=300):
    """Computes the real-valued Z(t) function."""
    eta_real, eta_imag = 0.0, 0.0
    for n in range(1, terms + 1):
        ln_n = math.log(n)
        magnitude = 1.0 / math.sqrt(n)
        term_real = magnitude * math.cos(t * ln_n)
        term_imag = -magnitude * math.sin(t * ln_n)
        if n % 2 == 0:
            eta_real -= term_real; eta_imag -= term_imag
        else:
            eta_real += term_real; eta_imag += term_imag

    factor_mag = math.sqrt(2.0)
    factor_angle = -t * math.log(2.0)
    factor_real = 1.0 - factor_mag * math.cos(factor_angle)
    factor_imag = -factor_mag * math.sin(factor_angle)
    denom = factor_real**2 + factor_imag**2
    zeta_real = (eta_real * factor_real + eta_imag * factor_imag) / denom
    zeta_imag = (eta_imag * factor_real - eta_real * factor_imag) / denom

    if t > 0:
        theta = t * math.log(t / (2.0 * math.pi * math.e)) - (math.pi / 8.0)
    else:
        theta = 0.0

    return zeta_real * math.cos(theta) - zeta_imag * math.sin(theta)

def find_i_coefficient(low, high, tolerance=1e-5):
    """Finds exact t where Z(t) crosses zero using pure bisection."""
    for _ in range(50):
        mid = (low + high) / 2.0
        z_mid = riemann_siegel_z(mid)
        if abs(z_mid) < tolerance:
            return mid
        if riemann_siegel_z(low) * z_mid < 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2.0

# Scan the imaginary axis from t=10 to t=80 to catch all 20 values
step_size = 0.25
current_t = 10.0
max_t = 80.0
found_count = 0

print(f"Scanning t-axis from {current_t} to {max_t} for crossings...")
print("=" * 45)

prev_z = riemann_siegel_z(current_t)
while current_t < max_t:
    next_t = current_t + step_size
    next_z = riemann_siegel_z(next_t)
    
    # Direct sign change detected across the step interval
    if prev_z * next_z < 0:
        found_count += 1
        exact_t = find_i_coefficient(current_t, next_t)
        print(f"t_{found_count:<2} isolated at: {exact_t:.5f}")
        
    current_t = next_t
    prev_z = next_z

print("=" * 45)
