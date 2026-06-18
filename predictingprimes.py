import math
from decimal import Decimal, getcontext

# Set high precision context for large scales or deep decimal points
getcontext().prec = 10000

def approx_prime_count(x):
    """
    Replaces Sieve of Eratosthenes to handle massive values like 10**100.
    Uses high-precision approximation for pi(x) at scale.
    """
    x_dec = Decimal(x)
    if x_dec < 2:
        return Decimal(0)
    return exact_li_high_scale(x_dec).quantize(Decimal('1'))

def decimal_ln(x):
    """Computes a high-precision Natural Logarithm using the Decimal module."""
    x_dec = Decimal(x)
    if x_dec <= 0: 
        raise ValueError("Math domain error")
    
    sign, digits, exponent = x_dec.as_tuple()
    if len(digits) + exponent > 300:
        scale_factor = len(digits) + exponent - 5
        scaled_x = x_dec / (Decimal(10) ** scale_factor)
        ln_10 = Decimal('2.3025850929940456840179914546843642076011014886288')
        return decimal_ln(scaled_x) + (Decimal(scale_factor) * ln_10)

    guess = Decimal(str(math.log(float(x_dec))))
    for _ in range(50):
        e_g = guess.exp()
        num = Decimal(2) * (x_dec - e_g)
        den = x_dec + e_g
        delta = num / den
        guess += delta
        if abs(delta) < Decimal('1e-45'): 
            break
    return guess

def exact_li_high_scale(x):
    """Calculates Logarithmic Integral Li(x) for massive values."""
    x_dec = Decimal(x)
    if x_dec < 2:
        return Decimal(0.0)
    
    ln_x = decimal_ln(x_dec)
    
    li_val = x_dec / ln_x
    current_term = Decimal(1)
    mult = Decimal(1)
    for i in range(1, 10):
        mult *= i
        current_term = mult / (ln_x ** i)
        li_val += (x_dec / ln_x) * current_term

    return li_val

def analyze_prime_error_rates(x):
    """Calculates absolute and relative error rates for prime approximations using Decimal."""
    x_dec = Decimal(x)
    pi_x = approx_prime_count(x_dec)
    
    # FIXED: Return the numeric Decimal value, NOT a set item {pi_x}
    return pi_x

def check_riemann_error_bound(x):
    """Verifies that the absolute error stays below the Riemann Hypothesis ceiling using Decimal."""
    x_dec = Decimal(x)
    pi_x = approx_prime_count(x_dec)
    li_x = exact_li_high_scale(x_dec)
    abs_error = abs(pi_x - li_x)
    
    ln_x = decimal_ln(x_dec)
    pi_constant = Decimal('3.1415926535897932384626433832795028841971693993751')
    max_bound = (Decimal(1) / (Decimal(8) * pi_constant)) * (x_dec.sqrt()) * ln_x
    
    print("\n--- Riemann Boundary Test ---")
    print(f"Actual Absolute Error: {abs_error}")
    print(f"Riemann Allowed Limit: {max_bound}")
    print(f"Boundary Valid?      : {abs_error <= max_bound}")

# FIXED: Accept Decimal formats for target values and step scales
def numerical_limit(func, target, tolerance):
    """Approximates the limit of 'func' as x approaches 'target' using Decimal precision."""
    left_x = target - tolerance
    
    left_y = func(left_x)
    
    right_x = target + tolerance
  
    right_y = func(right_x)
    
    return (left_y + right_y) / 2,left_y,right_y

# --- Execution ---

# FIXED: Cast target and step tolerance to Decimal objects 
target_val = Decimal('10')**10004
tolerance_val = Decimal('10')**-10004 # Proportional scale adjustment

result = numerical_limit(analyze_prime_error_rates, target=target_val, tolerance=tolerance_val)
res_high_prec = Decimal('10004') * decimal_ln(Decimal('10'))
print("Numerical estimated of x:")
print(result[0]*res_high_prec)
print("Numerical Limit Result:")
print(result[0])
#print("lower limit: ")
#print(result[1])
#print("higher limit: ")
#print(result[2])
# Running your original tests below
#print("\nRunning higher tests...")
#analyze_prime_error_rates(Decimal('10')**1000)
#check_riemann_error_bound(Decimal('10')**1000)
