def exact_prime_count(x):
    """Returns pi(x): the exact number of primes up to x."""
    if x < 2:
        return 0
    
    # Boolean array representing primality
    sieve = [True] * (x + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(x**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, x + 1, i):
                sieve[j] = False
                
    return sum(1 for prime in sieve if prime)
def math_ln(x):
    """Pure Python natural logarithm approximation using Taylor/Halley method."""
    if x <= 0: raise ValueError("Math domain error")
    # Using a simple iterative approximation for ln(x)
    guess = 0.0
    for _ in range(100):
        # Local fast exp(guess)
        e_g = 1.0
        term = 1.0
        for i in range(1, 20):
            term *= (guess / i)
            e_g += term
        num = 2 * (x - e_g)
        den = x + e_g
        delta = num / den
        guess += delta
        if abs(delta) < 1e-12: break
    return guess

def logarithmic_integral(x, intervals=100):
    """Computes Li(x) using numerical integration (Trapezoidal Rule)."""
    if x < 2:
        return 0.0
    
    # We integrate from 2 to x to avoid the singularity at t=1
    a = 2.0
    b = float(x)
    h = (b - a) / intervals
    
    # Initial endpoints evaluation
    integral_sum = 0.5 * (1.0 / math_ln(a) + 1.0 / math_ln(b))
    
    # Sum up inner panels
    for i in range(1, intervals):
        t = a + i * h
        integral_sum += 1.0 / math_ln(t)
        
    return integral_sum * h

def analyze_prime_error_rates(x):
    """Calculates absolute and relative error rates for prime approximations."""
    pi_x = exact_prime_count(x)
    li_x = logarithmic_integral(x)
    pnt_x = x / math_ln(x) if x > 1 else 0
    
    # Absolute Errors
    abs_error_li = pi_x - li_x
    abs_error_pnt = pi_x - pnt_x
    
    # Relative Errors (Percentage)
    rel_error_li = (abs_error_li / pi_x) * 100 if pi_x > 0 else 0
    rel_error_pnt = (abs_error_pnt / pi_x) * 100 if pi_x > 0 else 0
    
    print(f"Analysis up to x = {x}:")
    print(f"  Exact Primes pi(x)      : {pi_x}")
    print(f"  Log Integral Li(x)      : {li_x:.2f}")
    print(f"  PNT Estimate x/ln(x)    : {pnt_x:.2f}")
    print("-" * 45)
    print(f"  Li(x) Absolute Error    : {abs_error_li:.2f}")
    print(f"  Li(x) Relative Error    : {rel_error_li:.4f}%")
    print(f"  PNT Absolute Error      : {abs_error_pnt:.2f}")
    print(f"  PNT Relative Error      : {rel_error_pnt:.4f}%")

# Test with a limit of 100,000
analyze_prime_error_rates(100)
def check_riemann_error_bound(x):
    """Verifies that the absolute error stays below the Riemann Hypothesis ceiling."""
    pi_x = exact_prime_count(x)
    li_x = logarithmic_integral(x)
    abs_error = abs(pi_x - li_x)
    
    # Compute the theoretical maximal error bound
    ln_x = math_ln(x)
    max_bound = (1.0 / (8 * 3.1415926535)) * (x**0.5) * ln_x
    
    print(f"Actual Absolute Error: {abs_error:.4f}")
    print(f"Riemann Allowed Limit: {max_bound:.4f}")
    print(f"Boundary Valid?      : {abs_error <= max_bound}")

check_riemann_error_bound(100)






    
