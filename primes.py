import math

def pure_riemann_r(x, max_terms=60):
    """Calculates Riemann's R(x) using Gram's series from scratch."""
    if x < 2:
        return 0.0

    # Internal helper to calculate the Riemann Zeta function for integer powers
    def compute_zeta(s):
        # Sums 1 / n^s up to a precision limit
        return sum(1.0 / (float(n) ** s) for n in range(1, 1500))

    ln_x = math.log(x)
    total = 1.0
    factorial = 1.0
    
    for k in range(1, max_terms):
        factorial *= k
        zeta_val = compute_zeta(k + 1)
        
        # Calculate the specific term in Gram's Series
        term = (ln_x ** k) / (k * factorial * zeta_val)
        
        # Stop looping if terms drop below machine floating-point relevance
        if abs(term) < 1e-12:
            break
            
        total += term
        
    return total

# --- Test Output ---
# Actual primes under 1000 is 168
print(f"Riemann R(1,000): {round(pure_riemann_r(1000))}")  # Outputs: 168
